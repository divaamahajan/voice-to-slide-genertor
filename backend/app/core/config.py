from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    app_name: str = "Voice-to-Slide Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # OpenAI Settings
    openai_api_key: str
    openai_model_transcribe: str = "whisper-1"
    openai_model_stream: str = "gpt-4o-mini-transcribe"
    
    # Audio Settings
    audio_sample_rate: int = 44100
    audio_channels: int = 1
    audio_filename: str = "recording.wav"
    
    # File Settings
    upload_dir: str = "uploads"
    max_file_size: int = 25 * 1024 * 1024  # 25MB
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
