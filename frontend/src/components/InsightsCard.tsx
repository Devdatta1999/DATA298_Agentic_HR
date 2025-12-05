import React from 'react';
import { Lightbulb, TrendingUp, Target } from 'lucide-react';

interface InsightsCardProps {
  insights?: string[];
  explanation?: string;
}

const InsightsCard: React.FC<InsightsCardProps> = ({ insights, explanation }) => {
  // Parse explanation for patterns and recommendations
  // Try different variations of section headers
  const patternsMatch = explanation?.match(/NOTABLE PATTERNS?[^:]*:?\s*(.*?)(?=ACTIONABLE RECOMMENDATION|$)/is);
  let patterns = patternsMatch?.[1]?.trim();
  
  // Clean patterns - remove asterisks and other markdown
  if (patterns) {
    patterns = patterns
      .replace(/\*/g, '') // Remove all asterisks
      .replace(/^\d+\.\s*/gm, '') // Remove numbered list markers
      .trim();
  }
  
  const recommendationsMatch = explanation?.match(/ACTIONABLE RECOMMENDATIONS?[^:]*:?\s*(.*?)$/is);
  let recommendations = recommendationsMatch?.[1]?.trim();
  
  // Clean up recommendations - remove markdown formatting and validate
  if (recommendations) {
    recommendations = recommendations
      .replace(/\*\*/g, '')  // Remove bold markers
      .replace(/^\d+\.\s*/gm, '')  // Remove numbered list markers
      .trim();
    
    // Only show if it has meaningful content (more than just "Recommendation 1" etc)
    if (recommendations.length < 30 || recommendations.match(/^recommendation\s*\d+/i)) {
      recommendations = '';
    }
  }
  
  // Get clean explanation (before patterns and recommendations)
  let cleanExplanation = explanation || '';
  if (cleanExplanation.includes('NOTABLE PATTERN')) {
    cleanExplanation = cleanExplanation.split(/NOTABLE PATTERN/i)[0].trim();
  }
  if (cleanExplanation.includes('ACTIONABLE RECOMMENDATION')) {
    cleanExplanation = cleanExplanation.split(/ACTIONABLE RECOMMENDATION/i)[0].trim();
  }

  return (
    <div className="space-y-4 mt-4">
      {/* Key Insights Section */}
      {insights && insights.length > 0 && (
        <div className="bg-white border border-[#DFE4DD] rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="w-5 h-5 text-[#588157]" />
            <h4 className="text-lg font-semibold text-[#222]">Key Insights</h4>
          </div>
          <ul className="space-y-3">
            {insights.map((insight, idx) => (
              <li key={idx} className="flex items-start gap-3 text-[#222]">
                <div className="flex-shrink-0 mt-1.5 w-6 h-6 rounded-full bg-[#588157]/10 flex items-center justify-center border border-[#588157]/20">
                  <div className="w-2 h-2 rounded-full bg-[#588157]"></div>
                </div>
                <span className="flex-1 leading-relaxed text-[15px] text-[#222]">{insight.replace(/\*\*/g, '').trim()}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Explanation Section */}
      {cleanExplanation && (
        <div className="bg-white border border-[#DFE4DD] rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-5 h-5 text-[#344E41]" />
            <h4 className="text-lg font-semibold text-[#222]">Analysis</h4>
          </div>
          <p className="text-[#344E41] leading-relaxed whitespace-pre-line">{cleanExplanation.replace(/\*\*/g, '').trim()}</p>
        </div>
      )}

      {/* Patterns Section */}
      {patterns && (
        <div className="bg-white border border-[#DFE4DD] rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp className="w-5 h-5 text-[#588157]" />
            <h4 className="text-lg font-semibold text-[#222]">Notable Patterns & Trends</h4>
          </div>
          <div className="space-y-3">
            {patterns
              .replace(/\*/g, '') // Remove all asterisks first
              .split(/[•\-\n]/)
              .filter(p => {
                const trimmed = p.trim();
                return trimmed && trimmed.length > 10 && !trimmed.startsWith('**') && !trimmed.match(/^\d+\.?\s*$/) && !trimmed.match(/^[\*\•\-\s]+$/);
              })
              .map((pattern, idx) => (
                <div key={idx} className="flex items-start gap-3 text-[#222]">
                  <div className="flex-shrink-0 mt-1.5 w-6 h-6 rounded-full bg-[#588157]/10 flex items-center justify-center border border-[#588157]/20">
                    <div className="w-2 h-2 rounded-full bg-[#588157]"></div>
                  </div>
                  <span className="flex-1 leading-relaxed text-[15px] text-[#222]">{pattern.trim().replace(/\*\*/g, '').replace(/^\*\s*/, '')}</span>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Recommendations Section - Only show if recommendations exist and have meaningful content */}
      {recommendations && recommendations.trim() && recommendations.length > 20 && !recommendations.includes('**') && (
        <div className="bg-white border border-[#DFE4DD] rounded-xl p-5 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Target className="w-5 h-5 text-[#D4A373]" />
            <h4 className="text-lg font-semibold text-[#222]">Actionable Recommendations</h4>
          </div>
          <div className="space-y-3">
            {recommendations
              .replace(/\*/g, '') // Remove asterisks
              .split(/[•\-\n]/)
              .filter(r => {
                const trimmed = r.trim();
                return trimmed && trimmed.length > 10 && !trimmed.startsWith('**') && !trimmed.match(/^\d+\.?\s*$/) && !trimmed.match(/^[\*\•\-\s]+$/);
              })
              .map((rec, idx) => (
                <div key={idx} className="flex items-start gap-3 text-[#222]">
                  <div className="flex-shrink-0 mt-1.5 w-6 h-6 rounded-full bg-[#D4A373]/10 flex items-center justify-center border border-[#D4A373]/20">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#D4A373]"></div>
                  </div>
                  <span className="flex-1 leading-relaxed text-[15px] text-[#222]">{rec.trim().replace(/\*\*/g, '')}</span>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default InsightsCard;

