# music.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.auth import oauth2_scheme
router = APIRouter()
class MusicRequest(BaseModel):
    prompt: str
@router.post("/generate")
async def generate_music(req: MusicRequest, token: str = Depends(oauth2_scheme)):
    return {"message": "Music generation not yet implemented"}
