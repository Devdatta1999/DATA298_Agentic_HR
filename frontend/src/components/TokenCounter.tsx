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
      <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-slate-800/90 to-slate-900/90 border border-slate-700/50 rounded-lg shadow-lg backdrop-blur-sm">
        <Zap className="w-4 h-4 text-yellow-400" />
        <span className="text-sm text-slate-300">
          <span className="font-bold text-yellow-400">{tokenCount.toLocaleString()}</span>
          <span className="text-slate-400 ml-1">total tokens</span>
        </span>
      </div>

      {/* Last Query Tokens */}
      {lastQueryTokens > 0 && (
        <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-800/90 to-blue-900/90 border border-blue-700/50 rounded-lg shadow-lg backdrop-blur-sm">
          <Zap className="w-4 h-4 text-blue-400" />
          <span className="text-sm text-slate-300">
            <span className="font-bold text-blue-400">{lastQueryTokens.toLocaleString()}</span>
            <span className="text-slate-400 ml-1">this query</span>
          </span>
        </div>
      )}

      {/* Response Time */}
      {lastResponseTime > 0 && (
        <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-800/90 to-green-900/90 border border-green-700/50 rounded-lg shadow-lg backdrop-blur-sm">
          <Clock className="w-4 h-4 text-green-400" />
          <span className="text-sm text-slate-300">
            <span className="font-bold text-green-400">{(lastResponseTime / 1000).toFixed(1)}s</span>
            <span className="text-slate-400 ml-1">response time</span>
          </span>
        </div>
      )}
    </div>
  );
};

export default TokenCounter;


