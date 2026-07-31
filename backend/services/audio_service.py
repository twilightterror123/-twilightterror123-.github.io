from ai.whisper_client import WhisperService
from ai.tts_client import TTSService

class AudioService:
    def __init__(self, whisper: WhisperService, tts: TTSService):
        self.whisper = whisper
        self.tts = tts

    async def transcribe(self, audio_bytes: bytes) -> str:
        return await self.whisper.transcribe(audio_bytes)

    async def synthesize(self, text: str) -> str:
        return await self.tts.synthesize(text)
