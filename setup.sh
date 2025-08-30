#!/bin/bash
# Setup script for the Prompt2Post application

echo "Setting up Prompt2Post application..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found. Please run this script from the project directory."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create outputs directory if it doesn't exist
if [ ! -d "outputs" ]; then
    echo "Creating outputs directory..."
    mkdir outputs
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: ffmpeg is not installed. Please install it for video processing."
    echo "You can download it from https://ffmpeg.org/download.html"
else
    echo "ffmpeg is installed."
fi

if ! command -v ffprobe &> /dev/null; then
    echo "Warning: ffprobe is not installed. Please install it for video processing."
    echo "You can download it from https://ffmpeg.org/download.html"
else
    echo "ffprobe is installed."
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a .env file with your API keys:"
echo "   OPENROUTER_API_KEY=your_key_here"
echo "   ELEVENLABS_API_KEY=your_key_here"
echo "   ELEVENLABS_VOICE_ID=your_voice_id_here"
echo ""
echo "2. Run the application:"
echo "   ./start_app.sh"
echo ""