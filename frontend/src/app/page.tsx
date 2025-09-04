'use client';

import { useState, useRef } from 'react';
import { Mic, MicOff, Play, Pause, Upload, Download, Trash2, Volume2 } from 'lucide-react';
import AudioRecorder from '@/components/AudioRecorder';
import AudioPlayer from '@/components/AudioPlayer';
import TranscriptionDisplay from '@/components/TranscriptionDisplay';
import FileUpload from '@/components/FileUpload';
import { audioAPI } from '@/services/api';

// Helper function to create a proper file for API upload
const createAudioFile = (blob: Blob): File => {
  // Determine the appropriate file extension based on MIME type
  let extension = 'wav';
  if (blob.type.includes('webm')) {
    extension = 'webm';
  } else if (blob.type.includes('mp4')) {
    extension = 'm4a';
  } else if (blob.type.includes('ogg')) {
    extension = 'ogg';
  }
  
  return new File([blob], `audio.${extension}`, { type: blob.type });
};

export default function Home() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [transcription, setTranscription] = useState<string>('');
  const [translation, setTranslation] = useState<string>('');
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);
  const [isProcessingBoth, setIsProcessingBoth] = useState(false);
  const [error, setError] = useState<string>('');

  const handleRecordingComplete = (blob: Blob) => {
    console.log('Recording completed, blob received:', {
      size: blob.size,
      type: blob.type,
      constructor: blob.constructor.name
    });
    setAudioBlob(blob);
    setTranscription('');
    setTranslation('');
  };

  const handleFileUpload = (file: File) => {
    const blob = new Blob([file], { type: file.type });
    setAudioBlob(blob);
    setTranscription('');
    setTranslation('');
  };

  const handleTranscribe = async () => {
    if (!audioBlob) return;
    
    setIsTranscribing(true);
    setError('');
    
    try {
      const file = createAudioFile(audioBlob);
      const result = await audioAPI.transcribeAudio(file);
      setTranscription(result.transcription);
    } catch (error) {
      setError('Failed to transcribe audio. Please try again.');
      console.error('Transcription error:', error);
    } finally {
      setIsTranscribing(false);
    }
  };

  const handleTranslate = async () => {
    if (!audioBlob) return;
    
    setIsTranslating(true);
    setError('');
    
    try {
      const file = createAudioFile(audioBlob);
      const result = await audioAPI.translateAudio(file);
      setTranslation(result.translation);
    } catch (error) {
      setError('Failed to translate audio. Please try again.');
      console.error('Translation error:', error);
    } finally {
      setIsTranslating(false);
    }
  };

  const handleProcessBoth = async () => {
    if (!audioBlob) return;
    
    setIsProcessingBoth(true);
    setError('');
    
    try {
      const file = createAudioFile(audioBlob);
      const result = await audioAPI.processAudio(file);
      setTranscription(result.transcription);
      setTranslation(result.translation);
    } catch (error) {
      setError('Failed to process audio. Please try again.');
      console.error('Processing error:', error);
    } finally {
      setIsProcessingBoth(false);
    }
  };

  const handleTranscription = (text: string) => {
    setTranscription(text);
  };

  const handleTranslation = (text: string) => {
    setTranslation(text);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
  };

  const clearAll = () => {
    setAudioBlob(null);
    setTranscription('');
    setTranslation('');
    setError('');
    setIsTranscribing(false);
    setIsTranslating(false);
    setIsProcessingBoth(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🎙️ Voice-to-Slide Generator
          </h1>
          <p className="text-lg text-gray-600">
            Record, transcribe, and translate your voice into text
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Audio Controls */}
          <div className="space-y-6">
            {/* Audio Recorder */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <Mic className="mr-2" />
                Record Audio
              </h2>
              <AudioRecorder
                onRecordingComplete={handleRecordingComplete}
                onError={handleError}
                isProcessing={isTranscribing || isTranslating || isProcessingBoth}
              />
            </div>

            {/* File Upload */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <Upload className="mr-2" />
                Upload Audio File
              </h2>
              <FileUpload
                onFileUpload={handleFileUpload}
                onError={handleError}
                isProcessing={isTranscribing || isTranslating || isProcessingBoth}
              />
            </div>

            {/* Audio Player */}
            {audioBlob && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-semibold mb-4 flex items-center">
                  <Volume2 className="mr-2" />
                  Audio Player
                </h2>
                <AudioPlayer
                  audioBlob={audioBlob}
                  onError={handleError}
                />
              </div>
            )}
          </div>

          {/* Right Column - Processing & Results */}
          <div className="space-y-6">
            {/* Processing Controls */}
            {audioBlob && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-semibold mb-4">Process Audio</h2>
                <div className="space-y-4">
                  <button
                    onClick={handleTranscribe}
                    disabled={isTranscribing || isTranslating || isProcessingBoth}
                    className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                  >
                    {isTranscribing ? 'Transcribing...' : 'Transcribe Audio'}
                  </button>
                  <button
                    onClick={handleTranslate}
                    disabled={isTranscribing || isTranslating || isProcessingBoth}
                    className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                  >
                    {isTranslating ? 'Translating...' : 'Translate Audio'}
                  </button>
                  <button
                    onClick={handleProcessBoth}
                    disabled={isTranscribing || isTranslating || isProcessingBoth}
                    className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                  >
                    {isProcessingBoth ? 'Processing...' : 'Transcribe & Translate'}
                  </button>
                </div>
              </div>
            )}

            {/* Transcription Display */}
            <TranscriptionDisplay
              transcription={transcription}
              translation={translation}
              onClear={clearAll}
            />
          </div>
        </div>

        {/* Clear All Button */}
        {(audioBlob || transcription || translation) && (
          <div className="text-center mt-8">
            <button
              onClick={clearAll}
              className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-6 rounded-lg transition-colors flex items-center mx-auto"
            >
              <Trash2 className="mr-2" />
              Clear All
            </button>
          </div>
        )}
      </div>
    </div>
  );
}