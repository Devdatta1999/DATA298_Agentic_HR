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
      <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-emerald-800/90 to-teal-900/90 border border-emerald-700/50 rounded-lg shadow-lg backdrop-blur-sm">
        <Zap className="w-4 h-4 text-emerald-300" />
        <span className="text-sm text-emerald-100">
          <span className="font-bold text-emerald-300">{tokenCount.toLocaleString()}</span>
          <span className="text-emerald-200/70 ml-1">total tokens</span>
        </span>
      </div>

      {/* Last Query Tokens */}
      {lastQueryTokens > 0 && (
        <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-teal-800/90 to-cyan-900/90 border border-teal-700/50 rounded-lg shadow-lg backdrop-blur-sm">
          <Zap className="w-4 h-4 text-teal-300" />
          <span className="text-sm text-teal-100">
            <span className="font-bold text-teal-300">{lastQueryTokens.toLocaleString()}</span>
            <span className="text-teal-200/70 ml-1">this query</span>
          </span>
        </div>
      )}

      {/* Response Time */}
      {lastResponseTime > 0 && (
        <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-emerald-800/90 to-emerald-900/90 border border-emerald-700/50 rounded-lg shadow-lg backdrop-blur-sm">
          <Clock className="w-4 h-4 text-emerald-300" />
          <span className="text-sm text-emerald-100">
            <span className="font-bold text-emerald-300">{(lastResponseTime / 1000).toFixed(1)}s</span>
            <span className="text-emerald-200/70 ml-1">response time</span>
          </span>
        </div>
      )}
    </div>
  );
};

export default TokenCounter;


