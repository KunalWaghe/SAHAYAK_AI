# utils/translator.py
# Uses Helsinki-NLP opus-mt models — no login, no gating, works immediately

from transformers import MarianMTModel, MarianTokenizer

LANG_MODELS = {
    "hi": "Helsinki-NLP/opus-mt-en-hi",
    "mr": "Helsinki-NLP/opus-mt-en-mr",
    "ta": "Helsinki-NLP/opus-mt-en-ta",
    "te": "Helsinki-NLP/opus-mt-en-te",
    "bn": "Helsinki-NLP/opus-mt-en-bn",
}

REVERSE_MODELS = {
    "hi": "Helsinki-NLP/opus-mt-hi-en",
    "mr": "Helsinki-NLP/opus-mt-mr-en",
    "ta": "Helsinki-NLP/opus-mt-ta-en",
    "te": "Helsinki-NLP/opus-mt-te-en",
    "bn": "Helsinki-NLP/opus-mt-bn-en",
}

_cache = {}

def _get_model(model_name: str):
    if model_name not in _cache:
        print(f"⏳ Loading: {model_name}")
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model     = MarianMTModel.from_pretrained(model_name)
        _cache[model_name] = (tokenizer, model)
        print(f"✅ Ready: {model_name}")
    return _cache[model_name]

def _translate(text: str, model_name: str) -> str:
    tokenizer, model = _get_model(model_name)
    inputs  = tokenizer([text], return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def translate_to_english(text: str, src_lang: str) -> str:
    if src_lang == "en" or not text.strip():
        return text
    model_name = REVERSE_MODELS.get(src_lang)
    if not model_name:
        return text
    try:
        return _translate(text, model_name)
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return text

def translate_to_regional(text: str, tgt_lang: str) -> str:
    if tgt_lang == "en" or not text.strip():
        return text
    model_name = LANG_MODELS.get(tgt_lang)
    if not model_name:
        return text
    try:
        return _translate(text, model_name)
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return text