from gtts import gTTS
import os

def text_to_speech(text: str, output_path: str = "audio/output/response.mp3") -> str:
    """Convert text to speech using gTTS (free, no API key needed)"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_path)
    
    return output_path