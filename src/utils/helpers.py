import os
import shutil
import subprocess
import glob
import random

def require_bin(cmd_name: str):
    """Check if a required binary is available in PATH."""
    if shutil.which(cmd_name) is None:
        raise EnvironmentError(f"Required binary not found: {cmd_name}. Please install it and ensure it's on PATH.")


def get_duration(path: str) -> float:
    """Get the duration of a media file in seconds."""
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", path
        ]
        out = subprocess.check_output(cmd, text=True).strip()
        return float(out)
    except Exception as e:
        raise RuntimeError(f"Failed to get duration for {path}: {e}")


def list_video_fragments(folder_path=None):
    if folder_path is None:
        # Go up 3 levels: src/utils/helpers.py -> src/utils -> src -> root
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        folder_path = os.path.join(base_dir, "templates")

    """List all video fragments in the templates directory."""
    try:
        exts = ("*.mp4", "*.mov", "*.mkv", "*.webm", "*.m4v")
        videos = []
        for ext in exts:
            videos.extend(glob.glob(os.path.join(folder_path, ext)))
        return sorted(videos)
    except Exception as e:
        raise RuntimeError(f"Failed to list video fragments: {e}")

def select_random_fragment(folder_path=None):
    """Select a random video fragment from the templates directory."""
    try:
        fragments = list_video_fragments(folder_path)
        if not fragments:
            raise FileNotFoundError("No video fragments found in the templates directory.")
        return random.choice(fragments)
    except Exception as e:
        raise RuntimeError(f"Failed to select random fragment: {e}")

def format_text_for_video(text: str, max_chars_per_line: int = 40) -> str:
    """Format text for better display on video (wrap long lines)."""
    try:
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            if len(" ".join(current_line + [word])) <= max_chars_per_line:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word[:max_chars_per_line])
                    remaining = word[max_chars_per_line:]
                    while remaining:
                        lines.append(remaining[:max_chars_per_line])
                        remaining = remaining[max_chars_per_line:]
                    current_line = []
        
        if current_line:
            lines.append(" ".join(current_line))
        
        formatted_text = "\n".join(lines)
        return formatted_text
    except Exception as e:
        return text

