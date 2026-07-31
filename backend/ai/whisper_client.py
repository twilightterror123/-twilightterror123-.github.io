import whisper
import tempfile
import os

class WhisperService:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    async def transcribe(self, audio_bytes: bytes) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio_bytes)
            f.flush()
            result = self.model.transcribe(f.name)
            os.unlink(f.name)
            return result["text"]
