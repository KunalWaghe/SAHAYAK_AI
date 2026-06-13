# utils/tts.py
from gtts import gTTS
import tempfile
import os

LANG_MAP = {
    "hi": "hi",   # Hindi
    "mr": "mr",   # Marathi
    "ta": "ta",   # Tamil
    "te": "te",   # Telugu
    "bn": "bn",   # Bengali
    "gu": "gu",   # Gujarati
    "kn": "kn",   # Kannada
    "ml": "ml",   # Malayalam
    "pa": "pa",   # Punjabi
    "en": "en",   # English
}

def text_to_speech(text: str, lang: str = "hi") -> bytes:
    gtts_lang = LANG_MAP.get(lang, "hi")
    try:
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tts.save(f.name)
            tmp_path = f.name
        with open(tmp_path, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return b""
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)