import groq
import os
from dotenv import load_dotenv

load_dotenv()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

def transcribe_audio(audio_file_path: str) -> str:
    """Transcribe audio using Whisper via Groq (fast + free)"""
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file,
            response_format="text",
            language="en"  # Change to None for auto-detect (handles Hindi too!)
        )
    return transcription