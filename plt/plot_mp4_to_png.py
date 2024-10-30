import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
from datetime import datetime
from PIL import Image, ImageOps  # 使用PIL进行图片操作


def extract_and_concatenate_frames(
    video_path, n, decay_factor=1.0, show_image=True, layout="horizontal"
):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps  # Calculate video duration in seconds

    # Compute the frame indices to capture frames at
    frame_indices = []
    for i in range(n - 1):  # First n-1 frames
        # Use exponential decay to adjust the frame indices
        time_ratio = (i / (n - 1)) ** decay_factor  # Adjust with decay factor
        frame_time = time_ratio * duration  # Time position in seconds
        frame_idx = int(frame_time * fps)  # Corresponding frame index

        # Ensure frame index is within bounds
        if frame_idx >= total_frames:
            frame_idx = total_frames - 1
        frame_indices.append(frame_idx)

    # Ensure last frame is always the last frame of the video
    frame_indices.append(total_frames - 1)

    # To store all captured frames
    frames = []

    # Capture each frame
    for frame_idx in frame_indices:
        # Set the position of the video to the frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

        # Read the frame
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Could not read frame at index {frame_idx}")
            continue

        # Convert from BGR (OpenCV default) to RGB for visualization
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)

    # Release video capture
    cap.release()

    # Check if we captured any frames
    if len(frames) == 0:
        print(f"Error: No frames were captured from {video_path}.")
        return

    # Concatenate frames based on the layout
    if layout == "horizontal":
        # Concatenate frames horizontally (left to right)
        concatenated_image = np.hstack(frames)

        # Convert the concatenated image (numpy array) to a PIL Image
        concatenated_image = Image.fromarray(concatenated_image)

    elif layout == "grid":
        # Check if the number of frames can form a perfect square
        m = int(np.sqrt(len(frames)))
        if m * m != len(frames):
            raise ValueError(
                f"Cannot arrange {len(frames)} frames into a perfect square grid."
            )

        # Resize frames to match in size for grid arrangement
        frame_height, frame_width, _ = frames[0].shape
        concatenated_image = Image.new("RGB", (m * frame_width, m * frame_height))

        # Arrange frames into an m x m grid
        for i in range(m):
            for j in range(m):
                frame = Image.fromarray(frames[i * m + j])
                concatenated_image.paste(frame, (j * frame_width, i * frame_height))
    else:
        raise ValueError(f"Invalid layout option: {layout}")

    # Optionally display the concatenated image
    if show_image:
        plt.imshow(concatenated_image)
        plt.axis("off")  # Turn off axis
        plt.show()

    # Save the concatenated image to a new 'images' folder within the same directory as the video
    video_dir = os.path.dirname(video_path)
    images_dir = os.path.join(video_dir, "images")

    # Create the 'images' folder if it doesn't exist
    os.makedirs(images_dir, exist_ok=True)

    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Add a timestamp to ensure unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(images_dir, f"{video_name}_concatenated_{timestamp}.png")

    # Save the image
    concatenated_image.save(save_path)
    print(f"Image saved to: {save_path}")

    return save_path  # Return the path of the saved image


def process_folder(
    folder_path,
    n,
    decay_factor=1.0,
    show_image=True,
    max_images=None,
    layout="horizontal",
):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist.")
        return

    # Create the 'images' folder if it doesn't exist
    images_dir = os.path.join(folder_path, "images")
    os.makedirs(images_dir, exist_ok=True)

    # Check existing images in the 'images' folder
    existing_images = [
        os.path.join(images_dir, f)
        for f in os.listdir(images_dir)
        if f.endswith(".png")
    ]

    # If max_images is provided and already enough images exist, skip generation
    if max_images is not None and len(existing_images) >= max_images:
        print(f"Found {len(existing_images)} images, no need to generate more.")
        compose_images(folder_path, existing_images[:max_images], max_images)
        return

    # Create a list to store paths of all newly generated images
    generated_images = []

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Process only MP4 files
        if filename.lower().endswith(".mp4"):
            video_path = os.path.join(folder_path, filename)
            print(f"Processing video: {video_path}")
            image_path = extract_and_concatenate_frames(
                video_path, n, decay_factor, show_image, layout
            )
            if image_path:
                generated_images.append(image_path)
        else:
            print(f"Skipping non-MP4 file: {filename}")

    # Combine newly generated images with existing images
    all_images = existing_images + generated_images

    # If images were generated, concatenate them vertically
    if all_images:
        compose_images(folder_path, all_images, max_images)


def compose_images(folder_path, image_paths, max_images=None):
    # Create the 'images_compose' folder inside the 'images' folder
    images_dir = os.path.join(folder_path, "images")
    images_compose_dir = os.path.join(images_dir, "images_compose")
    os.makedirs(images_compose_dir, exist_ok=True)

    # If max_images is provided and fewer images exist, select only the specified number of images
    if max_images is not None and len(image_paths) > max_images:
        image_paths = image_paths[:max_images]

    # Load all images
    images = [Image.open(img_path) for img_path in image_paths]

    # Find the total width and height for the final concatenated image
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)

    # Create a blank image with the calculated width and height
    composed_image = Image.new("RGB", (max_width, total_height))

    # Paste each image vertically
    y_offset = 0
    for img in images:
        composed_image.paste(img, (0, y_offset))
        y_offset += img.height

    # Save the final composed image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    composed_image_path = os.path.join(
        images_compose_dir, f"composed_image_{len(images)}_images_{timestamp}.png"
    )
    composed_image.save(composed_image_path)

    print(f"Composed image saved to: {composed_image_path}")


# Example usage
if __name__ == "__main__":
    # input_path = "/home/qiao/Downloads/real_word_exp/grasp-movie.mp4"
    input_path = "/home/qiao/Projects/GraspDiffusionNetwork/grasp_diffusion_network/scripts/eval/checkpoints_evaluations_trash/GraspGeneratorDiffusionEuclidean/1730121411/grasp_generation_animations"
    n = 10
    decay_factor = 0.1
    show_image = False  # Set to True to display the generated image
    max_images = 10  # Change this to control the number of images to be concatenated
    layout = "horizontal"  # Use 'horizontal' for horizontal arrangement or 'grid' for m x m grid arrangement
    # layout = "grid"  # Use 'horizontal' for horizontal arrangement or 'grid' for m x m grid arrangement

    # Check if the input is a directory or a file
    if os.path.isdir(input_path):
        process_folder(input_path, n, decay_factor, show_image, max_images, layout)
    elif os.path.isfile(input_path) and input_path.lower().endswith(".mp4"):
        # For individual MP4 files, only generate images but don't compose vertically
        extract_and_concatenate_frames(input_path, n, decay_factor, show_image, layout)
    else:
        print(
            "Error: Invalid input path. Please provide a valid MP4 file or folder containing MP4 files."
        )
