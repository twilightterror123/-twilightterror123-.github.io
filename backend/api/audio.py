from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from api.auth import oauth2_scheme, validate_token
from services.audio_service import AudioService
from main import app

router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    user = await validate_token(token)
    if not user:
        raise HTTPException(401, "Invalid token")
    audio_bytes = await file.read()
    audio_service: AudioService = app.state.audio_service
    text = await audio_service.transcribe(audio_bytes)
    return {"text": text}

class TTSRequest(BaseModel):
    text: str

@router.post("/synthesize")
async def synthesize_tts(req: TTSRequest, token: str = Depends(oauth2_scheme)):
    user = await validate_token(token)
    if not user:
        raise HTTPException(401, "Invalid token")
    audio_service: AudioService = app.state.audio_service
    audio_base64 = await audio_service.synthesize(req.text)
    return {"audio": audio_base64}
