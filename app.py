import os
import json
import time
import shutil
import requests
import subprocess
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

def get_trending_placeholders(num=10):
    base = [
        "Minecraft parkour clutch",
        "AITA wild twist",
        "Creepy late-night story",
        "Petty revenge at work",
        "Mind-blowing science facts",
        "History but funny",
        "Daily weird news",
        "Hot take: gaming",
        "AI fails compilation",
        "Productivity myths"
    ]
    return base[:num]

# Placeholder video creator to match your reference style
# Replace with your actual video logic or import from video_creator
def create_video_from_script(script_text, out_path="outputs/black_vo.mp4"):
    
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


# Load env
load_dotenv()

# ---- API Keys ----
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
VOICE_ID = st.secrets["ELEVENLABS_VOICE_ID"]

# ---- OpenRouter / ElevenLabs Config ----
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# Pick a model accessible to your account
MODEL_ID = "moonshotai/kimi-k2:free"
ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# ---- Streamlit Page Config ----
st.set_page_config(
    page_title="Viral Video Maker",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="auto",
)

# ---- Title ----
st.title("🎬 AI Viral Video Maker")
st.markdown("Turn trending topics into engaging videos with one click.")


# ---- Topic selection (mirrors reference selectbox) ----
trending_options = get_trending_placeholders(num=10)
selected_trend = st.selectbox("Choose a trending topic:", trending_options)


# ---- Helpers ----
def require_bin(cmd_name: str):
    if shutil.which(cmd_name) is None:
        raise EnvironmentError(f"{cmd_name} not found. Install it and add to PATH.")

def test_openrouter(prompt="Write a 2-sentence fun fact about space.") -> (bool, str):
    if not OPENROUTER_API_KEY:
        return False, "OPENROUTER_API_KEY not set."
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
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
        return False, f"Network error: {e}"
    if resp.status_code != 200:
        try:
            return False, json.dumps(resp.json(), indent=2)
        except Exception:
            return False, resp.text
    try:
        content = resp.json()["choices"][0]["message"]["content"].strip()
        return True, content
    except Exception as e:
        return False, f"Parse error: {e}\nBody: {resp.text[:800]}"

def generate_script(prompt: str) -> str:
    if not OPENROUTER_API_KEY:
        raise EnvironmentError("OPENROUTER_API_KEY not set.")
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a creative scriptwriter. Write concise, punchy lines."},
            {"role": "user", "content": f"Write a tight 2-4 sentence voiceover script (max 60 words) for: {prompt}"}
        ],
        "max_tokens": 220,
        "temperature": 0.8
    }
    resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"OpenRouter API error: {resp.status_code} {resp.text}")
    payload = resp.json()
    return payload["choices"][0]["message"]["content"].strip()

def generate_audio(script_text: str, output_audio: str = "voiceover.mp3") -> str:
    if not ELEVENLABS_API_KEY:
        raise EnvironmentError("ELEVENLABS_API_KEY not set.")
    if not VOICE_ID:
        raise EnvironmentError("ELEVENLABS_VOICE_ID not set.")
    url = f"{ELEVENLABS_TTS_URL}/{VOICE_ID}"
    headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY}
    data = {
        "text": script_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    resp = requests.post(url, json=data, headers=headers, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error: {resp.status_code} {resp.text}")
    with open(output_audio, "wb") as f:
        f.write(resp.content)
    return output_audio


# ---- Main Button Action (mirrors your reference flow) ----
if st.button("🚀 Generate Video on a Trending Topic"):
    if not OPENROUTER_API_KEY or not ELEVENLABS_API_KEY or not VOICE_ID:
        st.error("Please set OPENROUTER_API_KEY, ELEVENLABS_API_KEY, and ELEVENLABS_VOICE_ID in your .env file.")
    else:
        try:
            # Check binaries
            require_bin("ffmpeg")
            require_bin("ffprobe")

            trend = selected_trend
            st.info(f"🔥 Trending Topic Selected: {trend}")

            # Optional: quick OpenRouter test inline (can remove if noisy)
            with st.spinner("✅ Testing OpenRouter…"):
                ok, msg = test_openrouter(f"Write a short 2-3 sentence about {trend}.")
                if not ok:
                    st.warning("OpenRouter test failed, but attempting generation anyway.")
                else:
                    st.caption("OpenRouter test passed.")

            # Generate script
            with st.spinner(f"✍️ Generating script for '{trend}'..."):
                script = generate_script(trend)

            # Generate audio
            with st.spinner("🎙️ Generating voiceover (ElevenLabs)…"):
                audio_path = generate_audio(script, "voiceover.mp3")

            # Create placeholder video (black with VO)
            with st.spinner("🎬 Creating video..."):
                video_path = create_video_from_script(script)

            if video_path and os.path.exists(video_path):
                st.success("🎉 Your video is ready!")
                st.balloons()

                col1, col2 = st.columns([3, 2])
                with col1:
                    st.video(video_path)
                    with open(video_path, "rb") as file:
                        st.download_button(
                            label="📥 Download Video",
                            data=file,
                            file_name=os.path.basename(video_path),
                            mime="video/mp4"
                        )
                with col2:
                    st.subheader("📝 Script")
                    st.text_area("", value=script, height=180)
                    st.subheader("＃ Hashtags (suggested)")
                    st.text_area("", value="#shorts #gaming #minecraft #ai", height=60)

            else:
                st.error("Failed to create the video. Check logs for errors.")

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
