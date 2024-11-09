import ffmpeg
import os

def mp4_to_gif(input_path: str, output_path: str, fps: int = 10, scale: int = 640, loop: int = 0):
    """
    将 MP4 文件转换为 GIF 动图。
    
    参数：
    - input_path: str，输入的 MP4 文件的绝对路径
    - output_path: str，输出的 GIF 文件路径
    - fps: int，指定的帧率 (默认 10)
    - scale: int，指定 GIF 的宽度，保持高度按比例缩放 (默认 640)
    - loop: int，GIF 循环次数 (0 表示无限循环)
    """
    
    # 检查输入文件是否存在
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"输入文件 {input_path} 不存在")
    
    # 创建 FFmpeg 转换流
    try:
        # 使用 filter 生成调色板
        palette_path = output_path.replace('.gif', '_palette.png')
        (
            ffmpeg
            .input(input_path)
            .filter('fps', fps)
            .filter('scale', scale, -1, flags='lanczos')
            .output(palette_path, vf='palettegen')
            .run(quiet=True)
        )

        # 使用生成的调色板转换为 GIF
        (
            ffmpeg
            .input(input_path)
            .filter('fps', fps)
            .filter('scale', scale, -1, flags='lanczos')
            .input(palette_path)
            .filter('paletteuse')
            .output(output_path, loop=loop)
            .run(quiet=True)
        )

        # 删除临时的调色板文件
        os.remove(palette_path)
        print(f"转换成功！GIF 已保存至 {output_path}")
    except ffmpeg.Error as e:
        print(f"转换失败: {e.stderr.decode()}")

# 使用示例
mp4_to_gif(
    input_path='/home/qiao/Projects/pytools/data/real_word_mp4/grasp-movie (1).mp4',  # 输入 MP4 文件路径
    output_path='/path/to/output.gif', # 输出 GIF 文件路径
    fps=10,  # GIF 帧率
    scale=1320,  # GIF 宽度（高度自动按比例缩放）
    loop=0   # GIF 循环次数 (0 为无限循环)
)
