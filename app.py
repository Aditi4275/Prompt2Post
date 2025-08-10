import os
import glob
import requests
import subprocess

# ==== CONFIG ====
OPENROUTER_API_KEY = os.getenv("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")  # export OPENROUTER_API_KEY="your-key"
ELEVENLABS_API_KEY = os.getenv("sk_6e804e4ca208a9ad33d459d4cf56de9450688d2559f442b4")  # export ELEVENLABS_API_KEY="your-key"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Example voice ID, replace with your own

# ==== STEP 1: Select a video from folder ====
def choose_video(folder_path):
    videos = glob.glob(os.path.join(folder_path, "*.mp4"))
    if not videos:
        raise FileNotFoundError("No MP4 videos found in folder.")
    print("\nAvailable videos:")
    for idx, video in enumerate(videos, start=1):
        print(f"{idx}. {video}")
    choice = int(input("\nSelect a video number: ")) - 1
    return videos[choice]

# ==== STEP 2: Get user prompt and generate script from OpenRouter ====
def generate_script(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",  # or another available model
        "messages": [
            {"role": "system", "content": "You are a creative scriptwriter."},
            {"role": "user", "content": f"Write a short voiceover script for: {prompt}"}
        ],
        "max_tokens": 200
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter API error: {response.text}")
    return response.json()["choices"][0]["message"]["content"].strip()

# ==== STEP 3: Use ElevenLabs to create audio ====
def generate_audio(script_text, output_audio="output.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
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

    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error: {response.text}")

    with open(output_audio, "wb") as f:
        f.write(response.content)
    return output_audio

# ==== STEP 4: Merge audio with video ====
def merge_audio_video(video_path, audio_path, output_path="final_video.mp4"):
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path

# ==== MAIN ====
if __name__ == "__main__":
    folder = input("Enter folder path containing videos: ").strip()
    video_path = choose_video(folder)
    user_prompt = input("Enter your idea for the video voiceover: ").strip()

    print("\nGenerating script...")
    script_text = generate_script(user_prompt)
    print("\nGenerated Script:\n", script_text)

    print("\nGenerating audio with ElevenLabs...")
    audio_file = generate_audio(script_text)

    print("\nMerging audio with video...")
    final_video = merge_audio_video(video_path, audio_file)

    print(f"\n✅ Done! Final video saved as: {final_video}")