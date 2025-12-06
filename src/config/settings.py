import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# API URLs
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")

# Model ID
MODEL_ID = os.getenv("MODEL_ID", "openrouter/auto")

# TTS Settings
GOOGLE_TTS_LANG = "en"
GOOGLE_TTS_TLD = "co.uk"