import React from 'react';
import { Message } from '../store/chatStore';
import { Sparkles, User, Zap, Database } from 'lucide-react';
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
        <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center shadow-lg">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
      )}
      
      <div className={`flex flex-col max-w-3xl ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Cache and RAG Indicators */}
        {!isUser && (message.metadata?.cache_hit || message.metadata?.rag_used) && (
          <div className="flex items-center gap-2 mb-2 animate-fade-in">
            {message.metadata?.cache_hit && (
              <div className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/40 rounded-lg text-green-300 text-xs font-semibold shadow-lg backdrop-blur-sm">
                <Zap className="w-3.5 h-3.5 animate-pulse" />
                <span>Cache Hit</span>
                {message.metadata?.cache_similarity && (
                  <span className="ml-1 px-1.5 py-0.5 bg-green-500/30 rounded text-green-200 text-[10px]">
                    {Math.round(message.metadata.cache_similarity * 100)}%
                  </span>
                )}
              </div>
            )}
            {message.metadata?.rag_used && (
              <div className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-purple-500/20 to-indigo-500/20 border border-purple-500/40 rounded-lg text-purple-300 text-xs font-semibold shadow-lg backdrop-blur-sm">
                <Database className="w-3.5 h-3.5" />
                <span>RAG Used</span>
                <span className="ml-1 text-purple-200/70 text-[10px]">Custom Term</span>
              </div>
            )}
          </div>
        )}
        
        {/* Main message bubble */}
        <div
          className={`rounded-2xl px-6 py-4 shadow-xl backdrop-blur-sm ${
            isUser
              ? 'bg-gradient-to-br from-teal-500/90 to-cyan-600/90 text-white border border-teal-400/20'
              : 'bg-gradient-to-br from-emerald-900/90 to-teal-900/90 text-emerald-50 border border-emerald-700/50'
          }`}
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
        <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-teal-500 to-cyan-500 flex items-center justify-center shadow-lg">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;

