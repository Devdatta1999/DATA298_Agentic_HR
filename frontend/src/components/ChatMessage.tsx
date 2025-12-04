import React from 'react';
import { Message } from '../store/chatStore';
import { Sparkles, User } from 'lucide-react';
import InsightsCard from './InsightsCard';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  // Extract main content (before insights/patterns/recommendations)
  const content = message.content;
  const hasStructuredContent = content.includes('NOTABLE PATTERN') || content.includes('ACTIONABLE RECOMMENDATION');
  const mainContent = hasStructuredContent 
    ? content.split('NOTABLE PATTERN')[0].split('ACTIONABLE RECOMMENDATION')[0].trim()
    : content;

  return (
    <div className={`flex gap-4 mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg" style={{ backgroundColor: '#F9A23F' }}>
          <Sparkles className="w-5 h-5" style={{ color: '#0A0F1F' }} />
        </div>
      )}
      
      <div className={`flex flex-col max-w-3xl ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Main message bubble */}
        <div
          className={`rounded-2xl px-6 py-4 shadow-xl backdrop-blur-sm ${
            isUser ? '' : ''
          }`}
          style={isUser ? {
            backgroundColor: '#F9A23F',
            color: '#0A0F1F',
            border: '1px solid rgba(249, 162, 63, 0.3)'
          } : {
            backgroundColor: '#11182A',
            color: '#FFFFFF',
            border: '1px solid rgba(30, 42, 64, 0.5)'
          }}
        >
          <div className="whitespace-pre-wrap leading-relaxed text-[15px]">{mainContent.replace(/\*\*/g, '').trim()}</div>
        </div>
        
        {message.metadata?.error && (
          <div className="mt-2 px-4 py-2 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
            Error occurred
          </div>
        )}
        
        {/* Insights and structured content */}
        {!isUser && (message.metadata?.insights || message.metadata?.explanation) && (
          <div className="w-full mt-3">
            <InsightsCard
              insights={message.metadata.insights}
              explanation={message.metadata.explanation || content}
            />
          </div>
        )}
      </div>
      
      {isUser && (
        <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg" style={{ backgroundColor: '#6EC1E4' }}>
          <User className="w-5 h-5" style={{ color: '#0A0F1F' }} />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;

