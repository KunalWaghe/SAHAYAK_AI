# utils/stt.py
import streamlit as st
import whisper
import tempfile
import os

@st.cache_resource
def _load_whisper():
    print("⏳ Loading Whisper model...")
    model = whisper.load_model("small")
    print("✅ Whisper ready")
    return model

def transcribe_audio(audio_bytes: bytes) -> dict:
    model = _load_whisper()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name
    try:
        # task="transcribe" ensures output stays in the SAME language as spoken
        # language=None lets Whisper auto-detect the spoken language
        result = model.transcribe(tmp_path, task="transcribe", language=None)
        return {
            "text":     result["text"].strip(),
            "language": result.get("language", "unknown")
        }
    except Exception as e:
        return {"text": "", "language": "unknown", "error": str(e)}
    finally:
        os.unlink(tmp_path)