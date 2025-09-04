'use client';

import { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Square } from 'lucide-react';

interface AudioRecorderProps {
  onRecordingComplete: (blob: Blob) => void;
  onError: (error: string) => void;
  isProcessing: boolean;
}

export default function AudioRecorder({ onRecordingComplete, onError, isProcessing }: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (isRecording) {
      intervalRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRecording]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const startRecording = async () => {
    try {
      // Clear any previous chunks
      audioChunksRef.current = [];
      
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Try to use webm format first, fallback to default
      let mimeType = 'audio/webm';
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        mimeType = 'audio/webm;codecs=opus';
      }
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        mimeType = 'audio/mp4';
      }
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        mimeType = ''; // Use default
      }
      
      const recorder = new MediaRecorder(stream, { mimeType });
      
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
          console.log('Received audio chunk:', event.data.size, 'bytes, total chunks:', audioChunksRef.current.length);
        }
      };

      recorder.onstop = () => {
        // Create blob with the recorded mime type
        if (audioChunksRef.current.length > 0) {
          const audioBlob = new Blob(audioChunksRef.current, { type: mimeType || 'audio/webm' });
          console.log('Created audio blob:', {
            size: audioBlob.size,
            type: audioBlob.type,
            chunks: audioChunksRef.current.length
          });
          onRecordingComplete(audioBlob);
        } else {
          console.error('No audio chunks recorded');
          onError('No audio was recorded. Please try again.');
        }
        audioChunksRef.current = [];
        stream.getTracks().forEach(track => track.stop());
      };

      recorder.start(1000); // Request data every second
      setMediaRecorder(recorder);
      setIsRecording(true);
      setRecordingTime(0);
      console.log('Started recording with mimeType:', mimeType);
    } catch (error) {
      onError('Failed to access microphone. Please check permissions.');
      console.error('Error starting recording:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="text-center">
        <div className="text-3xl font-mono text-gray-600 mb-2">
          {formatTime(recordingTime)}
        </div>
        <div className="text-sm text-gray-500">
          {isRecording ? 'Recording...' : 'Ready to record'}
        </div>
      </div>

      <div className="flex justify-center space-x-4">
        {!isRecording ? (
          <button
            onClick={startRecording}
            disabled={isProcessing}
            className="bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white p-4 rounded-full transition-colors flex items-center"
          >
            <Mic className="w-6 h-6" />
          </button>
        ) : (
          <button
            onClick={stopRecording}
            className="bg-gray-600 hover:bg-gray-700 text-white p-4 rounded-full transition-colors flex items-center"
          >
            <Square className="w-6 h-6" />
          </button>
        )}
      </div>

      <div className="text-center text-sm text-gray-500">
        {isRecording ? 'Click stop to finish recording' : 'Click microphone to start recording'}
      </div>
    </div>
  );
}
