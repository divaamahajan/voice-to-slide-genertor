from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
import logging
from typing import Optional

from app.services.audio_service import AudioService
from app.models.schemas import (
    AudioTranscriptionResponse,
    AudioTranslationResponse,
    AudioProcessingResponse,
    HealthResponse
)
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize audio service
audio_service = AudioService()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version
    )


@router.post("/record", response_model=AudioTranscriptionResponse)
async def record_audio():
    """Record audio from microphone."""
    try:
        filename, duration = audio_service.record_audio()
        transcription = audio_service.transcribe_audio(filename)
        
        return AudioTranscriptionResponse(
            transcription=transcription,
            duration=duration
        )
    except Exception as e:
        logger.error(f"Error recording audio: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to record audio: {str(e)}")


@router.post("/transcribe", response_model=AudioTranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe uploaded audio file."""
    try:
        # Debug logging
        logger.info(f"Transcribe request: filename={file.filename}, content_type={file.content_type}, size={file.size}")
        
        # Validate file type - be more lenient with content type checking
        if file.content_type and not file.content_type.startswith('audio/'):
            # Check file extension as fallback
            if not file.filename or not any(file.filename.lower().endswith(ext) for ext in ['.wav', '.mp3', '.m4a', '.webm', '.ogg', '.flac']):
                raise HTTPException(status_code=400, detail="File must be an audio file")
        elif not file.content_type:
            # If no content type, check file extension
            if not file.filename or not any(file.filename.lower().endswith(ext) for ext in ['.wav', '.mp3', '.m4a', '.webm', '.ogg', '.flac']):
                raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Ensure uploads directory exists
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # Save uploaded file to uploads directory
        filename = os.path.join(settings.upload_dir, f"temp_{file.filename}")
        with open(filename, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Transcribe audio
        transcription = audio_service.transcribe_audio(filename)
        
        # Clean up temp file
        os.remove(filename)
        
        return AudioTranscriptionResponse(transcription=transcription)
        
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to transcribe audio: {str(e)}")


@router.post("/translate", response_model=AudioTranslationResponse)
async def translate_audio(file: UploadFile = File(...)):
    """Translate uploaded audio file to English."""
    try:
        # Validate file type - be more lenient with content type checking
        if file.content_type and not file.content_type.startswith('audio/'):
            # Check file extension as fallback
            if not file.filename or not any(file.filename.lower().endswith(ext) for ext in ['.wav', '.mp3', '.m4a', '.webm', '.ogg', '.flac']):
                raise HTTPException(status_code=400, detail="File must be an audio file")
        elif not file.content_type:
            # If no content type, check file extension
            if not file.filename or not any(file.filename.lower().endswith(ext) for ext in ['.wav', '.mp3', '.m4a', '.webm', '.ogg', '.flac']):
                raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Ensure uploads directory exists
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # Save uploaded file to uploads directory
        filename = os.path.join(settings.upload_dir, f"temp_{file.filename}")
        with open(filename, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Translate audio
        translation = audio_service.translate_audio(filename)
        
        # Clean up temp file
        os.remove(filename)
        
        return AudioTranslationResponse(translation=translation)
        
    except Exception as e:
        logger.error(f"Error translating audio: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to translate audio: {str(e)}")


@router.post("/process", response_model=AudioProcessingResponse)
async def process_audio(file: UploadFile = File(...)):
    """Process audio file: transcribe and translate."""
    try:
        # Debug logging
        logger.info(f"Received file: filename={file.filename}, content_type={file.content_type}")
        
        # Simple validation - just check file extension
        if not file.filename or not any(file.filename.lower().endswith(ext) for ext in ['.wav', '.mp3', '.m4a', '.webm', '.ogg', '.flac']):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Ensure uploads directory exists
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # Save uploaded file to uploads directory
        filename = os.path.join(settings.upload_dir, f"temp_{file.filename}")
        with open(filename, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process audio
        transcription = audio_service.transcribe_audio(filename)
        translation = audio_service.translate_audio(filename)
        
        # Clean up temp file
        os.remove(filename)
        
        return AudioProcessingResponse(
            transcription=transcription,
            translation=translation,
            filename=file.filename
        )
        
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process audio: {str(e)}")


@router.post("/stream-transcribe", response_model=AudioTranscriptionResponse)
async def stream_transcribe_audio(file: UploadFile = File(...)):
    """Stream transcribe uploaded audio file."""
    try:
        # Validate file type - be more lenient with content type checking
        if file.content_type and not file.content_type.startswith('audio/'):
            # Check file extension as fallback
            if not file.filename or not any(file.filename.lower().endswith(ext) for ext in ['.wav', '.mp3', '.m4a', '.webm', '.ogg', '.flac']):
                raise HTTPException(status_code=400, detail="File must be an audio file")
        elif not file.content_type:
            # If no content type, check file extension
            if not file.filename or not any(file.filename.lower().endswith(ext) for ext in ['.wav', '.mp3', '.m4a', '.webm', '.ogg', '.flac']):
                raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Ensure uploads directory exists
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # Save uploaded file to uploads directory
        filename = os.path.join(settings.upload_dir, f"temp_{file.filename}")
        with open(filename, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Stream transcribe audio
        transcription = audio_service.stream_transcribe_audio(filename)
        
        # Clean up temp file
        os.remove(filename)
        
        return AudioTranscriptionResponse(transcription=transcription)
        
    except Exception as e:
        logger.error(f"Error stream transcribing audio: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to stream transcribe audio: {str(e)}")


@router.get("/play/{filename}")
async def play_audio(filename: str):
    """Play audio file."""
    try:
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        audio_service.play_audio(filename)
        return {"message": "Audio playback completed"}
        
    except Exception as e:
        logger.error(f"Error playing audio: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to play audio: {str(e)}")


@router.get("/download/{filename}")
async def download_audio(filename: str):
    """Download audio file."""
    try:
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        return FileResponse(
            path=filename,
            media_type="audio/wav",
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to download audio: {str(e)}")
