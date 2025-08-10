# app.py
# Corrected script with a working OpenRouter key test function, fixed typos, and safe flow.

import os
import glob
import json
import time
import shutil
import requests
import subprocess
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


# ==== CONFIG (env vars preferred) ====
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")  # e.g., "21m00Tcm4TlvDq8ikWAM"

MODEL_ID = "moonshotai/kimi-k2:free"  # change to another available model if desired
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Optional: align audio length to video
ALIGN_AUDIO_TO_VIDEO = False  # set True to trim/loop audio to match video duration (requires ffmpeg)


# ==== UTILITIES ====
def require_bin(cmd_name: str):
    if shutil.which(cmd_name) is None:
        raise EnvironmentError(f"Required binary not found: {cmd_name}. Please install it and ensure it's on PATH.")


def safe_int_input(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val <= val <= max_val:
                return val
        except ValueError:
            pass
        print(f"Enter a number between {min_val} and {max_val}.")


def list_videos(folder_path: str):
    exts = ("*.mp4", "*.mov", "*.mkv", "*.webm", "*.m4v")
    videos = []
    for ext in exts:
        videos.extend(glob.glob(os.path.join(folder_path, ext)))
    return sorted(videos)


def get_duration(path: str) -> float:
    # Use ffprobe to get media duration in seconds
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    return float(out)


def pad_or_trim_audio(audio_path: str, target_seconds: float, out_path: str):
    # If audio is longer, trim; if shorter, loop to match target
    dur = get_duration(audio_path)
    if abs(dur - target_seconds) < 0.05:
        # close enough
        return audio_path

    if dur > target_seconds:
        # trim to target_seconds
        cmd = ["ffmpeg", "-y", "-i", audio_path, "-t", f"{target_seconds:.3f}", "-c", "copy", out_path]
        subprocess.run(cmd, check=True)
        return out_path
    else:
        # loop to reach target_seconds
        temp = out_path.replace(".mp3", "_long.tmp.mp3")
        # stream_loop N-1 repeats the input N times total
        reps = max(2, int(target_seconds // max(0.1, dur)) + 1)
        cmd1 = ["ffmpeg", "-y", "-stream_loop", str(reps - 1), "-i", audio_path, "-c", "copy", temp]
        subprocess.run(cmd1, check=True)
        # then trim to exact length
        cmd2 = ["ffmpeg", "-y", "-i", temp, "-t", f"{target_seconds:.3f}", "-c", "copy", out_path]
        subprocess.run(cmd2, check=True)
        try:
            os.remove(temp)
        except OSError:
            pass
        return out_path


# ==== STEP 1: Select a video from folder ====
def choose_video(folder_path: str) -> str:
    videos = list_videos(folder_path)
    if not videos:
        raise FileNotFoundError("No videos found in folder (supported: .mp4, .mov, .mkv, .webm, .m4v).")
    print("\nAvailable videos:")
    for idx, video in enumerate(videos, start=1):
        print(f"{idx}. {video}")
    choice = safe_int_input("\nSelect a video number: ", 1, len(videos)) - 1
    return videos[choice]


# ==== STEP 2: Get user prompt and generate script from OpenRouter ====
def generate_script(prompt: str) -> str:
    if not OPENROUTER_API_KEY:
        raise EnvironmentError("OPENROUTER_API_KEY is not set.")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a creative scriptwriter. Write concise, punchy lines."},
            {"role": "user", "content": f"Write a tight 2-4 sentence voiceover script (max 60 words) for: {prompt}"}
        ],
        "max_tokens": 220,
        "temperature": 0.8
    }
    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
    except requests.RequestException as e:
        raise RuntimeError(f"OpenRouter request failed: {e}")
    if resp.status_code != 200:
        raise RuntimeError(f"OpenRouter API error: {resp.status_code} {resp.text}")

    try:
        payload = resp.json()
        content = payload["choices"][0]["message"]["content"].strip()
        return content
    except (KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Unexpected OpenRouter response format: {e}\nBody: {resp.text[:500]}")


# ==== Quick test for OpenRouter API key (fixed typo and improved output) ====
def test_openrouter(prompt="Write a 2-sentence fun fact about space.") -> bool:
    if not OPENROUTER_API_KEY:
        raise EnvironmentError("OPENROUTER_API_KEY environment variable is not set.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a concise scriptwriter."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 120,
        "temperature": 0.7,
    }

    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
    except requests.RequestException as e:
        print("❌ Network or request error:", e)
        return False

    print(f"\n🔹 HTTP Status: {resp.status_code}")

    # Try to decode JSON, or show raw body if it's not JSON
    try:
        payload = resp.json()
        # Print a compact summary instead of the full blob
        print("\n📜 Response keys:", list(payload.keys()))
    except json.JSONDecodeError:
        print("\n❌ Response is not valid JSON. Raw text:")
        print(resp.text[:1000])
        return False

    # Try extracting the model output if present
    try:
        content = payload["choices"][0]["message"]["content"].strip()
        print("\n✅ Model Output:\n", content)
        return resp.status_code == 200
    except (KeyError, IndexError) as e:
        print("\n⚠️ Could not find model output in response:", e)
        print("Partial JSON:", json.dumps(payload, indent=2)[:1500])
        return False


# ==== STEP 3: Use ElevenLabs to create audio ====
def generate_audio(script_text: str, output_audio: str = "output.mp3") -> str:
    if not ELEVENLABS_API_KEY:
        raise EnvironmentError("ELEVENLABS_API_KEY is not set.")
    if not VOICE_ID:
        raise EnvironmentError("ELEVENLABS_VOICE_ID is not set.")
    url = f"{ELEVENLABS_TTS_URL}/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": script_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=60)
    except requests.RequestException as e:
        raise RuntimeError(f"ElevenLabs request failed: {e}")
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error: {resp.status_code} {resp.text}")

    with open(output_audio, "wb") as f:
        f.write(resp.content)
    return output_audio


# ==== STEP 4: Merge audio with video ====
def merge_audio_video(video_path: str, audio_path: str, output_path: str = "final_video.mp4") -> str:
    # If codecs are fine, copy video and encode AAC if needed for compatibility
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",  # stop when the shortest stream ends
        output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path


def main():
    # Optional: sanity check OpenRouter key before doing anything else
    print("Testing OpenRouter API key...")
    ok = test_openrouter("Write a short 2-4 sentence voiceover script about a daring Minecraft parkour escape.")
    print("OpenRouter test:", "PASS" if ok else "FAIL")
    if not ok:
        print("Aborting because OpenRouter key test failed.")
        return

    require_bin("ffmpeg")
    require_bin("ffprobe")

    folder = input("Enter folder path containing videos: ").strip()
    if not folder:
        raise ValueError("Folder path cannot be empty.")
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"Not a directory: {folder}")

    video_path = choose_video(folder)
    user_prompt = input("Enter your idea for the video voiceover: ").strip()
    if not user_prompt:
        raise ValueError("Prompt cannot be empty.")

    print("\nGenerating script...")
    script_text = generate_script(user_prompt)
    print("\nGenerated Script:\n", script_text)

    print("\nGenerating audio with ElevenLabs...")
    audio_file = "voiceover.mp3"
    audio_file = generate_audio(script_text, audio_file)

    if ALIGN_AUDIO_TO_VIDEO:
        print("\nAligning audio length to video duration...")
        vid_dur = get_duration(video_path)
        audio_aligned = "voiceover_aligned.mp3"
        audio_file = pad_or_trim_audio(audio_file, vid_dur, audio_aligned)

    # Create output filename based on input video name
    base = Path(video_path).stem
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    final_name = f"{base}_vo_{timestamp}.mp4"

    print("\nMerging audio with video...")
    final_video = merge_audio_video(video_path, audio_file, final_name)

    print(f"\n✅ Done! Final video saved as: {final_video}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
