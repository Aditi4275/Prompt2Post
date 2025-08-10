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
