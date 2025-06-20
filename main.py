import os
from dotenv import load_dotenv
import base64

load_dotenv()

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
import chat

app = FastAPI()

origins = [
    "http://localhost:5173",  # Your local frontend's origin
    "https://realtime-front.vercel.app", # Your deployed frontend's origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

        return ChatResponse(audio_content=base64.b64encode(response_audio).decode("utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 