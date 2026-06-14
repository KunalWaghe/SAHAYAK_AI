# app.py — Sahayak Main Application
import streamlit as st
from utils.search import search_schemes
from utils.llm import ask_llm
from utils.tts import text_to_speech
from audio_recorder_streamlit import audio_recorder
from utils.stt import transcribe_audio

# ─── Greeting Detection ────────────────────────
GREETING_WORDS = [
    "hello", "hi", "hey", "namaste", "नमस्ते", "नमस्कार", 
    "thanks", "thank you", "धन्यवाद", "bye", "ok", "okay"
]

def is_greeting(text: str) -> bool:
    cleaned = text.lower().strip().strip("!.,?")
    return cleaned in GREETING_WORDS or len(cleaned.split()) <= 2 and any(g in cleaned for g in GREETING_WORDS)

# ─── Page Config ──────────────────────────────
st.set_page_config(
    page_title="Sahayak — सहायक",
    page_icon="",
    layout="centered"
)

# ─── Custom CSS ───────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f4f8fb; }
    .stChatMessage { border-radius: 12px; margin-bottom: 8px; }
    .scheme-card {
        background: white;
        border-left: 4px solid #FF6B35;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    .scheme-title { font-weight: bold; color: #1A3A5C; font-size: 15px; }
    .scheme-meta  { color: #5A7A94; font-size: 12px; margin-top: 4px; }
    .scheme-link  { color: #028090; font-size: 12px; }
    .header-bar {
        background: linear-gradient(90deg, #1A3A5C, #028090);
        color: white;
        padding: 16px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────
st.markdown("""
<div class="header-bar">
    <h2 style="margin:0; color:white;">🇮🇳 Sahayak — सहायक</h2>
    <p style="margin:4px 0 0 0; opacity:0.85; font-size:14px;">
        AI-powered Government Scheme Finder | अपनी भाषा में सरकारी योजनाएं खोजें
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Language Selector ────────────────────────
LANGUAGES = {
    "हिन्दी (Hindi)":   "hi",
    "मराठी (Marathi)":  "mr",
    "தமிழ் (Tamil)":    "ta",
    "తెలుగు (Telugu)":  "te",
    "বাংলা (Bengali)":  "bn",
    "English":           "en",
}

col1, col2 = st.columns([3, 1])
with col1:
    lang_label = st.selectbox(
        "🌐 Choose your language / भाषा चुनें",
        list(LANGUAGES.keys())
    )
with col2:
    st.metric("📚 Schemes", "4,718")

user_lang = LANGUAGES[lang_label]

# ─── Suggested Queries ────────────────────────
SUGGESTIONS = {
    "hi": ["किसानों के लिए योजना", "छात्रों के लिए छात्रवृत्ति", "महिलाओं के लिए योजना", "बुजुर्गों के लिए पेंशन"],
    "mr": ["शेतकऱ्यांसाठी योजना", "विद्यार्थ्यांसाठी शिष्यवृत्ती", "महिलांसाठी योजना", "वृद्धांसाठी पेंशन"],
    "ta": ["விவசாயிகளுக்கான திட்டம்", "மாணவர்களுக்கு உதவித்தொகை", "பெண்களுக்கான திட்டம்", "முதியோர் ஓய்வூதியம்"],
    "te": ["రైతులకు పథకాలు", "విద్యార్థులకు స్కాలర్షిప్", "మహిళలకు పథకాలు", "వృద్ధులకు పింఛను"],
    "bn": ["কৃষকদের জন্য প্রকল্প", "শিক্ষার্থীদের বৃত্তি", "মহিলাদের জন্য প্রকল্প", "বৃদ্ধদের পেনশন"],
    "en": ["Farmer schemes in Maharashtra", "Scholarship for students", "Pension for elderly women", "Startup funding schemes"],
}

st.markdown("**💡 Try asking:**")
suggestions = SUGGESTIONS.get(user_lang, SUGGESTIONS["en"])
cols = st.columns(len(suggestions))
for i, suggestion in enumerate(suggestions):
    if cols[i].button(suggestion, use_container_width=True):
        st.session_state["prefill"] = suggestion

# ─── Initialize Chat History ──────────────────
WELCOME = {
    "hi": "नमस्ते! मैं सहायक हूँ। आप मुझसे किसी भी सरकारी योजना के बारे में हिंदी में पूछ सकते हैं। आप किसान हैं, छात्र हैं, या कोई और? बताइए! 🙏",
    "mr": "नमस्कार! मी सहायक आहे। तुम्ही मला मराठीत कोणत्याही सरकारी योजनेबद्दल विचारू शकता। 🙏",
    "ta": "வணக்கம்! நான் சகாயக். தமிழில் எந்த அரசு திட்டத்தைப் பற்றியும் என்னிடம் கேளுங்கள். 🙏",
    "te": "నమస్కారం! నేను సహాయక్. తెలుగులో ఏదైనా ప్రభుత్వ పథకం గురించి నన్ను అడగండి. 🙏",
    "bn": "নমস্কার! আমি সহায়ক। বাংলায় যেকোনো সরকারি প্রকল্প সম্পর্কে আমাকে জিজ্ঞাসা করুন। 🙏",
    "en": "Hello! I'm Sahayak. Ask me about any government scheme — for farmers, students, women, elderly, or entrepreneurs. I'll find what you're eligible for! 🙏",
}

# Reset chat if language changed
if st.session_state.get("current_lang") != user_lang:
    st.session_state.current_lang = user_lang
    st.session_state.messages = [{
        "role":    "assistant",
        "content": WELCOME[user_lang],
        "schemes": [],
        "audio":   None
    }]

# First time init
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role":    "assistant",
        "content": WELCOME[user_lang],
        "schemes": [],
        "audio":   None
    }]

# ─── Display Chat History ─────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

        if msg.get("schemes"):
            for scheme in msg["schemes"][:3]:
                st.markdown(f"""
                <div class="scheme-card">
                    <div class="scheme-title">📋 {scheme['title']}</div>
                    <div class="scheme-meta">
                        🏛️ {scheme['ministry'] or 'State Scheme'} &nbsp;|&nbsp;
                        📍 {scheme['state']}
                    </div>
                    <div class="scheme-link">
                        🔗 <a href="{scheme['url']}" target="_blank">
                        View on MyScheme.gov.in</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if msg.get("audio"):
            st.audio(msg["audio"], format="audio/mp3")

# ─── Voice + Text Input Area ──────────────────
MIC_LABELS = {
    "hi": "🎙️ बोलकर पूछें",
    "mr": "🎙️ बोलून विचारा",
    "ta": "🎙️ பேசி கேளுங்கள்",
    "te": "🎙️ మాట్లాడి అడగండి",
    "bn": "🎙️ বলে জিজ্ঞাসা করুন",
    "en": "🎙️ Ask by voice",
}

LISTENING_LABELS = {
    "hi": "🎧 सुन रहे हैं...",
    "mr": "🎧 ऐकत आहे...",
    "ta": "🎧 கேட்கிறேன்...",
    "te": "🎧 వింటున్నాను...",
    "bn": "🎧 শুনছি...",
    "en": "🎧 Listening...",
}

col_mic, col_label = st.columns([1, 5])
with col_mic:
    audio_data = audio_recorder(
        text="",
        recording_color="#FF6B35",
        neutral_color="#028090",
        icon_size="2x",
        pause_threshold=2.0,
        sample_rate=16000,
    )
with col_label:
    st.caption(MIC_LABELS.get(user_lang, MIC_LABELS["en"]))

prefill = st.session_state.pop("prefill", "")
user_input = st.chat_input(
    "अपना सवाल यहाँ लिखें... / Type your question here...",
)

# Process voice input
if audio_data and audio_data != st.session_state.get("last_audio"):
    st.session_state["last_audio"] = audio_data
    with st.spinner(LISTENING_LABELS.get(user_lang, LISTENING_LABELS["en"])):
        transcription = transcribe_audio(audio_data)
        voice_text = transcription["text"]
        if voice_text.strip():
            user_input = voice_text
            st.info(f"🎙️ {voice_text}")

if prefill and not user_input:
    user_input = prefill

# ─── Process Input ────────────────────────────
if user_input:
    # Save user message to history
    st.session_state.messages.append({
        "role":    "user",
        "content": user_input,
        "schemes": [],
        "audio":   None
    })

    # Generate everything before rendering
    with st.spinner("🔍 Searching 4,718 schemes..."):
        schemes = search_schemes(user_input, top_k=5)

    with st.spinner("🤖 Generating answer in your language..."):
        final_response = ask_llm(user_input, schemes)

    with st.spinner("🔊 Generating voice response..."):
        audio_bytes = text_to_speech(final_response, user_lang)

    # Save assistant message to history
    st.session_state.messages.append({
        "role":    "assistant",
        "content": final_response,
        "schemes": schemes[:3],
        "audio":   audio_bytes if audio_bytes else None
    })

    # Rerun to render everything cleanly from history
    st.rerun()

SIDEBAR_LABELS = {
    "hi": {"about": "परिचय", "db": "डेटाबेस", "lang": "भाषाएं", "clear": "🗑️ चैट साफ करें"},
    "mr": {"about": "परिचय", "db": "डेटाबेस", "lang": "भाषा", "clear": "🗑️ चॅट साफ करा"},
    "ta": {"about": "பற்றி", "db": "தரவுத்தளம்", "lang": "மொழிகள்", "clear": "🗑️ அரட்டையை அழி"},
    "te": {"about": "గురించి", "db": "డేటాబేస్", "lang": "భాషలు", "clear": "🗑️ చాట్ క్లియర్"},
    "bn": {"about": "সম্পর্কে", "db": "ডেটাবেস", "lang": "ভাষা", "clear": "🗑️ চ্যাট মুছুন"},
    "en": {"about": "About", "db": "Database", "lang": "Languages", "clear": "🗑️ Clear Chat"},
}

with st.sidebar:
    labels = SIDEBAR_LABELS.get(user_lang, SIDEBAR_LABELS["en"])

    st.markdown("### 🇮🇳 Sahayak")
    st.markdown("*AI for Social Impact*")
    st.divider()

    st.markdown(f"**{labels['about']}**")
    st.caption("Sahayak helps Indian citizens discover government welfare schemes in their own language using AI.")

    st.divider()
    st.markdown(f"**📊 {labels['db']}**")
    st.caption("4,718 schemes from MyScheme.gov.in")
    st.caption("Central + All State schemes")

    st.divider()
    st.markdown(f"**🌐 {labels['lang']}**")
    st.caption("Hindi • Marathi • Tamil • Telugu • Bengali • English")

    st.divider()
    if st.button(labels["clear"], use_container_width=True):
        st.session_state.messages = [{
            "role":    "assistant",
            "content": WELCOME[user_lang],
            "schemes": [],
            "audio":   None
        }]
        st.rerun()

    st.divider()
    st.caption("Built for OSC AI Build 1.0 Hackathon 2026")