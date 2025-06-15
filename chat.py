import os
from openai import OpenAI
from io import BytesIO
from typing import Dict, List

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conversation_history: Dict[str, List[Dict[str, str]]] = {}

async def transcribe_audio(audio_content: bytes) -> str:
    """Transcribes audio content using OpenAI Whisper API."""
    audio_file = BytesIO(audio_content)
    audio_file.name = "audio.mpeg" # Whisper API expects a file-like object with a name
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

async def generate_chat_response(session_id: str, transcript: str) -> str:
    """Generates a chat response using OpenAI Chat API, maintaining context."""
    if session_id not in conversation_history:
        conversation_history[session_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    conversation_history[session_id].append({"role": "user", "content": transcript})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history[session_id],
    )

    ai_message = response.choices[0].message.content
    conversation_history[session_id].append({"role": "assistant", "content": ai_message})
    return ai_message

async def convert_text_to_speech(text: str) -> bytes:
    """Converts text to speech using OpenAI Text-to-Speech API."""
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=text)
    return response.content

async def process_audio_chat(session_id: str, audio_content: bytes) -> bytes:
    """Processes audio input to generate an audio response, maintaining chat context."""
    transcript = await transcribe_audio(audio_content)
    ai_response_text = await generate_chat_response(session_id, transcript)
    response_audio = await convert_text_to_speech(ai_response_text)
    return response_audio 