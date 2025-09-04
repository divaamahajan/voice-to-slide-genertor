"""
Command line interface for the voice-to-slide generator.
This provides the original CLI functionality.
"""
import logging
import sys
import os

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.audio_service import AudioService
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Suppress verbose HTTP logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)


def main():
    """Main CLI function."""
    print("🎙️ Voice-to-Slide Generator")
    print("=" * 30)
    
    audio_service = AudioService()
    
    # Record audio
    filename, duration = audio_service.record_audio()
    
    # Transcribe audio
    print("\n--- Streaming Transcription ---")
    audio_service.stream_transcribe_audio(filename)

    print("\n--- Transcription ---")
    print(f"Transcription: {audio_service.transcribe_audio(filename)}")
    
    # Translate audio
    print("\n--- Translation ---")
    translation = audio_service.translate_audio(filename)
    print(f"Translation: {translation}")
    
    # Play audio
    audio_service.play_audio(filename)
    print("\n✅ Process completed!")


if __name__ == "__main__":
    main()
