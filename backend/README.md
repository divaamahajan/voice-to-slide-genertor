# Voice-to-Slide Generator API

A FastAPI-based application that can record, transcribe, and translate audio files using OpenAI's Whisper models.

## Features

- 🎙️ **Audio Recording**: Record audio from microphone
- 📝 **Transcription**: Convert speech to text using OpenAI Whisper
- 🌐 **Translation**: Translate audio to English
- 🔄 **Streaming**: Real-time streaming transcription
- 📁 **File Upload**: Upload and process audio files
- 🎵 **Playback**: Play recorded audio files
- 📊 **API Documentation**: Interactive Swagger UI

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── cli.py               # Command line interface
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API routes
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   └── services/
│       ├── __init__.py
│       └── audio_service.py # Audio processing logic
├── requirements.txt
├── env.example
└── run.py
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd voice-to-slide-generator/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your OpenAI API key
   ```

## Usage

### API Server

Start the FastAPI server:
```bash
python run.py
# or
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

### Command Line Interface

Run the original CLI version:
```bash
python app/cli.py
```

## API Endpoints

### Health Check
- `GET /api/v1/health` - Check API health

### Audio Processing
- `POST /api/v1/record` - Record audio from microphone
- `POST /api/v1/transcribe` - Transcribe uploaded audio file
- `POST /api/v1/translate` - Translate uploaded audio file
- `POST /api/v1/process` - Process audio (transcribe + translate)
- `POST /api/v1/stream-transcribe` - Stream transcribe audio file

### File Operations
- `GET /api/v1/play/{filename}` - Play audio file
- `GET /api/v1/download/{filename}` - Download audio file

## Configuration

Environment variables can be set in `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
DEBUG=False
AUDIO_SAMPLE_RATE=44100
AUDIO_CHANNELS=1
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

## Dependencies

- **FastAPI**: Web framework
- **OpenAI**: AI transcription and translation
- **SoundDevice**: Audio recording and playback
- **SciPy**: Audio file processing
- **NumPy**: Numerical operations
- **Pydantic**: Data validation

## License

MIT License