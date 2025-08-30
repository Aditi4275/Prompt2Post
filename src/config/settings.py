import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

# API Endpoints
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech"

# Model Configuration
MODEL_ID = "moonshotai/kimi-k2:free"

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30