from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.auth import oauth2_scheme, validate_token

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    model: str = "llama3.2"
    use_rag: bool = True
    use_memory: bool = True

@router.post("/message")
async def send_message(req: ChatRequest, token: str = Depends(oauth2_scheme)):
    user = await validate_token(token)
    if not user:
        raise HTTPException(401, "Invalid token")
    # Hier könnte man die ChatService synchron aufrufen (non‑streaming)
    return {"message": "OK (use WebSocket for streaming)"}
