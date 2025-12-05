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
      <div className="flex items-center gap-2 px-4 py-2 bg-white border border-[#DFE4DD] rounded-lg shadow-sm">
        <Zap className="w-4 h-4 text-[#588157]" />
        <span className="text-sm text-[#222]">
          <span className="font-bold text-[#588157]">{tokenCount.toLocaleString()}</span>
          <span className="text-[#344E41] ml-1">total tokens</span>
        </span>
      </div>

      {/* Last Query Tokens */}
      {lastQueryTokens > 0 && (
        <div className="flex items-center gap-2 px-4 py-2 bg-white border border-[#DFE4DD] rounded-lg shadow-sm">
          <Zap className="w-4 h-4 text-[#D4A373]" />
          <span className="text-sm text-[#222]">
            <span className="font-bold text-[#D4A373]">{lastQueryTokens.toLocaleString()}</span>
            <span className="text-[#344E41] ml-1">this query</span>
          </span>
        </div>
      )}

      {/* Response Time */}
      {lastResponseTime > 0 && (
        <div className="flex items-center gap-2 px-4 py-2 bg-white border border-[#DFE4DD] rounded-lg shadow-sm">
          <Clock className="w-4 h-4 text-[#588157]" />
          <span className="text-sm text-[#222]">
            <span className="font-bold text-[#588157]">{(lastResponseTime / 1000).toFixed(1)}s</span>
            <span className="text-[#344E41] ml-1">response time</span>
          </span>
        </div>
      )}
    </div>
  );
};

export default TokenCounter;


