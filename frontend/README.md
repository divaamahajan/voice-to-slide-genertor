# Voice-to-Slide Generator Frontend

A modern Next.js frontend application for the Voice-to-Slide Generator API. This application provides an intuitive interface for recording, uploading, and processing audio files with real-time transcription and translation capabilities.

## Features

- 🎙️ **Audio Recording**: Record audio directly from your microphone
- 📁 **File Upload**: Upload audio files with drag-and-drop support
- 🎵 **Audio Player**: Built-in audio player with controls
- 📝 **Real-time Transcription**: Convert speech to text using OpenAI Whisper
- 🌐 **Translation**: Translate audio to English
- 📋 **Copy & Download**: Copy results to clipboard or download as text files
- 📱 **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety and better development experience
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client for API calls

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running on http://localhost:8000

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Configure environment**
   ```bash
   cp env.local.example .env.local
   # Edit .env.local if needed (default API URL is http://localhost:8000)
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Open in browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Usage

### Recording Audio
1. Click the microphone button to start recording
2. Speak into your microphone
3. Click the stop button to finish recording
4. Use the processing buttons to transcribe or translate

### Uploading Files
1. Drag and drop an audio file onto the upload area, or
2. Click the upload area to browse for files
3. Supported formats: MP3, WAV, M4A, and other audio formats
4. Maximum file size: 25MB

### Processing Audio
- **Transcribe**: Convert speech to text in the original language
- **Translate**: Convert speech to English text
- **Transcribe & Translate**: Do both operations in one go

### Results
- View transcription and translation results
- Copy text to clipboard
- Download results as text files
- Clear all data to start over

## API Integration

The frontend communicates with the FastAPI backend through the following endpoints:

- `POST /api/v1/transcribe` - Transcribe audio file
- `POST /api/v1/translate` - Translate audio file  
- `POST /api/v1/process` - Process audio (transcribe + translate)
- `POST /api/v1/stream-transcribe` - Stream transcribe audio
- `GET /api/v1/health` - Health check

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx          # Main page component
│   │   └── layout.tsx        # Root layout
│   ├── components/
│   │   ├── AudioRecorder.tsx # Audio recording component
│   │   ├── AudioPlayer.tsx   # Audio playback component
│   │   ├── FileUpload.tsx    # File upload component
│   │   └── TranscriptionDisplay.tsx # Results display
│   └── services/
│       └── api.ts            # API service layer
├── public/                   # Static assets
├── .env.local               # Environment variables
└── package.json             # Dependencies
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Environment Variables

- `BACKEND_URL` - Backend API URL (default: http://localhost:8000)

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License