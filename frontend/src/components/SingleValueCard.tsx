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
      return <DollarSign className="w-8 h-8 text-[#D4A373]" />;
    }
    if (questionLower.includes('employee') || questionLower.includes('headcount') || questionLower.includes('count')) {
      return <Users className="w-8 h-8 text-[#588157]" />;
    }
    if (questionLower.includes('performance') || questionLower.includes('rating') || questionLower.includes('score')) {
      return <Award className="w-8 h-8 text-[#588157]" />;
    }
    return <BarChart3 className="w-8 h-8 text-[#344E41]" />;
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
    <div className="bg-white border border-[#DFE4DD] rounded-2xl p-8 shadow-sm mb-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          {getIcon()}
          <div>
            <h3 className="text-sm font-medium text-[#344E41] uppercase tracking-wide">Result</h3>
            <p className="text-xl font-bold text-[#222] mt-1">
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
                  ? 'bg-[#F8F9F5] border-[#588157]'
                  : 'bg-[#F8F9F5] border-[#DFE4DD]'
              } border rounded-xl p-5`}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-[#222] uppercase tracking-wide">
                  {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </span>
                <span
                  className={`text-3xl font-bold ${
                    isPrimary ? 'text-[#588157]' : 'text-[#222]'
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
        <div className="mt-6 pt-6 border-t border-[#DFE4DD]">
          <p className="text-sm text-[#344E41] text-center">
            Single value result - no chart visualization needed
          </p>
        </div>
      )}
    </div>
  );
};

export default SingleValueCard;

