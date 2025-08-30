<<<<<<< HEAD
# Prompt2Post

This project provides tools to create short videos with AI-generated scripts and voiceovers. It features both a Streamlit web application for an interactive user interface and a command-line interface (CLI) for automated or batch processing. Additionally, a utility script is included for splitting video files.

## Features

*   **AI Script Generation:** Utilizes OpenRouter API to generate concise video scripts based on user prompts or selected topics.
*   **AI Voiceover Generation:** Integrates with ElevenLabs API to convert generated scripts into natural-sounding voiceovers.
*   **Video Creation:** Combines a visual component (random video clips) with the AI-generated voiceover and text overlay to produce a final video file.
*   **Multiple Interfaces:**
    *   **Streamlit Web App (`app.py`):** An interactive graphical interface for easy use.
    *   **Command-Line Interface (`cli.py`):** A text-based interface for more control and scripting.
    *   **Enhanced Video Maker (`video_maker.py`):** A simplified script that randomly selects video clips and adds text overlays.
*   **Video Splitting Utility (`split.py`):** A standalone script to divide large video files into smaller fragments.


## Getting Started

### Prerequisites

Before running the application, ensure you have the following installed:

*   **Python 3.8+**
*   **`ffmpeg` and `ffprobe`:** These are essential for video processing. You can download them from [ffmpeg.org](https://ffmpeg.org/download.html) and ensure they are added to your system's PATH.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd tr
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### API Keys Setup

This project requires API keys for OpenRouter and ElevenLabs.

1.  **Create a `.env` file:** In the root directory of the project (`tr/`), create a file named `.env`.
2.  **Add your API keys to `.env`:**
    ```
    OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY"
    ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY"
    ELEVENLABS_VOICE_ID="YOUR_ELEVENLABS_VOICE_ID"
    ```
    *   Replace `"YOUR_OPENROUTER_API_KEY"` with your key from [OpenRouter](https://openrouter.ai/).
    *   Replace `"YOUR_ELEVENLABS_API_KEY"` with your key from [ElevenLabs](https://elevenlabs.io/).
    *   Replace `"YOUR_ELEVENLABS_VOICE_ID"` with the ID of the voice you wish to use from ElevenLabs.

## Usage

### Streamlit Web App

To run the interactive web application:

```bash
streamlit run app.py
```

Or use the provided startup script:

```bash
./start_app.sh
```

This will open the application in your web browser. You can select a trending topic or enter a custom topic, then generate a video.

### Enhanced Video Maker (New)

To use the enhanced video maker that randomly selects video clips and adds text overlays:

```bash
python video_maker.py
```

Or use the provided shell script:

```bash
./run_video_maker.sh
```

The script will prompt you for a topic, then generate a script, select a random video clip, add a voiceover and text overlay, and create the final video.

### Command-Line Interface (CLI) Tool

To use the CLI version of the video maker:

```bash
python cli.py
```
The script will guide you through selecting a video, providing a voiceover prompt, and generating the final video.

### Video Splitting Utility

To split a video file into fragments:

```bash
python split.py
```
**Note:** You may need to modify `split.py` to specify your `input.mp4` and desired `output_dir` and `fragment_duration`.

## Deployment

For deployment instructions, see `README_STREAMLIT.md` which contains specific guidance for deploying to Streamlit Cloud.

## Future Enhancements

*   Integrate a real-time trending topics API (e.g., Google Trends API via SerpApi) into `app.py` to replace the hardcoded placeholders.
*   Allow users to upload their own video footage instead of using a black screen.
*   Add more advanced video editing features.
*   Improve the text overlay formatting and positioning.
*   Add support for multiple languages in the voiceover.
*   Implement a web API for the video maker functionality.
=======
# 🎬 Prompt2Post

Create short, AI-powered videos in minutes.

**Prompt2Post** lets you turn ideas into videos — with AI-generated scripts, realistic voiceovers, and automated video creation.  
Whether you prefer a beautiful Streamlit web interface or a fast command-line tool, Prompt2Post has you covered.

---

## ✨ Features

- 📝 **AI Script Generation** – Harness the **OpenRouter API** to create concise, engaging video scripts from prompts or trending topics.
- 🎙 **AI Voiceover Generation** – Convert scripts into natural-sounding speech using **ElevenLabs**.
- 🎥 **Automated Video Creation** – Merge visuals with AI voiceovers into a ready-to-share video file.
- 🖥 **Two Ways to Use**:
  - **Streamlit Web App (`app.py`)** – Interactive, beginner-friendly interface.
  - **Command-Line Interface (`cli.py`)** – Perfect for power users & batch processing.

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aditi4275/prompt2post.git
   cd prompt2post
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
    ```
3. **Set environment variables**
   ```bash
    OPENROUTER_API_KEY=your_openrouter_api_key
    ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ```
## 📦 Usage
1️⃣ Run the Streamlit App
  ```bash
    streamlit run app.py
  ```
2️⃣ Run from Command Line
  ```bash
    python cli.py --prompt "Your video idea here"
   ```

💡 Tip: Use the CLI for automation & batch processing, and the Streamlit app for experimentation & creativity!
>>>>>>> 70833c3f99629a2555cc20a8cbf1eba986d42b76
