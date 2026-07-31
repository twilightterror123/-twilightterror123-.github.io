from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from api.auth import oauth2_scheme, validate_token
from services.rag_service import RagService
from core.chroma_client import chroma_client
from ai.ollama_client import OllamaClient
from core.config import settings
import PyPDF2

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme)
):
    user = await validate_token(token)
    if not user:
        raise HTTPException(401, "Invalid token")
    
    # Temporär speichern
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Text extrahieren (nur PDF/TXT)
    text = ""
    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()
    elif file.filename.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        # Für Bilder/Audio nur Metadaten speichern
        text = ""
    
    if text:
        ollama = OllamaClient(settings.OLLAMA_BASE_URL)
        rag = RagService(chroma_client, ollama)
        await rag.add_document(user["id"], text, {"filename": file.filename})
    
    return JSONResponse({"message": "File uploaded", "filename": file.filename})
