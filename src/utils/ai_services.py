import requests
import json
from gtts import gTTS

from src.config.settings import OPENROUTER_API_KEY, OPENROUTER_URL, MODEL_ID, GOOGLE_TTS_LANG, GOOGLE_TTS_TLD


def _make_request(url: str, headers: dict, json_data: dict = None, timeout: int = 30, method: str = "POST") -> requests.Response:
    """Helper function to make HTTP requests with error handling."""
    try:
        if method == "POST":
            resp = requests.post(url, headers=headers, json=json_data, timeout=timeout)
        else:
            resp = requests.get(url, headers=headers, timeout=timeout)
            
        resp.raise_for_status()
        return resp
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")


def generate_script(topic: str) -> str:
    """Generate a script using OpenRouter API."""
    if not OPENROUTER_API_KEY:
        raise EnvironmentError("OPENROUTER_API_KEY is not set.")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a creative scriptwriter. Write concise, punchy lines."},
            {"role": "user", "content": f"Write a tight 2-4 sentence voiceover script (max 60 words) for: {topic}"}
        ],
        "max_tokens": 220,
        "temperature": 0.8
    }
    
    try:
        resp = _make_request(OPENROUTER_URL, headers, data)
        payload = resp.json()
        content = payload["choices"][0]["message"]["content"].strip()
        return content
    except (KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Unexpected OpenRouter response format: {e}")


def generate_audio(script_text: str, output_audio: str = "voiceover.mp3") -> str:
    """Generate audio using Google TTS."""
    if not script_text or not script_text.strip():
        raise ValueError("Script text is empty. Cannot generate audio.")
    
    try:
        tts = gTTS(text=script_text, lang=GOOGLE_TTS_LANG, tld=GOOGLE_TTS_TLD)
        tts.save(output_audio)
        return output_audio
    except Exception as e:
        raise RuntimeError(f"Google TTS generation failed: {e}")



