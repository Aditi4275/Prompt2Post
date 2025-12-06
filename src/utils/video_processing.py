import os
import subprocess
from pathlib import Path
from src.utils.helpers import format_text_for_video

def add_text_overlay(video_path: str, text: str, output_path: str) -> str:
    """Add text overlay to a video."""
    try:
        # Escape special characters for FFmpeg drawtext
        # 1. Escape single quotes with backslash
        # 2. Escape colons with backslash
        formatted_text = format_text_for_video(text)
        safe_text = formatted_text.replace("'", r"\'").replace(":", r"\:")
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                   f"text='{safe_text}':"
                   f"fontcolor=white:"
                   f"fontsize=24:"
                   f"box=1:"
                   f"boxcolor=black@0.5:"
                   f"boxborderw=5:"
                   f"x=(w-text_w)/2:"
                   f"y=(h-text_h)/2",
            "-c:a", "copy",
            output_path
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")
    except Exception as e:
        raise RuntimeError(f"Error adding text overlay: {str(e)}")

def merge_audio_video(video_path: str, audio_path: str, output_path: str = "final_video.mp4") -> str:
    """Merge audio with video."""
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "libx264",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")
    except Exception as e:
        raise RuntimeError(f"Error merging audio and video: {str(e)}")
