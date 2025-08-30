import streamlit as st
import os

def render_header():
    """Render the app header."""
    st.set_page_config(
        page_title="Viral Video Maker",
        page_icon="🎬",
        layout="centered",
        initial_sidebar_state="auto",
    )
    
    st.title("🎬 AI Viral Video Maker")
    st.markdown("Turn trending topics into engaging videos with one click.")

def get_trending_topics():
    """Get list of trending topics."""
    return [
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

def render_topic_selection():
    """Render the topic selection component."""
    trending_options = get_trending_topics()
    selected_trend = st.selectbox("Choose a trending topic:", trending_options)
    return selected_trend

def render_custom_topic():
    """Render the custom topic input."""
    st.subheader("Or create your own topic")
    custom_topic = st.text_input("Enter your own topic:")
    return custom_topic

def render_generate_button():
    """Render the generate button."""
    return st.button("🚀 Generate Video")

def render_results(video_path, script):
    """Render the results section."""
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
            st.subheader("# Hashtags (suggested)")
            st.text_area("", value="#shorts #gaming #minecraft #ai", height=60)