# 🎙️ VoiceIQ — AI Voice Assistant Pipeline

> **AI Project.** |  
> A fully functional end-to-end Voice AI pipeline built without all-in-one voice assistant APIs.

---

## 📌 Project Overview

**VoiceIQ** is a minimal yet powerful Voice AI pipeline that takes live or recorded speech input, converts it to text, passes it through a large language model, and returns an intelligent spoken audio response — all in real time.

```
🎤 Speech Input  →  📝 Whisper STT  →  🧠 LLaMA 3.1 LLM  →  🔊 gTTS  →  🎧 Audio Output
```

---



## 🛠️ Tech Stack

| Component | Tool | Why |
|-----------|------|-----|
| **Speech-to-Text (ASR)** | Whisper Large V3 via Groq API | Fast, accurate, free tier |
| **LLM** | LLaMA 3.1 8B Instant via Groq API | Ultra-low latency, no OpenAI needed |
| **Text-to-Speech (TTS)** | gTTS (Google Text-to-Speech) | Free, no API key required |
| **UI** | Streamlit | Rapid prototyping, built-in mic recorder |
| **Memory** | Custom Sliding Window | Conversation context management |

> ✅ No OpenAI used. Groq API handles both STT and LLM.

---

## ✨ Features

- 🎤 **Live Browser Recording** — Record directly from mic using `st.audio_input` (no extra libraries)
- 📁 **File Upload Support** — WAV, MP3, M4A, OGG formats
- 🧠 **Conversation Memory** — Sliding window stores last 8 turns per session
- 💬 **Multiple Chat Sessions** — Create separate conversations for different topics
- 📌 **Topic Tracking** — AI knows what topics were discussed and builds deeper context
- ⚡ **Fast Pipeline** — Groq's inference is 10x faster than standard OpenAI endpoints
- 🔊 **Audio Response** — Every AI response is converted to speech automatically

---

## 🔧 Engineering Improvement: Conversation Memory

**Default behavior:** Every LLM call is stateless — the model has no memory of previous turns.

**What I changed:** Implemented a `ConversationMemory` class with a sliding window approach:

```python
class ConversationMemory:
    def __init__(self, max_turns: int = 8):
        self.history = []
        self.max_turns = max_turns
        self.topics = []  # tracks discussed topics

    def add_exchange(self, user_msg, assistant_msg):
        self.history.append({"role": "user", "content": user_msg})
        self.history.append({"role": "assistant", "content": assistant_msg})
        # Sliding window — prevents context overflow
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-(self.max_turns * 2):]
```

**Why this matters:**
- Without memory → AI treats every question as brand new
- With memory → AI builds on previous answers, goes deeper, connects related concepts
- Sliding window → prevents token limit overflow while keeping recent context

---

## 📁 Project Structure

```
voice-ai-pipeline/
├── app.py                  # Main Streamlit application
├── pipeline/
│   ├── __init__.py
│   ├── stt.py              # Speech-to-Text via Whisper (Groq)
│   ├── llm.py              # LLM response via LLaMA 3.1 (Groq)
│   ├── tts.py              # Text-to-Speech via gTTS
│   └── memory.py           # ConversationMemory + SessionManager
├── audio/
│   ├── input/              # Uploaded/recorded audio files
│   └── output/             # Generated TTS audio responses
├── .env                    # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Installation

### 1. Clone / Create Project
```bash
mkdir voice-ai-pipeline
cd voice-ai-pipeline
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` File
```bash
GROQ_API_KEY=your_groq_api_key_here
```
> Get your free API key at: https://console.groq.com

### 5. Run the App
```bash
streamlit run app.py
```

---

## 📦 requirements.txt

```
streamlit>=1.23.0
groq
gtts
python-dotenv
pydub
```

---

## 🎯 Pipeline Code Overview

### `pipeline/stt.py` — Speech to Text
```python
def transcribe_audio(audio_file_path: str) -> str:
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            response_format="text"
        )
    return transcription
```

### `pipeline/llm.py` — LLM Response
```python
def get_llm_response(user_text, conversation_history, topics_discussed=None):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Fast model for low latency
        messages=messages,
        max_tokens=250
    )
    return response.choices[0].message.content
```

### `pipeline/tts.py` — Text to Speech
```python
def text_to_speech(text: str, output_path: str) -> str:
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_path)
    return output_path
```

---

## 🧪 Test Inputs

| Test Type | Description | Expected Behavior |
|-----------|-------------|-------------------|
| **Clean Input** | Clear English speech, normal speed | High accuracy transcript, accurate AI response |
| **Challenging Input** | Fast speech / Hinglish / background noise | Tests robustness of Whisper ASR |

---

## ⚖️ Tradeoffs

| Decision | Chosen | Alternative | Tradeoff |
|----------|--------|-------------|----------|
| LLM Model | `llama-3.1-8b-instant` | `llama-3.3-70b` | Speed vs Quality |
| Memory | Sliding window (8 turns) | Full history | Context vs Token cost |
| TTS | gTTS (free) | ElevenLabs | Cost vs Voice quality |
| STT | Whisper Large V3 | Whisper Tiny | Accuracy vs Speed |

---

## 🐛 Known Issue & Fix

**Issue:** `llama3-8b-8192` model was decommissioned by Groq mid-development.

**Error:**
```
Error code: 400 - model llama3-8b-8192 has been decommissioned
```

**Fix:** Updated model string to `llama-3.1-8b-instant` in `pipeline/llm.py`

---

## 👤 Author

Built as part of the **AI Voice Engineer 60-Minute Build Challenge**

---

## 📄 License

MIT License — free to use and modify.

## 🏗️ Architecture (flowchart).
<img width="1536" height="1024" alt="archtecture_" src="https://github.com/user-attachments/assets/6b8ab733-9b9b-41e2-a935-44099a2c2faf" />

