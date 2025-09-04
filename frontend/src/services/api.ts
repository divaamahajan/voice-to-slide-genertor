import axios from 'axios';

const API_BASE_URL = process.env.BACKEND_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for audio processing
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      statusText: error.response?.statusText,
      config: {
        url: error.config?.url,
        method: error.config?.method,
        baseURL: error.config?.baseURL
      }
    });
    return Promise.reject(error);
  }
);

export interface TranscriptionResponse {
  transcription: string;
  duration?: number;
  language?: string;
}

export interface TranslationResponse {
  translation: string;
  original_language?: string;
}

export interface ProcessingResponse {
  transcription: string;
  translation: string;
  duration?: number;
  filename: string;
}

export const audioAPI = {
  // Health check
  async healthCheck() {
    const response = await api.get('/api/v1/health');
    return response.data;
  },

  // Record audio (this would be handled by the backend's microphone recording)
  async recordAudio() {
    const response = await api.post('/api/v1/record');
    return response.data as TranscriptionResponse;
  },

  // Transcribe uploaded audio file
  async transcribeAudio(file: File) {
    console.log('Transcribing file:', {
      name: file.name,
      size: file.size,
      type: file.type,
      lastModified: file.lastModified
    });
    
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/v1/transcribe', formData);
    return response.data as TranscriptionResponse;
  },

  // Translate uploaded audio file
  async translateAudio(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/v1/translate', formData);
    return response.data as TranslationResponse;
  },

  // Process audio (transcribe + translate)
  async processAudio(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/v1/process', formData);
    return response.data as ProcessingResponse;
  },

  // Stream transcribe audio
  async streamTranscribeAudio(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/v1/stream-transcribe', formData);
    return response.data as TranscriptionResponse;
  },

  // Play audio file
  async playAudio(filename: string) {
    const response = await api.get(`/api/v1/play/${filename}`);
    return response.data;
  },

  // Download audio file
  async downloadAudio(filename: string) {
    const response = await api.get(`/api/v1/download/${filename}`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export default api;
