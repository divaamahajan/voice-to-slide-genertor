'use client';

import { useState } from 'react';
import { Copy, Download, FileText, Languages } from 'lucide-react';

interface TranscriptionDisplayProps {
  transcription: string;
  translation: string;
  onClear: () => void;
}

export default function TranscriptionDisplay({ transcription, translation, onClear }: TranscriptionDisplayProps) {
  const [copiedText, setCopiedText] = useState<string>('');

  const copyToClipboard = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedText(type);
      setTimeout(() => setCopiedText(''), 2000);
    } catch (error) {
      console.error('Failed to copy text:', error);
    }
  };

  const downloadText = (text: string, filename: string) => {
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!transcription && !translation) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Results</h2>
        <div className="text-center text-gray-500 py-8">
          <FileText className="w-12 h-12 mx-auto mb-4 text-gray-300" />
          <p>No transcription or translation yet</p>
          <p className="text-sm">Record audio or upload a file to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Transcription */}
      {transcription && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold flex items-center">
              <FileText className="w-5 h-5 mr-2" />
              Transcription
            </h3>
            <div className="flex space-x-2">
              <button
                onClick={() => copyToClipboard(transcription, 'transcription')}
                className="text-gray-500 hover:text-blue-600 transition-colors"
                title="Copy transcription"
              >
                <Copy className="w-4 h-4" />
              </button>
              <button
                onClick={() => downloadText(transcription, 'transcription.txt')}
                className="text-gray-500 hover:text-green-600 transition-colors"
                title="Download transcription"
              >
                <Download className="w-4 h-4" />
              </button>
            </div>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-gray-800 leading-relaxed">{transcription}</p>
          </div>
          {copiedText === 'transcription' && (
            <p className="text-sm text-green-600 mt-2">Copied to clipboard!</p>
          )}
        </div>
      )}

      {/* Translation */}
      {translation && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold flex items-center">
              <Languages className="w-5 h-5 mr-2" />
              Translation
            </h3>
            <div className="flex space-x-2">
              <button
                onClick={() => copyToClipboard(translation, 'translation')}
                className="text-gray-500 hover:text-blue-600 transition-colors"
                title="Copy translation"
              >
                <Copy className="w-4 h-4" />
              </button>
              <button
                onClick={() => downloadText(translation, 'translation.txt')}
                className="text-gray-500 hover:text-green-600 transition-colors"
                title="Download translation"
              >
                <Download className="w-4 h-4" />
              </button>
            </div>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-gray-800 leading-relaxed">{translation}</p>
          </div>
          {copiedText === 'translation' && (
            <p className="text-sm text-green-600 mt-2">Copied to clipboard!</p>
          )}
        </div>
      )}
    </div>
  );
}
