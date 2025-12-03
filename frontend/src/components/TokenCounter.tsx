import React from 'react';
import { useChatStore } from '../store/chatStore';
import { Zap } from 'lucide-react';

const TokenCounter: React.FC = () => {
  const tokenCount = useChatStore((state) => state.tokenCount);

  return (
    <div className="flex items-center gap-2 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg">
      <Zap className="w-4 h-4 text-yellow-400" />
      <span className="text-sm text-gray-300">
        <span className="font-semibold text-yellow-400">{tokenCount.toLocaleString()}</span>
        {' '}tokens used
      </span>
    </div>
  );
};

export default TokenCounter;


