import requests
import json
import os

from src.config.settings import OPENROUTER_API_KEY, ELEVENLABS_API_KEY, VOICE_ID, OPENROUTER_URL, ELEVENLABS_TTS_URL, MODEL_ID


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
    """Generate audio using ElevenLabs API."""
    if not ELEVENLABS_API_KEY:
        raise EnvironmentError("ELEVENLABS_API_KEY is not set.")
    if not VOICE_ID:
        raise EnvironmentError("ELEVENLABS_VOICE_ID is not set.")
    
    url = f"{ELEVENLABS_TTS_URL}/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": script_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    
    resp = _make_request(url, headers, data, timeout=60)
    
    with open(output_audio, "wb") as f:
        f.write(resp.content)
    return output_audio

