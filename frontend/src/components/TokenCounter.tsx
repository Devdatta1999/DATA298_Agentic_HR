import React from 'react';
import { useChatStore } from '../store/chatStore';
import { Zap, Clock } from 'lucide-react';

const TokenCounter: React.FC = () => {
  const tokenCount = useChatStore((state) => state.tokenCount);
  const lastQueryTokens = useChatStore((state) => state.lastQueryTokens);
  const lastResponseTime = useChatStore((state) => state.lastResponseTime);

  return (
    <div className="flex items-center gap-4">
      {/* Total Tokens */}
      <div className="flex items-center gap-2 px-4 py-2 rounded-lg shadow-lg backdrop-blur-sm" style={{
        backgroundColor: '#11182A',
        border: '1px solid rgba(30, 42, 64, 0.5)'
      }}>
        <Zap className="w-4 h-4" style={{ color: '#F9A23F' }} />
        <span className="text-sm" style={{ color: '#FFFFFF' }}>
          <span className="font-bold" style={{ color: '#F9A23F' }}>{tokenCount.toLocaleString()}</span>
          <span className="ml-1" style={{ color: '#B6C2CC' }}>total tokens</span>
        </span>
      </div>

      {/* Last Query Tokens */}
      {lastQueryTokens > 0 && (
        <div className="flex items-center gap-2 px-4 py-2 rounded-lg shadow-lg backdrop-blur-sm" style={{
          backgroundColor: '#11182A',
          border: '1px solid rgba(110, 193, 228, 0.3)'
        }}>
          <Zap className="w-4 h-4" style={{ color: '#6EC1E4' }} />
          <span className="text-sm" style={{ color: '#FFFFFF' }}>
            <span className="font-bold" style={{ color: '#6EC1E4' }}>{lastQueryTokens.toLocaleString()}</span>
            <span className="ml-1" style={{ color: '#B6C2CC' }}>this query</span>
          </span>
        </div>
      )}

      {/* Response Time */}
      {lastResponseTime > 0 && (
        <div className="flex items-center gap-2 px-4 py-2 rounded-lg shadow-lg backdrop-blur-sm" style={{
          backgroundColor: '#11182A',
          border: '1px solid rgba(30, 42, 64, 0.5)'
        }}>
          <Clock className="w-4 h-4" style={{ color: '#6EC1E4' }} />
          <span className="text-sm" style={{ color: '#FFFFFF' }}>
            <span className="font-bold" style={{ color: '#6EC1E4' }}>{(lastResponseTime / 1000).toFixed(1)}s</span>
            <span className="ml-1" style={{ color: '#B6C2CC' }}>response time</span>
          </span>
        </div>
      )}
    </div>
  );
};

export default TokenCounter;


