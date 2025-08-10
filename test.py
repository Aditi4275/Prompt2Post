import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_ID = "moonshotai/kimi-k2:free"  # change to a valid model from your OpenRouter dashboard


def test_openrouter(prompt="Write a 2-sentence fun fact about space."):
    if not OPENROUTER_API_KEY:
        raise EnvironmentError("OPENROUTER_API_KEY environment variable is not set.")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
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
        print("❌ Network or request error:", e)
        return False

    print(f"\n🔹 HTTP Status: {resp.status_code}")

    # Try to decode JSON, or show raw body if it's not JSON
    try:
        payload = resp.json()
        print("\n📜 Full API response:\n", json.dumps(payload, indent=2))
    except json.JSONDecodeError:
        print("\n❌ Response is not valid JSON. Raw text:")
        print(resp.text)
        return False

    # Try extracting the model output if present
    try:
        content = payload["choices"][0]["message"]["content"].strip()
        print("\n✅ Model Output:\n", content)
        return True
    except (KeyError, IndexError) as e:
        print("\n⚠️ Could not find model output in response:", e)
        return False


if __name__ == "__main__":
    ok = test_openrouter(
        "Write a short 2–4 sentence voiceover script about a daring Minecraft parkour escape."
    )
    print("\n🏁 Result:", "PASS ✅" if ok else "FAIL ❌")
