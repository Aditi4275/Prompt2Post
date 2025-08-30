import requests
import json
import os
from src.config.settings import OPENROUTER_API_KEY, ELEVENLABS_API_KEY, VOICE_ID, OPENROUTER_URL, ELEVENLABS_TTS_URL, MODEL_ID

def generate_script(topic: str) -> str:
    """Generate a script using OpenRouter API."""
    api_key = OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY is not set.")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
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
        resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
    except requests.RequestException as e:
        raise RuntimeError(f"OpenRouter request failed: {e}")
    
    if resp.status_code != 200:
        raise RuntimeError(f"OpenRouter API error: {resp.status_code} {resp.text}")

    try:
        payload = resp.json()
        content = payload["choices"][0]["message"]["content"].strip()
        return content
    except (KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Unexpected OpenRouter response format: {e}\nBody: {resp.text[:500]}")

def generate_hashtags(topic: str) -> str:
    """Generate relevant hashtags using OpenRouter API."""
    api_key = OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY is not set.")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a social media expert. Generate 5-8 relevant hashtags for a short video about the given topic. Return only the hashtags separated by spaces, starting with #."},
            {"role": "user", "content": f"Generate hashtags for a short video about: {topic}"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
    except requests.RequestException as e:
        raise RuntimeError(f"OpenRouter request failed: {e}")
    
    if resp.status_code != 200:
        raise RuntimeError(f"OpenRouter API error: {resp.status_code} {resp.text}")

    try:
        payload = resp.json()
        content = payload["choices"][0]["message"]["content"].strip()
        return content
    except (KeyError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Unexpected OpenRouter response format: {e}\nBody: {resp.text[:500]}")

def generate_audio(script_text: str, output_audio: str = "voiceover.mp3") -> str:
    """Generate audio using ElevenLabs API."""
    api_key = ELEVENLABS_API_KEY or os.getenv("ELEVENLABS_API_KEY")
    voice_id = VOICE_ID or os.getenv("ELEVENLABS_VOICE_ID")
    
    if not api_key:
        raise EnvironmentError("ELEVENLABS_API_KEY is not set.")
    if not voice_id:
        raise EnvironmentError("ELEVENLABS_VOICE_ID is not set.")
    
    url = f"{ELEVENLABS_TTS_URL}/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": script_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    
    try:
        resp = requests.post(url, json=data, headers=headers, timeout=60)
    except requests.RequestException as e:
        raise RuntimeError(f"ElevenLabs request failed: {e}")
    
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error: {resp.status_code} {resp.text}")

    with open(output_audio, "wb") as f:
        f.write(resp.content)
    return output_audio

def test_openrouter(prompt="Write a 2-sentence fun fact about space.") -> (bool, str):
    """Test the OpenRouter API key."""
    api_key = OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        return False, "OPENROUTER_API_KEY not set."
        
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a concise scriptwriter."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 120,
        "temperature": 0.7,
    }
    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
    except requests.RequestException as e:
        return False, f"Network error: {e}"
    if resp.status_code != 200:
        try:
            return False, json.dumps(resp.json(), indent=2)
        except Exception:
            return False, resp.text
    try:
        content = resp.json()["choices"][0]["message"]["content"].strip()
        return True, content
    except Exception as e:
        return False, f"Parse error: {e}\nBody: {resp.text[:800]}"