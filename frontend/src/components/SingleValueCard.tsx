import React from 'react';
import { BarChart3, TrendingUp, Users, DollarSign, Award } from 'lucide-react';

interface SingleValueCardProps {
  data: any[];
  question?: string;
}

const SingleValueCard: React.FC<SingleValueCardProps> = ({ data, question }) => {
  if (!data || data.length === 0) {
    return null;
  }

  const firstRow = data[0];
  const keys = Object.keys(firstRow);
  const values = Object.values(firstRow);

  // Determine icon based on question or data type
  const getIcon = () => {
    const questionLower = (question || '').toLowerCase();
    if (questionLower.includes('salary') || questionLower.includes('compensation')) {
      return <DollarSign className="w-8 h-8 text-green-400" />;
    }
    if (questionLower.includes('employee') || questionLower.includes('headcount') || questionLower.includes('count')) {
      return <Users className="w-8 h-8 text-blue-400" />;
    }
    if (questionLower.includes('performance') || questionLower.includes('rating') || questionLower.includes('score')) {
      return <Award className="w-8 h-8 text-purple-400" />;
    }
    return <BarChart3 className="w-8 h-8 text-cyan-400" />;
  };

  // Format value based on type
  const formatValue = (value: any): string => {
    if (typeof value === 'number') {
      // Format large numbers with commas
      if (value >= 1000) {
        return value.toLocaleString('en-US', { maximumFractionDigits: 2 });
      }
      return value.toString();
    }
    return String(value);
  };

  return (
    <div className="bg-gradient-to-br from-slate-800/95 via-slate-900/95 to-slate-800/95 border border-slate-700/50 rounded-2xl p-8 shadow-2xl mb-6 backdrop-blur-sm">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          {getIcon()}
          <div>
            <h3 className="text-sm font-medium text-slate-400 uppercase tracking-wide">Result</h3>
            <p className="text-xl font-bold text-white mt-1">
              {keys[0]?.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {keys.map((key, idx) => {
          const value = values[idx];
          const isPrimary = idx === 0;
          
          return (
            <div
              key={key}
              className={`${
                isPrimary
                  ? 'bg-gradient-to-r from-purple-500/20 to-blue-500/20 border-purple-500/30 backdrop-blur-sm'
                  : 'bg-slate-700/30 border-slate-600/50 backdrop-blur-sm'
              } border rounded-xl p-5`}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-slate-300 uppercase tracking-wide">
                  {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </span>
                <span
                  className={`text-3xl font-bold ${
                    isPrimary ? 'text-purple-300' : 'text-white'
                  }`}
                >
                  {formatValue(value)}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {keys.length === 1 && (
        <div className="mt-6 pt-6 border-t border-slate-700/50">
          <p className="text-sm text-slate-400 text-center">
            Single value result - no chart visualization needed
          </p>
        </div>
      )}
    </div>
  );
};

export default SingleValueCard;

