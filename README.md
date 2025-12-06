## 🎬 **Prompt2Post**

Create stunning short videos with AI-generated scripts and voiceovers in minutes! Prompt2Post offers both a Streamlit web app for creative exploration and a CLI for automation and batch processing. Perfect for content creators, educators, and marketers.


## ✨ Features

- 📝 **AI Script Generation** – Harness the **OpenRouter API** to create concise, engaging video scripts from prompts or trending topics.
- 🎙 **AI Voiceover Generation** – Convert scripts into natural-sounding speech using **ElevenLabs**.
- 🎥 **Automated Video Creation** – Merge visuals with AI voiceovers into a ready-to-share video file.
- 🖥 ** Ho to Use** - 
  - **Streamlit Web App (`app.py`)** – Interactive, beginner-friendly interface.
  
## 🛠️ **Getting Started**

### Prerequisites

- **Python 3.8+**
- **ffmpeg & ffprobe** (for video processing): [Download here](https://ffmpeg.org/download.html) and add to your PATH.

### 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Aditi4275/Prompt2Post.git 
    cd Prompt2Post
    ```
2.  **Install dependencies:**
    ```bash
    uv sync
    ```

### 🔑 API Keys Setup

This project requires API keys for OpenRouter and ElevenLabs.

1.  **Create a `.env` file:** In the root directory of the project, create a file named `.env`.
2.  **Add your API keys to `.env`:**
    *   Replace `"YOUR_OPENROUTER_API_KEY"` with your key from [OpenRouter](https://openrouter.ai/).

## 📦 Usage

### Streamlit Web App

To run the interactive web application:

```bash
uv run streamlit run app.py
```

- Select a trending topic or enter your own.
- Generate your video with a click!
