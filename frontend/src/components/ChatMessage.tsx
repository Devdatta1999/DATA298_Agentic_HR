import React from 'react';
import { Message } from '../store/chatStore';
import { Sparkles, User } from 'lucide-react';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-4 mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
      )}
      
      <div className={`flex flex-col max-w-3xl ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`rounded-lg px-4 py-3 ${
            isUser
              ? 'bg-blue-600 text-white'
              : 'bg-gray-800 text-gray-100 border border-gray-700'
          }`}
        >
          <div className="whitespace-pre-wrap">{message.content}</div>
        </div>
        
        {message.metadata?.error && (
          <div className="mt-2 text-red-400 text-sm">Error occurred</div>
        )}
        
        {message.metadata?.insights && message.metadata.insights.length > 0 && (
          <div className="mt-3 bg-gray-800 border border-gray-700 rounded-lg p-4 w-full">
            <h4 className="text-sm font-semibold text-purple-400 mb-2">Key Insights:</h4>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-300">
              {message.metadata.insights.map((insight, idx) => (
                <li key={idx}>{insight}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
      
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;

