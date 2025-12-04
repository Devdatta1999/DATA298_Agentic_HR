import React, { useState } from 'react';
import { Send, Database } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend, isLoading }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSend(message.trim());
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-6 backdrop-blur-sm">
      <div className="flex gap-3 max-w-5xl mx-auto">
        <div className="flex-1 relative">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask your HR question... (e.g., Show me department wise headcount)"
            className="w-full px-6 py-4 rounded-xl transition-all shadow-xl backdrop-blur-sm text-[15px] focus:outline-none focus:ring-2"
            style={{
              backgroundColor: '#1E2A40',
              border: '1px solid rgba(30, 42, 64, 0.6)',
              color: '#FFFFFF',
              placeholderColor: '#B6C2CC'
            }}
            onFocus={(e) => {
              e.target.style.borderColor = '#F9A23F';
              e.target.style.boxShadow = '0 0 0 2px rgba(249, 162, 63, 0.3)';
            }}
            onBlur={(e) => {
              e.target.style.borderColor = 'rgba(30, 42, 64, 0.6)';
              e.target.style.boxShadow = 'none';
            }}
            disabled={isLoading}
          />
        </div>
        <button
          type="submit"
          disabled={!message.trim() || isLoading}
          className="px-8 py-4 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2 shadow-xl font-semibold text-[15px] backdrop-blur-sm"
          style={{
            backgroundColor: '#F9A23F',
            color: '#0A0F1F',
            border: '1px solid rgba(249, 162, 63, 0.3)'
          }}
          onMouseEnter={(e) => {
            if (!e.currentTarget.disabled) {
              e.currentTarget.style.backgroundColor = 'rgba(249, 162, 63, 0.9)';
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = '#F9A23F';
          }}
        >
          <Send className="w-5 h-5" />
          {isLoading ? 'Processing...' : 'Send'}
        </button>
      </div>
    </form>
  );
};

export default ChatInput;


