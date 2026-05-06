import groq
import os
from dotenv import load_dotenv

load_dotenv()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an intelligent voice assistant with memory of the ongoing conversation.

Your behavior:
- You REMEMBER everything discussed in this session
- If the user asks about a topic discussed before, BUILD on that explanation — go deeper, add examples, connect concepts
- Keep responses CONCISE (3-4 sentences max) since they will be spoken aloud
- If a topic was explained before, DO NOT repeat basics — instead add new insight
- Use simple, clear language suitable for text-to-speech
- If the user says "explain more", "tell me more", or "aur batao" — expand on the LAST topic discussed
- Connect related topics when relevant (e.g., if AI was discussed and user asks about ML, link them)

Response style:
- Speak naturally, as if in a conversation
- Avoid bullet points or markdown — use flowing sentences
- End with a subtle invitation to ask more if topic is complex
"""

def get_llm_response(user_text: str, conversation_history: list, topics_discussed: list = None) -> str:
    """
    Get LLM response with full conversation context + topic awareness.
    
    Args:
        user_text: Current user input (transcribed speech)
        conversation_history: Full history of this session
        topics_discussed: List of topics covered so far in this session
    """

    # Build enriched system message
    system_content = SYSTEM_PROMPT

    if topics_discussed and len(topics_discussed) > 0:
        topics_str = ", ".join(topics_discussed[-5:])  # Last 5 topics
        system_content += f"\n\nTopics already covered in this session: {topics_str}"
        system_content += "\nBuild upon these when relevant instead of starting fresh."

    messages = [
        {"role": "system", "content": system_content}
    ] + conversation_history + [
        {"role": "user", "content": user_text}
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=250,
        temperature=0.7
    )

    return response.choices[0].message.content