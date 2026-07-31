from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    REDIS_URL: str
    CHROMA_URL: str
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    WHISPER_MODEL: str = "base"
    TTS_MODEL: str = "tts_models/de/thorsten"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"

settings = Settings()
