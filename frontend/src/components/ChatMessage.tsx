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
  const hasStructuredContent = (message.metadata?.insights && message.metadata.insights.length > 0) || 
                                message.metadata?.explanation ||
                                content.includes('NOTABLE PATTERN') || 
                                content.includes('ACTIONABLE RECOMMENDATION') ||
                                content.includes('INSIGHTS:') ||
                                content.includes('EXPLANATION:');
  
  // If we have structured content in metadata, show minimal or no text in bubble
  // The InsightsCard will display everything nicely
  const mainContent = hasStructuredContent && message.metadata?.insights
    ? "" // Don't show raw text if we have structured insights
    : hasStructuredContent
    ? content.split('NOTABLE PATTERN')[0].split('ACTIONABLE RECOMMENDATION')[0].split('INSIGHTS:')[0].split('EXPLANATION:')[0].trim()
    : content;

  return (
    <div className={`flex gap-4 mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="flex-shrink-0 w-10 h-10 rounded-full bg-[#588157] flex items-center justify-center shadow-sm">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
      )}
      
      <div className={`flex flex-col max-w-3xl ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Cache and RAG Indicators */}
        {!isUser && (message.metadata?.cache_hit || message.metadata?.rag_used) && (
          <div className="flex items-center gap-2 mb-2 animate-fade-in">
            {message.metadata?.cache_hit && (
              <div className="flex items-center gap-1.5 px-3 py-1.5 bg-[#588157]/10 border border-[#588157]/30 rounded-lg text-[#588157] text-xs font-semibold shadow-sm">
                <Zap className="w-3.5 h-3.5 animate-pulse" />
                <span>Cache Hit</span>
                {message.metadata?.cache_similarity && (
                  <span className="ml-1 px-1.5 py-0.5 bg-[#588157]/20 rounded text-[#588157] text-[10px]">
                    {Math.round(message.metadata.cache_similarity * 100)}%
                  </span>
                )}
              </div>
            )}
            {message.metadata?.rag_used && (
              <div className="flex items-center gap-1.5 px-3 py-1.5 bg-[#D4A373]/10 border border-[#D4A373]/30 rounded-lg text-[#D4A373] text-xs font-semibold shadow-sm">
                <Database className="w-3.5 h-3.5" />
                <span>RAG Used</span>
                <span className="ml-1 text-[#D4A373]/70 text-[10px]">Custom Term</span>
              </div>
            )}
          </div>
        )}
        
        {/* Main message bubble - only show if we have content and no structured insights */}
        {mainContent && (!message.metadata?.insights || message.metadata.insights.length === 0) && (
          <div
            className={`rounded-2xl px-6 py-4 shadow-sm ${
              isUser
                ? 'bg-[#344E41] text-white border border-[#344E41]'
                : 'bg-white text-[#222] border border-[#DFE4DD]'
            }`}
          >
            <div className="whitespace-pre-wrap leading-relaxed text-[15px]">{mainContent.replace(/\*\*/g, '').trim()}</div>
          </div>
        )}
        
        {message.metadata?.error && (
          <div className="mt-2 px-4 py-2 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
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
        <div className="flex-shrink-0 w-10 h-10 rounded-full bg-[#D4A373] flex items-center justify-center shadow-sm">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;

