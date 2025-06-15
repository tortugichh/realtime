import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import chat

app = FastAPI()

class ChatResponse(BaseModel):
    audio_content: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(audio_file: UploadFile = File(...)):
    try:
        audio_content = await audio_file.read()
        session_id = "default_session"  # In a real app, generate/get from client

        response_audio = await chat.process_audio_chat(
            session_id=session_id,
            audio_content=audio_content,
        )

        return ChatResponse(audio_content=response_audio.decode("latin-1"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 