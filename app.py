import os
import time
import random
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Import our modules
try:
    from src.utils.ai_services import generate_script, generate_audio, test_openrouter
    from src.utils.video_processing import add_text_overlay, merge_audio_video
    from src.utils.helpers import require_bin, select_random_fragment
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# ---- API Keys Configuration ----
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
    VOICE_ID = st.secrets["ELEVENLABS_VOICE_ID"]
except:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

# ---- Streamlit Page Config ----
st.set_page_config(
    page_title="Prompt2Post",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- Header Section ----
st.title("🎬 Prompt2Post")
st.markdown("Turn any topic into engaging videos with AI-generated scripts and voiceovers!")

# ---- Sidebar ----
with st.sidebar:
    
    st.header("How to Use")
    st.markdown("""
    1. Enter a topic or select a trending one
    2. Click 'Generate Video'
    3. Wait for the AI to create your video
    4. Download and share!
    """)
    

# ---- Main Content ----

trending_topics = [
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

# Topic input section
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Choose a topic")
    topic_option = st.radio("Select input method:", ["Trending Topics", "Custom Topic"])
    
    if topic_option == "Trending Topics":
        selected_topic = st.selectbox("Select a trending topic:", trending_topics)
        topic = selected_topic
    else:
        custom_topic = st.text_input("Enter your own topic:")
        topic = custom_topic

with col2:
    st.subheader("Preview")
    if topic:
        st.info(f"Selected: {topic}")
    else:
        st.info("No topic selected")

# Generate button
generate_button = st.button("🚀 Generate Video", type="primary", use_container_width=True)

# ---- Video Generation Process ----
if generate_button:
    
    if not topic:
        st.error("Please select a topic or enter a custom one!")
        st.stop()
        
    if not OPENROUTER_API_KEY or not ELEVENLABS_API_KEY or not VOICE_ID:
        st.error("Missing API keys! Please configure your API keys in the sidebar.")
        st.stop()
    
    try:
        # Check required tools
        require_bin("ffmpeg")
        require_bin("ffprobe")
        
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Test OpenRouter API
        status_text.text("🔍 Testing API connections...")
        progress_bar.progress(10)
        ok, msg = test_openrouter(f"Write a short 2-3 sentence about {topic}.")
        if not ok:
            st.warning("OpenRouter test failed, but continuing anyway...")
        progress_bar.progress(20)
        
        # Step 2: Generate script
        status_text.text(f"✍️ Generating script for '{topic}'...")
        script = generate_script(topic)
        progress_bar.progress(40)
        
        # Step 3: Generate audio
        status_text.text("🎙️ Generating voiceover...")
        audio_path = generate_audio(script, "voiceover.mp3")
        progress_bar.progress(60)
        
        # Step 4: Select random video fragment
        status_text.text("🎬 Selecting video fragment...")
        fragment_path = select_random_fragment()
        progress_bar.progress(70)
        
        # Step 5: Add text overlay
        status_text.text("📝 Adding text overlay...")
        video_with_text = "video_with_text.mp4"
        add_text_overlay(fragment_path, script, video_with_text)
        progress_bar.progress(80)
        
        # Step 6: Merge audio and video
        status_text.text("🎥 Creating final video...")
        Path("outputs").mkdir(exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        final_video = f"outputs/video_{timestamp}.mp4"
        merge_audio_video(video_with_text, audio_path, final_video)
        progress_bar.progress(90)
        
        # Clean up temporary files
        try:
            os.remove("voiceover.mp3")
            os.remove("video_with_text.mp4")
        except OSError:
            pass
            
        progress_bar.progress(100)
        status_text.text("🎉 Video generation complete!")
        
        # ---- Results Section ----
        st.success("🎉 Your video is ready!")
        st.balloons()
        
        # Display results in columns
        result_col1, result_col2 = st.columns(2)
        
        with result_col1:
            st.subheader("🎥 Your Video")
            st.video(final_video)
            
            with open(final_video, "rb") as file:
                st.download_button(
                    label="📥 Download Video",
                    data=file,
                    file_name=os.path.basename(final_video),
                    mime="video/mp4",
                    use_container_width=True
                )
                
        with result_col2:
            st.subheader("📝 Generated Script")
            st.text_area("", value=script, height=200)
            
            st.subheader("#️⃣ Suggested Hashtags")
            hashtags = "#shorts #ai #trending #viral #funny #facts #storytime #gaming"
            st.text_area("", value=hashtags, height=100)
            
            st.subheader("📊 Video Details")
            st.info(f"Topic: {topic}")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)

# ---- Footer ----
st.markdown("---")
st.markdown("Made with ❤️ by [Aditi](https://github.com/Aditi4275)")