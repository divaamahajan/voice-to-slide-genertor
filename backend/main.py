from openai import OpenAI
from dotenv import load_dotenv
import sounddevice as sd
from scipy.io.wavfile import write, read
import os
import time
import numpy as np
import logging

# Setup simple logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Suppress verbose HTTP logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def record_audio(filename="output.wav"):
    """
    Records audio by waiting for user to press Enter to start and stop recording.
    Uses standard parameters: 44100 Hz sample rate, 1 channel.
    """
    print("Press Enter to start recording...")
    input()  # Wait for Enter key
    
    print("Recording... Press Enter to stop.")
    
    # Start recording with standard parameters
    samplerate = 44100
    channels = 1  # Use mono instead of stereo for better compatibility
    
    # Record audio in chunks to allow for real-time stopping
    recording_data = []
    recording = False
    
    def audio_callback(indata, frames, time, status):
        if status:
            print(f"Audio status: {status}")
        if recording:
            recording_data.append(indata.copy())
    
    # Start recording stream
    stream = sd.InputStream(samplerate=samplerate, channels=channels, callback=audio_callback)
    stream.start()
    recording = True
    
    try:
        input()  # Wait for Enter key to stop
    except KeyboardInterrupt:
        pass
    
    # Stop recording
    recording = False
    stream.stop()
    stream.close()
    
    # Convert list of chunks to numpy array
    if recording_data:
        audio_data = np.concatenate(recording_data, axis=0)
        duration = len(audio_data) / samplerate
        # Convert to int16 for proper WAV format
        audio_data = (audio_data * 32767).astype(np.int16)
        # Save the audio file using scipy
        write(filename, samplerate, audio_data)
        print(f"Recording saved as {filename} ({duration:.1f}s)")
    else:
        print("No audio recorded.")

def play_audio(filename="output.wav"):
    print("Playing audio...")
    fs, data = read(filename)  # Note: scipy.io.wavfile.read returns (sample_rate, data)
    # Convert to float32 for sounddevice compatibility
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32767.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483647.0
    
    sd.play(data, fs)
    sd.wait()  # Wait until playback is finished
    print("Audio playback complete.")

def transcribe_audio(filename="output.wav"):
    audio_file = open(filename, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text",
        prompt="The following conversation is a test conversation.",
    )
    return transcription  # When response_format="text", transcription is already a string

def stream_transcribe_audio(filename="output.wav"):
    audio_file = open(filename, "rb")
    stream = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",  # Use gpt-4o-mini-transcribe for streaming
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
            # Only print if we haven't already printed this text
            if event.text not in full_transcription:
                print(event.text, end="", flush=True)
                full_transcription = event.text
    
    print()  # New line after streaming
    # return full_transcription

def translate_audio(filename="output.wav"):
    audio_file = open(filename, "rb")
    translation = client.audio.translations.create(
        model="whisper-1", 
        file=audio_file,
    )
    return translation.text

def main():
    print("🎙️ Voice-to-Slide Generator")
    print("=" * 30)
    
    record_audio()
    
    # Transcribe audio
    print("\n--- Streaming Transcription ---")
    stream_transcribe_audio()
    print("\n--- Transcription ---")
    print(f"Transcription: {transcribe_audio()}")
    
    # Translate audio
    print("\n--- Translation ---")
    translation = translate_audio()
    print(f"Translation: {translation}")
    
    play_audio()
    print("\n✅ Process completed!")

if __name__ == "__main__":
    main()
    
# client = OpenAI()
# audio_file = open("/path/to/file/speech.mp3", "rb")

# transcription = client.audio.transcriptions.create(
#     model="gpt-4o-transcribe", 
#     file=audio_file, 
#     response_format="text",
#   prompt="The following conversation is a test conversation.",
# #   stream=True

# )

# # for event in stream:
# #   print(event)

# print(transcription.text)
# # translated to English text
# translation = client.audio.translations.create(
#     model="whisper-1", 
#     file=audio_file,
# )

# print(translation.text)