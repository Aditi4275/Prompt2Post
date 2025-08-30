import os
import subprocess
from pathlib import Path
from src.utils.helpers import format_text_for_video

def add_text_overlay(video_path: str, text: str, output_path: str) -> str:
    """Add text overlay to a video."""
    try:
        # Format text for better display (wrap long lines)
        formatted_text = format_text_for_video(text)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                   f"text='{formatted_text}':"
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

def create_video_from_script(script_text: str, out_path="outputs/black_vo.mp4"):
    """Create a video from script (placeholder implementation)."""
    audio = Path("voiceover.mp3")
    if not audio.exists():
        raise FileNotFoundError("Expected voiceover.mp3 to exist. Generate audio first.")

    out_dir = Path(out_path).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Probe audio duration
        dur_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio)
        ]
        audio_dur = float(subprocess.check_output(dur_cmd, text=True).strip())
    except Exception as e:
        raise RuntimeError(f"Failed to read audio duration: {e}")

    black_tmp = "black.mp4"
    # Create black video slightly longer than audio, then cut shortest at merge
    cmd_black = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=black:s=1080x1920:r=60",
        "-t", f"{audio_dur + 0.2:.2f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        black_tmp
    ]
    subprocess.run(cmd_black, check=True)

    # Merge black video with audio
    cmd_merge = [
        "ffmpeg", "-y",
        "-i", black_tmp,
        "-i", str(audio),
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(out_path)
    ]
    subprocess.run(cmd_merge, check=True)

    try:
        os.remove(black_tmp)
    except OSError:
        pass

    return str(out_path)