import os

# API Keys - will fall back to environment variables if not set directly
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

# API URLs
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
ELEVENLABS_TTS_URL = os.getenv("ELEVENLABS_TTS_URL", "https://api.elevenlabs.io/v1/text-to-speech")

# Model ID
MODEL_ID = os.getenv("MODEL_ID", "openrouter/auto")