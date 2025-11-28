import os
from typing import Optional

from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("[gemini_client] ❌ No API key found in .env (GOOGLE_API_KEY or GEMINI_API_KEY).")
else:
    genai.configure(api_key=API_KEY)
    print("[gemini_client] ✅ API key loaded. Gemini client configured.")

GEMINI_MODEL_NAME: Optional[str] = None


def _pick_default_model() -> Optional[str]:
    """
    Ask the API which models exist and pick one that supports generateContent.
    This avoids hardcoding 'gemini-1.5-flash' / 'gemini-pro' and getting 404s.
    """
    global GEMINI_MODEL_NAME

    if not API_KEY:
        return None

    try:
        models = genai.list_models()
        # Look for any text model that supports generateContent
        for m in models:
            # Most models have attributes: name, supported_generation_methods
            methods = getattr(m, "supported_generation_methods", [])
            if "generateContent" in methods:
                GEMINI_MODEL_NAME = m.name  # e.g. 'models/gemini-1.5-flash'
                print(f"[gemini_client] ✅ Using model: {GEMINI_MODEL_NAME}")
                return GEMINI_MODEL_NAME

        print("[gemini_client] ⚠️ No model with generateContent found.")
        return None
    except Exception as e:
        print("[gemini_client] ❌ Error listing models:", e)
        return None


def enhance_message(base_text: str, tone_hint: Optional[str] = None) -> str:
    """
    Uses Gemini to rewrite a reply. If anything fails, returns the original text
    with '[fallback]' prefix so we can see when AI is not used.
    """
    if not API_KEY:
        return base_text  # no key, no enhancement

    global GEMINI_MODEL_NAME
    if GEMINI_MODEL_NAME is None:
        GEMINI_MODEL_NAME = _pick_default_model()

    if not GEMINI_MODEL_NAME:
        return "[fallback] " + base_text

    try:
        prompt = (
            "You are a friendly, clear customer service assistant for an art & craft store. "
            "Rewrite the following reply to sound natural, empathetic, and easy to understand, "
            "without changing the facts. Keep it short and conversational.\n\n"
        )
        if tone_hint:
            prompt += f"Tone hint: {tone_hint}\n\n"

        prompt += f"Original reply:\n{base_text}\n\nRewritten reply:"

        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        response = model.generate_content(prompt)

        if response and getattr(response, "text", None):
            return response.text.strip()

        print("[gemini_client] ⚠️ Empty response from Gemini, using fallback.")
        return "[fallback] " + base_text

    except Exception as e:
        print("[gemini_client] ❌ Error calling Gemini:", e)
        return  base_text


