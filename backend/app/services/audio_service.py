import os
import logging
from typing import Optional, Tuple
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read
from openai import OpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)


class AudioService:
    """Service for audio recording, playback, and processing."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.sample_rate = settings.audio_sample_rate
        self.channels = settings.audio_channels
        
    def record_audio(self, filename: str = None) -> Tuple[str, float]:
        """
        Record audio from microphone.
        
        Args:
            filename: Output filename for the audio file
            
        Returns:
            Tuple of (filename, duration)
        """
        if filename is None:
            filename = settings.audio_filename
        
        # Ensure uploads directory exists
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # Use uploads directory for audio files
        if not os.path.dirname(filename):
            filename = os.path.join(settings.upload_dir, filename)
            
        logger.info(f"Starting audio recording: {filename}")
        
        # Record audio in chunks to allow for real-time stopping
        recording_data = []
        recording = False
        
        def audio_callback(indata, frames, time, status):
            if status:
                logger.warning(f"Audio status: {status}")
            if recording:
                recording_data.append(indata.copy())
        
        # Start recording stream
        stream = sd.InputStream(
            samplerate=self.sample_rate, 
            channels=self.channels, 
            callback=audio_callback
        )
        stream.start()
        recording = True
        
        try:
            input("Press Enter to stop recording...")
        except KeyboardInterrupt:
            pass
        
        # Stop recording
        recording = False
        stream.stop()
        stream.close()
        
        # Process recorded audio
        if recording_data:
            audio_data = np.concatenate(recording_data, axis=0)
            duration = len(audio_data) / self.sample_rate
            
            # Convert to int16 for proper WAV format
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Save the audio file
            write(filename, self.sample_rate, audio_data)
            logger.info(f"Audio saved: {filename} ({duration:.2f}s)")
            
            return filename, duration
        else:
            raise ValueError("No audio data recorded")
    
    def play_audio(self, filename: str) -> None:
        """
        Play audio file.
        
        Args:
            filename: Path to audio file
        """
        logger.info(f"Playing audio: {filename}")
        
        fs, data = read(filename)
        
        # Convert to float32 for sounddevice compatibility
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32767.0
        elif data.dtype == np.int32:
            data = data.astype(np.float32) / 2147483647.0
        
        sd.play(data, fs)
        sd.wait()
        
        logger.info("Audio playback completed")
    
    def transcribe_audio(self, filename: str) -> str:
        """
        Transcribe audio file to text.
        
        Args:
            filename: Path to audio file
            
        Returns:
            Transcribed text
        """
        logger.info(f"Transcribing audio: {filename}")
        
        with open(filename, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model=settings.openai_model_transcribe,
                file=audio_file,
                response_format="text",
                prompt="The following conversation is a test conversation.",
            )
        
        logger.info("Transcription completed")
        return transcription
    
    def translate_audio(self, filename: str) -> str:
        """
        Translate audio file to English.
        
        Args:
            filename: Path to audio file
            
        Returns:
            Translated text
        """
        logger.info(f"Translating audio: {filename}")
        
        with open(filename, "rb") as audio_file:
            translation = self.client.audio.translations.create(
                model=settings.openai_model_transcribe,
                file=audio_file,
            )
        
        logger.info("Translation completed")
        return translation.text
    
    def stream_transcribe_audio(self, filename: str) -> str:
        """
        Stream transcribe audio file.
        
        Args:
            filename: Path to audio file
            
        Returns:
            Transcribed text
        """
        logger.info(f"Starting streaming transcription: {filename}")
        
        with open(filename, "rb") as audio_file:
            stream = self.client.audio.transcriptions.create(
                model=settings.openai_model_stream,
                file=audio_file,
                response_format="text",
                prompt="The following conversation is a test conversation.",
                stream=True,
            )
        
        full_transcription = ""
        for event in stream:
            if hasattr(event, 'delta') and event.delta:
                print(event.delta, end="", flush=True)
                full_transcription += event.delta
            elif hasattr(event, 'text') and event.text:
                if event.text not in full_transcription:
                    print(event.text, end="", flush=True)
                    full_transcription = event.text
        
        print()  # New line after streaming
        logger.info("Streaming transcription completed")
        return full_transcription
