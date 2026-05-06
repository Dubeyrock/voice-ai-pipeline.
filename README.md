
# 🎙️ Voice AI Pipeline (End-to-End)

An end-to-end **Voice AI system** that converts speech to intelligent spoken responses using a modular pipeline:

**Speech Input → Speech-to-Text → LLM → Text-to-Speech → Audio Output**

---

## 🚀 Overview

This project demonstrates a **real-world Voice AI pipeline** built from scratch without using any all-in-one voice assistant APIs.

It takes user speech (live/recorded), transcribes it, processes it using an LLM, and returns a spoken response.

---

## 🧠 Features

- 🎤 Speech Input (audio file / microphone)
- 📝 Speech-to-Text (STT)
- 🤖 LLM-based response generation
- 🔊 Text-to-Speech (TTS)
- 🔁 End-to-end audio response output
- 🧩 Modular pipeline design (easy to extend)

---

## ⚙️ Tech Stack

- Python
- SpeechRecognition / Whisper (STT)
- OpenAI / LLM API / GROQ API  (for response generation)
- pyttsx3 / gTTS (TTS)
- Streamlit (optional UI)

---

## 🏗️ Architecture (flowchart).


<img width="1360" height="640" alt="voice_ai_pipeline_architecture" src="https://github.com/user-attachments/assets/1df316d0-bdf9-49cd-b0b8-584e4188b1a5" />
