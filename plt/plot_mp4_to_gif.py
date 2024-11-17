import ffmpeg
from pathlib import Path
from PIL import Image
import tempfile


def mp4_to_gif(
    input_folder: str,
    output_folder: str,
    fps: int = 10,
    scale: int = 320,
    colors: int = 128,
    loop: int = 0,
    hold_last_frame: float = 1.0,
    frame_duration: int = 20,
    generate_individual: bool = True,
    rows: int = 1,
    cols: int = 1,
):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    if generate_individual:
        for mp4_file in input_folder.glob("*.mp4"):
            convert_single_mp4_to_gif(
                mp4_file,
                output_folder,
                fps,
                scale,
                colors,
                loop,
                hold_last_frame,
                frame_duration,
            )
    else:
        output_folder_merge = output_folder / "merge"
        output_folder_merge.mkdir(parents=True, exist_ok=True)
        mp4_to_merged_gif(
            input_folder,
            output_folder_merge,
            fps,
            scale,
            colors,
            loop,
            hold_last_frame,
            frame_duration,
            rows,
            cols,
        )


def mp4_to_merged_gif(
    input_folder: str,
    output_folder: str,
    fps: int,
    scale: int,
    colors: int,
    loop: int,
    hold_last_frame: float,
    frame_duration: int,
    rows: int,
    cols: int,
):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    mp4_files = list(input_folder.glob("*.mp4"))
    required_count = rows * cols
    if len(mp4_files) < required_count:
        raise ValueError(
            f"Insufficient number of MP4 files in the folder, {required_count} needed, but only {len(mp4_files)} found."
        )

    mp4_files = mp4_files[:required_count]
    all_frames = []
    all_durations = []
    last_frames = []

    # Extract frames from each MP4 file and load into memory
    for mp4_file in mp4_files:
        frames, durations, last_frame = extract_frames_from_mp4(
            mp4_file, fps, scale, colors, frame_duration, hold_last_frame
        )
        all_frames.append(frames)
        all_durations.append(durations)
        last_frames.append(last_frame)  # Collect the last frame of each video

    max_frames = max(len(frames) for frames in all_frames)
    grid_frames = []
    grid_durations = []

    for i in range(max_frames):
        grid_frame_images = []
        current_durations = []
        for idx, frames in enumerate(all_frames):
            img = frames[i % len(frames)]
            grid_frame_images.append(img)
            current_durations.append(all_durations[idx][i % len(frames)])

        grid_width = grid_frame_images[0].width * cols
        grid_height = grid_frame_images[0].height * rows
        grid_image = Image.new("RGBA", (grid_width, grid_height))

        for r in range(rows):
            for c in range(cols):
                img = grid_frame_images[r * cols + c]
                grid_image.paste(img, (c * img.width, r * img.height))

        grid_frames.append(grid_image)
        grid_durations.append(max(current_durations))

    # Set hold time for the last frame
    grid_durations[-1] = int(hold_last_frame * 1000)

    output_path = (
        output_folder
        / f"merged_{rows * cols}_gifs_hold_{int(hold_last_frame*1000)}ms.gif"
    )
    grid_frames[0].save(
        output_path,
        save_all=True,
        append_images=grid_frames[1:],
        duration=grid_durations,
        loop=loop,
    )

    print(f"Successfully created merged GIF grid! Saved to {output_path}")


def convert_single_mp4_to_gif(
    mp4_path: Path,
    output_folder: str,
    fps: int,
    scale: int,
    colors: int,
    loop: int,
    hold_last_frame: float,
    frame_duration: int,
):
    base_name = mp4_path.stem
    output_path = os.path.join(output_folder, f"{base_name}.gif")

    with tempfile.NamedTemporaryFile(suffix=".gif", delete=True) as temp_gif:
        try:
            ffmpeg.input(str(mp4_path), r=fps).output(
                temp_gif.name,
                vf=f"fps={fps},scale={scale}:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors={colors}[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5",
                loop=loop,
            ).run(quiet=True, overwrite_output=True)

            frames, durations, last_frame = load_frames_from_gif(
                temp_gif.name, frame_duration, hold_last_frame
            )

            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=loop,
            )
            print(f"Single GIF generated successfully! Saved to {output_path}")
        except ffmpeg.Error as e:
            print(f"Conversion failed: {e.stderr.decode()}")


def load_frames_from_gif(gif_path, frame_duration, hold_last_frame):
    frames = []
    durations = []
    last_frame = None
    with Image.open(gif_path) as img:
        for i in range(img.n_frames):
            img.seek(i)
            frame = img.copy()
            frames.append(frame)
            durations.append(frame_duration)
            last_frame = frame  # Record the last frame

    durations[-1] = int(hold_last_frame * 1000)  # Set hold time for the last frame
    return frames, durations, last_frame


def extract_frames_from_mp4(
    mp4_path, fps, scale, colors, frame_duration, hold_last_frame
):
    with tempfile.NamedTemporaryFile(
        suffix=".gif", delete=True
    ) as temp_gif, tempfile.NamedTemporaryFile(
        suffix=".png", delete=True
    ) as last_frame_file:

        try:
            ffmpeg.input(str(mp4_path), r=fps).output(
                temp_gif.name,
                vf=f"fps={fps},scale={scale}:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors={colors}[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5",
            ).run(quiet=True, overwrite_output=True)

            ffmpeg.input(str(mp4_path), ss="999999", r=1).output(
                last_frame_file.name, vframes=1
            ).run(quiet=True, overwrite_output=True)

            frames, durations, last_frame = load_frames_from_gif(
                temp_gif.name, frame_duration, hold_last_frame
            )

            # Load the last frame image
            with Image.open(last_frame_file.name) as img:
                last_frame = img.copy()

            return frames, durations, last_frame

        except ffmpeg.Error as e:
            print(f"Failed to extract frames from MP4: {e.stderr.decode()}")
            return [], [], None


# Example code
mp4_to_gif(
    input_folder="/home/qiao/Projects/pytools/data/gdn_grasps",  # Path to input MP4 folder
    output_folder="/home/qiao/Projects/pytools/output/gifs/gdn_grasps",  # Path to output GIF folder
    fps=5,
    scale=320,
    colors=128,
    loop=0,
    hold_last_frame=0.5,
    frame_duration=20,
    generate_individual=False,  # True for individual GIFs, False for merged grid GIF
    rows=4,
    cols=6,
)
