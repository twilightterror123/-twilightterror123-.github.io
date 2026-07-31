from TTS.api import TTS
import tempfile
import os
import base64

class TTSService:
    def __init__(self, model_name="tts_models/de/thorsten"):
        self.tts = TTS(model_name)

    async def synthesize(self, text: str) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            self.tts.tts_to_file(text=text, file_path=f.name)
            with open(f.name, "rb") as audio_file:
                audio_bytes = audio_file.read()
            os.unlink(f.name)
            return base64.b64encode(audio_bytes).decode()
