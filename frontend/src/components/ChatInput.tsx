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
    <form onSubmit={handleSubmit} className="p-6 bg-gradient-to-r from-emerald-900/95 to-teal-900/95 border-t border-emerald-700/50 backdrop-blur-sm">
      <div className="flex gap-3 max-w-5xl mx-auto">
        <div className="flex-1 relative">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask your HR question... (e.g., Calculate Internal Mobility Rate)"
            className="w-full px-6 py-4 bg-emerald-900/60 border border-emerald-600/50 rounded-xl text-emerald-50 placeholder-emerald-300/50 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 transition-all shadow-xl backdrop-blur-sm text-[15px]"
            disabled={isLoading}
          />
        </div>
        <button
          type="submit"
          disabled={!message.trim() || isLoading}
          className="px-8 py-4 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-xl hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2 shadow-xl font-semibold text-[15px] backdrop-blur-sm border border-emerald-400/20"
        >
          <Send className="w-5 h-5" />
          {isLoading ? 'Processing...' : 'Send'}
        </button>
      </div>
    </form>
  );
};

export default ChatInput;


