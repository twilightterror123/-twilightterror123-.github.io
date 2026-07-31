from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.auth import oauth2_scheme, validate_token
from services.image_service import ImageService
from main import app

router = APIRouter()

class ImageRequest(BaseModel):
    prompt: str

@router.post("/generate")
async def generate_image(req: ImageRequest, token: str = Depends(oauth2_scheme)):
    user = await validate_token(token)
    if not user:
        raise HTTPException(401, "Invalid token")
    image_service: ImageService = app.state.image_service
    image_url = await image_service.generate(req.prompt)
    return {"image": image_url}
