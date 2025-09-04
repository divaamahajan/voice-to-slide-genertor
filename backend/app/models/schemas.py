from pydantic import BaseModel
from typing import Optional


class AudioTranscriptionResponse(BaseModel):
    """Response model for audio transcription."""
    transcription: str
    duration: Optional[float] = None
    language: Optional[str] = None


class AudioTranslationResponse(BaseModel):
    """Response model for audio translation."""
    translation: str
    original_language: Optional[str] = None


class AudioProcessingResponse(BaseModel):
    """Response model for complete audio processing."""
    transcription: str
    translation: str
    duration: Optional[float] = None
    filename: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    app_name: str
    version: str
