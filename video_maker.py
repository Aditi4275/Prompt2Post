import os
import time
import random
from pathlib import Path

from src.config.settings import OPENROUTER_API_KEY, ELEVENLABS_API_KEY, VOICE_ID
from src.utils.helpers import require_bin, list_video_fragments, select_random_fragment, format_text_for_video
from src.utils.ai_services import generate_script, generate_audio
from src.utils.video_processing import add_text_overlay, merge_audio_video

def create_video(topic: str) -> str:
    \"\"\"Create a video from a topic.\"\"\"
    # Check required tools
    require_bin("ffmpeg")
    require_bin("ffprobe")
    
    print(f"Generating content for topic: {topic}")
    
    # Step 1: Generate script
    print("Generating script...")
    script_text = generate_script(topic)
    print(f"Script: {script_text}")
    
    # Step 2: Select random video fragment
    print("Selecting random video fragment...")
    fragment_path = select_random_fragment()
    print(f"Selected fragment: {fragment_path}")
    
    # Step 3: Generate audio
    print("Generating audio...")
    audio_path = generate_audio(script_text, "voiceover.mp3")
    
    # Step 4: Add text overlay to video fragment
    print("Adding text overlay to video...")
    video_with_text = "video_with_text.mp4"
    add_text_overlay(fragment_path, script_text, video_with_text)
    
    # Step 5: Merge audio with video
    print("Merging audio with video...")
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    final_video = f"outputs/video_{timestamp}.mp4"
    
    # Create outputs directory if it doesn't exist
    Path("outputs").mkdir(exist_ok=True)
    
    merge_audio_video(video_with_text, audio_path, final_video)
    
    # Clean up temporary files
    try:
        os.remove("voiceover.mp3")
        os.remove("video_with_text.mp4")
    except OSError:
        pass
    
    return final_video

def main():
    \"\"\"Main entry point.\"\"\"
    print("AI Video Maker")
    print("=" * 30)
    
    # Get topic from user
    topic = input("Enter the topic you want to create a video about: ").strip()
    
    if not topic:
        print("Topic cannot be empty!")
        return
    
    try:
        # Create the video
        video_path = create_video(topic)
        print(f"\n✅ Video successfully created: {video_path}")
        print("You can now download and play the video.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()