# utils/stt.py
import whisper
import tempfile
import os

_model = None

def _load():
    global _model
    if _model is None:
        print("⏳ Loading Whisper model...")
        _model = whisper.load_model("base")
        print("✅ Whisper ready")

def transcribe_audio(audio_bytes: bytes) -> dict:
    _load()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name
    try:
        result = _model.transcribe(tmp_path)
        return {
            "text":     result["text"].strip(),
            "language": result.get("language", "unknown")
        }
    except Exception as e:
        return {"text": "", "language": "unknown", "error": str(e)}
    finally:
        os.unlink(tmp_path)