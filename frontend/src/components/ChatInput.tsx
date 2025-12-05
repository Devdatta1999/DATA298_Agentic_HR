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
    <form onSubmit={handleSubmit} className="p-6 bg-white border-t border-[#DFE4DD]">
      <div className="flex gap-3 max-w-5xl mx-auto">
        <div className="flex-1 relative">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask your HR question..."
            className="w-full px-6 py-4 bg-[#F8F9F5] border border-[#DFE4DD] rounded-xl text-[#222] placeholder-[#344E41]/50 focus:outline-none focus:ring-2 focus:ring-[#588157]/30 focus:border-[#588157] transition-all shadow-sm text-[15px]"
            disabled={isLoading}
          />
        </div>
        <button
          type="submit"
          disabled={!message.trim() || isLoading}
          className="px-8 py-4 bg-[#344E41] text-white rounded-xl hover:bg-[#588157] disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2 shadow-md hover:shadow-lg font-semibold text-[15px]"
        >
          <Send className="w-5 h-5" />
          {isLoading ? 'Processing...' : 'Send'}
        </button>
      </div>
    </form>
  );
};

export default ChatInput;


