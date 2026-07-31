import asyncio
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from api import auth, chat, files, images, video, audio, music
from core.database import init_db, get_db
from core.redis_client import redis_pool
from core.chroma_client import chroma_client
from core.config import settings

from services.chat_service import ChatService
from services.memory_service import MemoryService
from services.rag_service import RagService
from services.image_service import ImageService
from services.audio_service import AudioService
from services.video_service import VideoService
from services.music_service import MusicService

from ai.ollama_client import OllamaClient
from ai.stable_diffusion import StableDiffusionService
from ai.whisper_client import WhisperService
from ai.tts_client import TTSService

from utils.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await redis_pool.initialize()
    
    # KI-Clients initialisieren
    ollama = OllamaClient(settings.OLLAMA_BASE_URL)
    sd = StableDiffusionService(device="cpu")  # oder "cuda" falls GPU
    whisper = WhisperService(settings.WHISPER_MODEL)
    tts = TTSService(settings.TTS_MODEL)
    
    # Services
    rag = RagService(chroma_client, ollama)
    memory = MemoryService(redis_pool)
    chat_service = ChatService(ollama, rag, memory, redis_pool, get_db)
    image_service = ImageService(sd)
    audio_service = AudioService(whisper, tts)
    video_service = VideoService()
    music_service = MusicService()
    
    app.state.chat_service = chat_service
    app.state.image_service = image_service
    app.state.audio_service = audio_service
    app.state.video_service = video_service
    app.state.music_service = music_service
    
    logger.info("Twilight AI Backend gestartet")
    yield
    await redis_pool.close()
    logger.info("Twilight AI Backend beendet")

app = FastAPI(title="Twilight AI API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(images.router, prefix="/api/images", tags=["images"])
app.include_router(video.router, prefix="/api/video", tags=["video"])
app.include_router(audio.router, prefix="/api/audio", tags=["audio"])
app.include_router(music.router, prefix="/api/music", tags=["music"])

@app.websocket("/ws/chat/{conversation_id}")
async def websocket_chat(websocket: WebSocket, conversation_id: str, token: str):
    await websocket.accept()
    user = await auth.validate_token(token)
    if not user:
        await websocket.close(code=1008)
        return
    try:
        async for raw in websocket.iter_text():
            data = json.loads(raw)
            async for chunk in app.state.chat_service.process_message(
                user_id=user["id"],
                conversation_id=conversation_id,
                message=data["message"],
                model=data.get("model", "llama3.2"),
                use_rag=data.get("use_rag", True),
                use_memory=data.get("use_memory", True),
                stream=True
            ):
                await websocket.send_text(chunk)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_text(f"ERROR: {str(e)}")
    finally:
        await websocket.close()
