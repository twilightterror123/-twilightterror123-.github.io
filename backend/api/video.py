# video.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.auth import oauth2_scheme
router = APIRouter()
class VideoRequest(BaseModel):
    prompt: str
@router.post("/generate")
async def generate_video(req: VideoRequest, token: str = Depends(oauth2_scheme)):
    return {"message": "Video generation not yet implemented"}
