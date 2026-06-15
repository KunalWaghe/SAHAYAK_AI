


---

# 🇮🇳 Sahayak (सहायक)

**AI-Powered Multilingual Government Scheme Discovery System**

Sahayak is an AI-powered, voice-first platform designed to bridge the gap between 4,700+ Indian government welfare schemes and the citizens who need them most. By removing language barriers and simplifying bureaucratic jargon, Sahayak empowers citizens to discover, understand, and apply for schemes in their own language.

---

## 🚀 The Problem

Millions of eligible Indian citizens miss out on government welfare due to:

* **Information Fragmentation:** Schemes are scattered across thousands of central and state portals.
* **Language Barriers:** Complex policy documents are often inaccessible to regional language speakers.
* **Navigation Friction:** Bureaucratic terminology creates a high barrier to entry for rural and semi-urban users.

## 💡 The Sahayak Solution

Sahayak transforms the discovery process through:

* **Voice-First Accessibility:** Talk to the app in Hindi, Marathi, Tamil, Telugu, Bengali, or English.
* **Semantic Intelligence:** Uses MuRIL and FAISS to understand *intent* rather than just keywords.
* **Simplified Eligibility:** Gemini 2.5 Flash distills complex legal documents into easy-to-understand, actionable points.
* **Geo-Filtering:** Automatically surfaces schemes relevant to the user's specific state/location.

---

## 🏗️ Technical Architecture

* **Frontend:** Streamlit with a custom Dark Mode interface.
* **Search Engine:** FAISS (Facebook AI Similarity Search) for sub-millisecond retrieval.
* **Embedding Model:** `google/muril-base-cased` for superior multilingual semantic understanding.
* **Generative Engine:** Google Gemini 2.5 Flash for natural language synthesis.
* **Audio Pipeline:** Google Text-to-Speech (gTTS) & native Gemini Audio transcription.

---

## 🛠️ Tech Stack

| Layer | Technology |
| --- | --- |
| **Frontend** | Streamlit |
| **LLM** | Gemini 2.5 Flash |
| **Embeddings** | MuRIL (Sentence Transformers) |
| **Vector DB** | FAISS |
| **Audio** | gTTS |
| **Language** | Python |

---

## 📂 Project Structure

```text
/
├── app.py              # Main Streamlit application
├── search.py           # FAISS search logic
├── llm.py              # Gemini response generation
├── stt.py              # Audio transcription engine
├── translator.py       # Language detection/translation
├── tts.py              # Text-to-speech module
├── requirements.txt    # Project dependencies
└── data/               # Contains schemes.json (4,718 schemes)

```

## 🚀 How to Run Locally

1. **Clone the repo:**
```bash
git clone https://github.com/yourusername/sahayak-ai.git

```


2. **Setup virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Set API Key:** Create a `.env` file and add: `GEMINI_API_KEY=your_key_here`
5. **Run the app:**
```bash
streamlit run app.py

```
Made By Kunal Waghe and Kashish Soni
knlwagheit@gmail.com
sonikashish173@gmail.com
---

## 🏆 Hackathon Details

* **Event:** OSC AI Build 1.0 Hackathon 2026
* **Impact Goal:** Empowering citizens through open-source AI and inclusive design.

---

*Built with ❤️ for social impact.*
