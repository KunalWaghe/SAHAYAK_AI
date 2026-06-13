# utils/tts.py
from gtts import gTTS
import tempfile
import os
import re

LANG_MAP = {
    "hi": "hi",
    "mr": "mr",
    "ta": "ta",
    "te": "te",
    "bn": "bn",
    "gu": "gu",
    "kn": "kn",
    "ml": "ml",
    "pa": "pa",
    "en": "en",
}

def clean_for_speech(text: str) -> str:
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\*(.*?)\*', r'\1', text)        # *italic*
    text = re.sub(r'#{1,6}\s*', '', text)            # ## headers
    text = re.sub(r'`(.*?)`', r'\1', text)           # `code`
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # [links](url)

    # Remove URLs completely
    text = re.sub(r'https?://\S+', '', text)

    # Remove bullet points and list markers
    text = re.sub(r'^\s*[-•*]\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)

    # Remove special characters that get read out loud
    text = re.sub(r'[_~|<>{}[\]\\]', '', text)

    # Clean up extra whitespace and blank lines
    text = re.sub(r'\n{2,}', '. ', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)

    return text.strip()

def text_to_speech(text: str, lang: str = "hi") -> bytes:
    gtts_lang = LANG_MAP.get(lang, "hi")
    clean_text = clean_for_speech(text)

    if not clean_text:
        return b""

    try:
        tts = gTTS(text=clean_text, lang=gtts_lang, slow=False)
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