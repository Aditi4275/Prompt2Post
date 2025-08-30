# AI Video Maker

This application generates short videos with AI-generated scripts and voiceovers. It uses OpenRouter for script generation and ElevenLabs for voiceover generation.

## Deployment Instructions

### For Streamlit Cloud

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and select your forked repository
4. Set the main file to `app.py`
5. Add the following secrets in the Streamlit Cloud settings:
   - `OPENROUTER_API_KEY`
   - `ELEVENLABS_API_KEY`
   - `ELEVENLABS_VOICE_ID`

### For Local Deployment

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your API keys in a `.env` file:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ELEVENLABS_VOICE_ID=your_voice_id
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Requirements

- Python 3.8+
- FFmpeg and FFprobe installed and available in PATH
- Internet connection
- API keys for OpenRouter and ElevenLabs

## Usage

1. Select a trending topic or enter a custom topic
2. Click "Generate Video"
3. Wait for the AI to create your video
4. Download and share your video!