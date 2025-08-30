#!/bin/bash
# Startup script for the Prompt2Post application

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found. Please run this script from the project directory."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Check if required binaries are available
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed or not in PATH."
    exit 1
fi

if ! command -v ffprobe &> /dev/null; then
    echo "Error: ffprobe is not installed or not in PATH."
    exit 1
fi

# Check if required environment variables are set
if [ -z "$OPENROUTER_API_KEY" ] || [ -z "$ELEVENLABS_API_KEY" ] || [ -z "$ELEVENLABS_VOICE_ID" ]; then
    echo "Warning: API keys not set in environment variables."
    echo "Please set OPENROUTER_API_KEY, ELEVENLABS_API_KEY, and ELEVENLABS_VOICE_ID"
    echo "You can set them in your .env file or export them in your shell."
fi

# Run the Streamlit application
echo "Starting AI Video Maker application..."
streamlit run app.py