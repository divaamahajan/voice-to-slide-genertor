# 🎙️ Voice-to-Slide Generator

A full-stack application that converts voice recordings into text through transcription and translation using OpenAI's Whisper models. Features both a FastAPI backend and a modern Next.js frontend.

## ✨ Features

### Backend (FastAPI)
- 🎙️ **Audio Recording**: Record audio from microphone
- 📝 **Transcription**: Convert speech to text using OpenAI Whisper
- 🌐 **Translation**: Translate audio to English
- 🔄 **Streaming**: Real-time streaming transcription
- 📁 **File Management**: Upload and process audio files
- 🎵 **Audio Playback**: Play recorded audio files
- 📊 **API Documentation**: Interactive Swagger UI

### Frontend (Next.js)
- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS
- 🎙️ **Audio Recording**: Browser-based microphone recording
- 📁 **Drag & Drop**: Easy file upload with drag-and-drop
- 🎵 **Audio Player**: Built-in audio player with controls
- 📋 **Copy & Download**: Copy results or download as text files
- 📱 **Mobile Friendly**: Responsive design for all devices

## 🏗️ Architecture

```
voice-to-slide-generator/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── uploads/            # Audio files storage
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js Frontend
│   ├── src/
│   │   ├── app/            # Next.js app router
│   │   ├── components/     # React components
│   │   └── services/       # API client
│   └── package.json        # Node dependencies
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- OpenAI API key

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
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
   # Edit .env and add your OPENAI_API_KEY
   ```

5. **Start the backend server**
   ```bash
   python run.py
   # or
   uvicorn app.main:app --reload
   ```

   Backend will be available at: http://localhost:8000
   API Documentation: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the frontend server**
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000

## 📖 Usage

### Using the Web Interface

1. **Open the application** at http://localhost:3000
2. **Record audio** by clicking the microphone button
3. **Upload files** by dragging and dropping audio files
4. **Process audio** using the transcription/translation buttons
5. **View results** and copy or download them

### Using the CLI

```bash
cd backend
source myenv/bin/activate
python app/cli.py
```

### Using the API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Transcribe audio file
curl -X POST "http://localhost:8000/api/v1/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav"

# Translate audio file
curl -X POST "http://localhost:8000/api/v1/translate" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.wav"
```

## 🔧 Configuration

### Backend Configuration

Environment variables in `backend/.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=False
AUDIO_SAMPLE_RATE=44100
AUDIO_CHANNELS=1
UPLOAD_DIR=uploads
MAX_FILE_SIZE=26214400
```

### Frontend Configuration

Environment variables in `frontend/.env.local`:

```env
BACKEND_URL=http://localhost:8000
```

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/record` | Record audio from microphone |
| POST | `/api/v1/transcribe` | Transcribe uploaded audio |
| POST | `/api/v1/translate` | Translate uploaded audio |
| POST | `/api/v1/process` | Process audio (transcribe + translate) |
| POST | `/api/v1/stream-transcribe` | Stream transcribe audio |
| GET | `/api/v1/play/{filename}` | Play audio file |
| GET | `/api/v1/download/{filename}` | Download audio file |

## 🛠️ Development

### Backend Development

```bash
cd backend
source myenv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Deployment

### Backend Deployment

1. **Build the application**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

3. **Run with production server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Frontend Deployment

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Start production server**
   ```bash
   npm start
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for the Whisper models
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Next.js](https://nextjs.org/) for the frontend framework
- [Tailwind CSS](https://tailwindcss.com/) for styling