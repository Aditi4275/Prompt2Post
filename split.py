import subprocess
import os

def split_video_ffmpeg(input_path, output_dir, fragment_duration=30):
    """
    Splits a video into fragments using ffmpeg.

    Args:
        input_path (str): Path to the input video file.
        output_dir (str): Directory to save the fragments.
        fragment_duration (int): Duration of each fragment in seconds.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_pattern = os.path.join(output_dir, "fragment_%03d.mp4")
    
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c", "copy",
        "-map", "0",
        "-f", "segment",
        "-segment_time", str(fragment_duration),
        output_pattern
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Video split into {fragment_duration}-second fragments in '{output_dir}'")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while splitting video: {e}")

# Example usage:
split_video_ffmpeg("input.mp4", "fragments", fragment_duration=30)
