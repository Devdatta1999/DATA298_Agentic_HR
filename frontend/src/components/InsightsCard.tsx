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
  const patterns = patternsMatch?.[1]?.trim();
  
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
        <div className="bg-gradient-to-br from-emerald-500/10 to-teal-500/10 border border-emerald-500/20 rounded-xl p-5 shadow-lg">
          <div className="flex items-center gap-2 mb-3">
            <Lightbulb className="w-5 h-5 text-emerald-400" />
            <h4 className="text-lg font-semibold text-emerald-300">Key Insights</h4>
          </div>
          <ul className="space-y-3">
            {insights.map((insight, idx) => (
              <li key={idx} className="flex items-start gap-3 text-emerald-50">
                <span className="text-emerald-400 mt-1.5 flex-shrink-0 w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                <span className="flex-1 leading-relaxed">{insight.replace(/\*\*/g, '').trim()}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Explanation Section */}
      {cleanExplanation && (
        <div className="bg-gradient-to-br from-teal-500/10 to-cyan-500/10 border border-teal-500/20 rounded-xl p-5 shadow-lg">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-5 h-5 text-teal-400" />
            <h4 className="text-lg font-semibold text-teal-300">Analysis</h4>
          </div>
          <p className="text-emerald-50 leading-relaxed whitespace-pre-line">{cleanExplanation.replace(/\*\*/g, '').trim()}</p>
        </div>
      )}

      {/* Patterns Section */}
      {patterns && (
        <div className="bg-gradient-to-br from-amber-500/10 to-orange-500/10 border border-amber-500/20 rounded-xl p-5 shadow-lg">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-5 h-5 text-amber-400" />
            <h4 className="text-lg font-semibold text-amber-300">Notable Patterns & Trends</h4>
          </div>
          <p className="text-gray-200 leading-relaxed whitespace-pre-line">{patterns.replace(/\*\*/g, '').trim()}</p>
        </div>
      )}

      {/* Recommendations Section - Only show if recommendations exist and have meaningful content */}
      {recommendations && recommendations.trim() && recommendations.length > 20 && !recommendations.includes('**') && (
        <div className="bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/20 rounded-xl p-5 shadow-lg">
          <div className="flex items-center gap-2 mb-3">
            <Target className="w-5 h-5 text-green-400" />
            <h4 className="text-lg font-semibold text-green-300">Actionable Recommendations</h4>
          </div>
          <div className="space-y-3">
            {recommendations
              .split(/[•\-\n]/)
              .filter(r => {
                const trimmed = r.trim();
                return trimmed && trimmed.length > 10 && !trimmed.startsWith('**') && !trimmed.match(/^\d+\.?\s*$/);
              })
              .map((rec, idx) => (
                <div key={idx} className="flex items-start gap-3 text-gray-200">
                  <span className="text-green-400 mt-1 flex-shrink-0">→</span>
                  <span className="flex-1 leading-relaxed">{rec.trim().replace(/\*\*/g, '')}</span>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default InsightsCard;

