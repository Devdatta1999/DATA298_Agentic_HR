import React, { useState, useEffect, useRef } from 'react';
import { Zap, Database, TrendingUp, Sparkles } from 'lucide-react';

interface LandingPageProps {
  onEnterChat: () => void;
}

const HR_QUOTES = [
  { text: "The best way to predict the future is to create it.", author: "Peter Drucker" },
  { text: "People are not your most important asset. The right people are.", author: "Jim Collins" },
  { text: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
  { text: "Innovation distinguishes between a leader and a follower.", author: "Steve Jobs" },
  { text: "Data is the new oil, but insights are the new gold.", author: "Unknown" },
];

const LandingPage: React.FC<LandingPageProps> = ({ onEnterChat }) => {
  const [currentQuoteIndex, setCurrentQuoteIndex] = useState(0);
  const [fadeIn, setFadeIn] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setFadeIn(false);
      setTimeout(() => {
        setCurrentQuoteIndex((prev) => (prev + 1) % HR_QUOTES.length);
        setFadeIn(true);
      }, 500);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const currentQuote = HR_QUOTES[currentQuoteIndex];

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#F8F9F5] via-[#F0F4ED] to-[#F8F9F5] relative overflow-hidden">
      {/* Animated CSS */}
      <style>{`
        @keyframes float {
          0%, 100% {
            transform: translateY(0px) translateX(0px);
          }
          33% {
            transform: translateY(-20px) translateX(10px);
          }
          66% {
            transform: translateY(10px) translateX(-10px);
          }
        }
        
        @keyframes pulse {
          0%, 100% {
            opacity: 0.4;
            transform: scale(1);
          }
          50% {
            opacity: 0.8;
            transform: scale(1.1);
          }
        }
        
        @keyframes rotate {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }
        
        @keyframes drawLine {
          from {
            stroke-dashoffset: 1000;
          }
          to {
            stroke-dashoffset: 0;
          }
        }
        
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
        
        .animate-float-delayed {
          animation: float 8s ease-in-out infinite;
          animation-delay: 2s;
        }
        
        .animate-pulse-slow {
          animation: pulse 4s ease-in-out infinite;
        }
        
        .animate-rotate-slow {
          animation: rotate 20s linear infinite;
        }
        
        .animate-draw {
          stroke-dasharray: 1000;
          animation: drawLine 3s ease-in-out infinite;
        }
      `}</style>

      {/* Enhanced Background Elements - HR/People Analytics Vibe */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Large animated gradient orbs */}
        <div className="absolute top-0 left-0 w-[600px] h-[600px] bg-gradient-to-br from-[#588157]/15 via-[#344E41]/10 to-transparent rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-0 right-0 w-[700px] h-[700px] bg-gradient-to-tl from-[#D4A373]/12 via-[#588157]/8 to-transparent rounded-full blur-3xl animate-float-delayed"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-[#588157]/8 via-[#344E41]/5 to-[#D4A373]/8 rounded-full blur-3xl animate-pulse-slow"></div>
        
        {/* Background Charts - Spread Across Entire Page Using Individual Positioned Divs */}
        
        {/* Bar Chart 1 - Top Left */}
        <div className="absolute top-20 left-16 opacity-[0.25] animate-float" style={{ pointerEvents: 'none' }}>
          <svg width="150" height="130" viewBox="0 0 150 130">
            <rect x="0" y="60" width="18" height="50" fill="#588157" rx="3" opacity="0.7" className="animate-pulse-slow" />
            <rect x="25" y="40" width="18" height="70" fill="#588157" rx="3" opacity="0.7" style={{ animationDelay: '0.2s' }} className="animate-pulse-slow" />
            <rect x="50" y="25" width="18" height="85" fill="#588157" rx="3" opacity="0.7" style={{ animationDelay: '0.4s' }} className="animate-pulse-slow" />
            <rect x="75" y="50" width="18" height="60" fill="#588157" rx="3" opacity="0.7" style={{ animationDelay: '0.6s' }} className="animate-pulse-slow" />
            <rect x="100" y="35" width="18" height="75" fill="#588157" rx="3" opacity="0.7" style={{ animationDelay: '0.8s' }} className="animate-pulse-slow" />
            <text x="9" y="125" fontSize="9" fill="#344E41" opacity="0.5">Q1</text>
            <text x="34" y="125" fontSize="9" fill="#344E41" opacity="0.5">Q2</text>
            <text x="59" y="125" fontSize="9" fill="#344E41" opacity="0.5">Q3</text>
            <text x="84" y="125" fontSize="9" fill="#344E41" opacity="0.5">Q4</text>
          </svg>
        </div>
        
        {/* Line Chart 1 - Top Right */}
        <div className="absolute top-16 right-20 opacity-[0.25] animate-float-delayed" style={{ pointerEvents: 'none' }}>
          <svg width="250" height="120" viewBox="0 0 250 120">
            <line x1="0" y1="0" x2="0" y2="90" stroke="#DFE4DD" strokeWidth="1" opacity="0.3" />
            <line x1="0" y1="90" x2="220" y2="90" stroke="#DFE4DD" strokeWidth="1" opacity="0.3" />
            <polyline
              points="0,75 35,70 70,55 105,60 140,40 175,45 210,30"
              fill="none"
              stroke="#588157"
              strokeWidth="3"
              opacity="0.8"
            />
            <circle cx="0" cy="75" r="5" fill="#588157" opacity="0.9" />
            <circle cx="70" cy="55" r="5" fill="#588157" opacity="0.9" />
            <circle cx="140" cy="40" r="5" fill="#588157" opacity="0.9" />
            <circle cx="210" cy="30" r="5" fill="#588157" opacity="0.9" />
            <text x="0" y="105" fontSize="10" fill="#344E41" opacity="0.6">Jan</text>
            <text x="70" y="105" fontSize="10" fill="#344E41" opacity="0.6">Jun</text>
            <text x="140" y="105" fontSize="10" fill="#344E41" opacity="0.6">Dec</text>
          </svg>
        </div>
        
        {/* Pie Chart 1 - Left Center */}
        <div className="absolute top-1/2 left-12 -translate-y-1/2 opacity-[0.25] animate-rotate-slow" style={{ pointerEvents: 'none' }}>
          <svg width="120" height="120" viewBox="-60 -60 120 120">
            <circle cx="0" cy="0" r="55" fill="none" stroke="#DFE4DD" strokeWidth="2" opacity="0.3" />
            <path d="M 0,0 L 0,-55 A 55,55 0 0,1 38.89,-38.89 Z" fill="#588157" opacity="0.7" />
            <path d="M 0,0 L 38.89,-38.89 A 55,55 0 0,1 55,0 Z" fill="#344E41" opacity="0.7" />
            <path d="M 0,0 L 55,0 A 55,55 0 0,1 38.89,38.89 Z" fill="#D4A373" opacity="0.7" />
            <path d="M 0,0 L 38.89,38.89 A 55,55 0 0,1 0,55 Z" fill="#588157" opacity="0.7" />
            <circle cx="0" cy="0" r="22" fill="#F8F9F5" />
            <text x="-12" y="5" fontSize="11" fill="#344E41" fontWeight="bold">HR</text>
          </svg>
        </div>
        
        {/* Bar Chart 2 - Right Center */}
        <div className="absolute top-1/2 right-16 -translate-y-1/2 opacity-[0.25] animate-float" style={{ pointerEvents: 'none' }}>
          <svg width="200" height="100" viewBox="0 0 200 100">
            <rect x="0" y="50" width="22" height="45" fill="#344E41" rx="3" opacity="0.7" />
            <rect x="30" y="30" width="22" height="65" fill="#344E41" rx="3" opacity="0.7" />
            <rect x="60" y="20" width="22" height="75" fill="#344E41" rx="3" opacity="0.7" />
            <rect x="90" y="40" width="22" height="55" fill="#344E41" rx="3" opacity="0.7" />
            <rect x="120" y="25" width="22" height="70" fill="#344E41" rx="3" opacity="0.7" />
            <rect x="150" y="45" width="22" height="50" fill="#344E41" rx="3" opacity="0.7" />
          </svg>
        </div>
        
        {/* Line Chart 2 - Bottom Left */}
        <div className="absolute bottom-32 left-20 opacity-[0.25] animate-float-delayed" style={{ pointerEvents: 'none' }}>
          <svg width="220" height="120" viewBox="0 0 220 120">
            <line x1="0" y1="0" x2="0" y2="100" stroke="#DFE4DD" strokeWidth="1" opacity="0.3" />
            <line x1="0" y1="100" x2="200" y2="100" stroke="#DFE4DD" strokeWidth="1" opacity="0.3" />
            <polyline
              points="0,85 30,80 60,65 90,70 120,50 150,55 180,40"
              fill="none"
              stroke="#D4A373"
              strokeWidth="3"
              opacity="0.7"
            />
            <circle cx="0" cy="85" r="5" fill="#D4A373" opacity="0.8" />
            <circle cx="90" cy="70" r="5" fill="#D4A373" opacity="0.8" />
            <circle cx="180" cy="40" r="5" fill="#D4A373" opacity="0.8" />
          </svg>
        </div>
        
        {/* Pie Chart 2 - Bottom Right */}
        <div className="absolute bottom-24 right-20 opacity-[0.25] animate-rotate-slow" style={{ pointerEvents: 'none' }}>
          <svg width="110" height="110" viewBox="-55 -55 110 110">
            <circle cx="0" cy="0" r="50" fill="none" stroke="#DFE4DD" strokeWidth="2" opacity="0.3" />
            <path d="M 0,0 L 0,-50 A 50,50 0 0,1 35.36,-35.36 Z" fill="#D4A373" opacity="0.7" />
            <path d="M 0,0 L 35.36,-35.36 A 50,50 0 0,1 50,0 Z" fill="#588157" opacity="0.7" />
            <path d="M 0,0 L 50,0 A 50,50 0 0,1 35.36,35.36 Z" fill="#344E41" opacity="0.7" />
            <path d="M 0,0 L 35.36,35.36 A 50,50 0 0,1 0,50 Z" fill="#588157" opacity="0.7" />
          </svg>
        </div>
        
        {/* Area Chart - Center Right */}
        <div className="absolute top-1/2 right-1/4 -translate-y-1/2 opacity-[0.25] animate-float" style={{ pointerEvents: 'none' }}>
          <svg width="280" height="140" viewBox="0 0 280 140">
            <line x1="0" y1="0" x2="0" y2="120" stroke="#DFE4DD" strokeWidth="1" opacity="0.3" />
            <line x1="0" y1="120" x2="250" y2="120" stroke="#DFE4DD" strokeWidth="1" opacity="0.3" />
            <defs>
              <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="#588157" stopOpacity="0.6" />
                <stop offset="100%" stopColor="#588157" stopOpacity="0" />
              </linearGradient>
            </defs>
            <path
              d="M 0,95 L 40,85 L 80,60 L 120,70 L 160,40 L 200,50 L 240,30 L 240,120 L 200,120 L 160,120 L 120,120 L 80,120 L 40,120 L 0,120 Z"
              fill="url(#areaGradient)"
              opacity="0.6"
            />
            <polyline
              points="0,95 40,85 80,60 120,70 160,40 200,50 240,30"
              fill="none"
              stroke="#588157"
              strokeWidth="3"
              opacity="0.8"
            />
          </svg>
        </div>
        
        {/* Scatter Plot - Center Left */}
        <div className="absolute top-1/2 left-1/4 -translate-y-1/2 opacity-[0.25] animate-float-delayed" style={{ pointerEvents: 'none' }}>
          <svg width="220" height="130" viewBox="0 0 220 130">
            <line x1="0" y1="0" x2="0" y2="110" stroke="#DFE4DD" strokeWidth="1" opacity="0.3" />
            <line x1="0" y1="110" x2="200" y2="110" stroke="#DFE4DD" strokeWidth="1" opacity="0.3" />
            <circle cx="25" cy="75" r="7" fill="#588157" opacity="0.7" />
            <circle cx="60" cy="40" r="7" fill="#588157" opacity="0.7" />
            <circle cx="95" cy="90" r="7" fill="#588157" opacity="0.7" />
            <circle cx="130" cy="55" r="7" fill="#588157" opacity="0.7" />
            <circle cx="165" cy="80" r="7" fill="#588157" opacity="0.7" />
            <line x1="25" y1="75" x2="165" y2="80" stroke="#344E41" strokeWidth="2" strokeDasharray="5,5" opacity="0.4" />
          </svg>
        </div>
        
        {/* Math Formulas - Top Center */}
        <div className="absolute top-24 left-1/2 -translate-x-1/2 opacity-[0.25] animate-float" style={{ pointerEvents: 'none' }}>
          <svg width="200" height="80" viewBox="0 0 200 80">
            <text x="0" y="20" fontSize="28" fill="#344E41" fontWeight="bold" opacity="0.4">Σ</text>
            <text x="40" y="20" fontSize="24" fill="#588157" opacity="0.4">μ</text>
            <text x="75" y="20" fontSize="26" fill="#344E41" opacity="0.4">σ</text>
            <text x="110" y="20" fontSize="22" fill="#588157" opacity="0.4">π</text>
            <text x="145" y="20" fontSize="20" fill="#344E41" opacity="0.4">β</text>
            <text x="0" y="50" fontSize="16" fill="#344E41" opacity="0.35">μ = (Σx) / n</text>
            <text x="0" y="75" fontSize="16" fill="#588157" opacity="0.35">σ² = Σ(x-μ)² / n</text>
          </svg>
        </div>
        
        {/* Math Formulas - Bottom Center */}
        <div className="absolute bottom-32 left-1/2 -translate-x-1/2 opacity-[0.25] animate-float-delayed" style={{ pointerEvents: 'none' }}>
          <svg width="350" height="90" viewBox="0 0 350 90">
            <text x="0" y="20" fontSize="20" fill="#344E41" opacity="0.35">R² = 1 - (SS_res / SS_tot)</text>
            <text x="0" y="50" fontSize="18" fill="#588157" opacity="0.35">P(A|B) = P(B|A) × P(A) / P(B)</text>
            <text x="0" y="80" fontSize="22" fill="#344E41" opacity="0.4">χ²</text>
            <text x="35" y="80" fontSize="22" fill="#588157" opacity="0.4">α</text>
          </svg>
        </div>
        
        {/* Trend Chart 3 - Center Top */}
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 opacity-[0.25] animate-float" style={{ pointerEvents: 'none' }}>
          <svg width="200" height="100" viewBox="0 0 200 100">
            <line x1="0" y1="0" x2="0" y2="80" stroke="#DFE4DD" strokeWidth="1" opacity="0.3" />
            <line x1="0" y1="80" x2="180" y2="80" stroke="#DFE4DD" strokeWidth="1" opacity="0.3" />
            <polyline
              points="0,70 25,65 50,50 75,55 100,40 125,45 150,30 175,25"
              fill="none"
              stroke="#344E41"
              strokeWidth="3"
              opacity="0.7"
            />
            <circle cx="0" cy="70" r="4" fill="#344E41" opacity="0.8" />
            <circle cx="75" cy="55" r="4" fill="#344E41" opacity="0.8" />
            <circle cx="175" cy="25" r="4" fill="#344E41" opacity="0.8" />
          </svg>
        </div>
        
        {/* Bar Chart 3 - Center Bottom */}
        <div className="absolute bottom-1/3 left-1/2 -translate-x-1/2 opacity-[0.25] animate-float-delayed" style={{ pointerEvents: 'none' }}>
          <svg width="180" height="100" viewBox="0 0 180 100">
            <rect x="0" y="45" width="20" height="50" fill="#D4A373" rx="3" opacity="0.7" />
            <rect x="28" y="25" width="20" height="70" fill="#D4A373" rx="3" opacity="0.7" />
            <rect x="56" y="15" width="20" height="80" fill="#D4A373" rx="3" opacity="0.7" />
            <rect x="84" y="35" width="20" height="60" fill="#D4A373" rx="3" opacity="0.7" />
            <rect x="112" y="20" width="20" height="75" fill="#D4A373" rx="3" opacity="0.7" />
            <rect x="140" y="40" width="20" height="55" fill="#D4A373" rx="3" opacity="0.7" />
          </svg>
        </div>
        
        {/* Animated People Analytics Icons - Abstract People - More Visible */}
        <div className="absolute top-40 right-40 opacity-[0.15] animate-float">
          <svg width="120" height="120" viewBox="0 0 120 120">
            {/* Person 1 */}
            <circle cx="30" cy="30" r="12" fill="#588157" className="animate-pulse-slow" />
            <rect x="22" y="42" width="16" height="20" rx="8" fill="#588157" />
            {/* Person 2 */}
            <circle cx="60" cy="25" r="12" fill="#344E41" style={{ animationDelay: '0.3s' }} className="animate-pulse-slow" />
            <rect x="52" y="37" width="16" height="20" rx="8" fill="#344E41" />
            {/* Person 3 */}
            <circle cx="90" cy="30" r="12" fill="#588157" style={{ animationDelay: '0.6s' }} className="animate-pulse-slow" />
            <rect x="82" y="42" width="16" height="20" rx="8" fill="#588157" />
            {/* Connection lines */}
            <line x1="42" y1="30" x2="48" y2="25" stroke="#DFE4DD" strokeWidth="2" className="animate-pulse-slow" />
            <line x1="72" y1="25" x2="78" y2="30" stroke="#DFE4DD" strokeWidth="2" style={{ animationDelay: '0.5s' }} className="animate-pulse-slow" />
          </svg>
        </div>
        
        <div className="absolute bottom-60 left-60 opacity-[0.15] animate-float-delayed">
          <svg width="100" height="100" viewBox="0 0 100 100">
            {/* Team group */}
            <circle cx="25" cy="35" r="10" fill="#588157" className="animate-pulse-slow" />
            <rect x="18" y="45" width="14" height="18" rx="7" fill="#588157" />
            <circle cx="50" cy="30" r="12" fill="#344E41" style={{ animationDelay: '0.4s' }} className="animate-pulse-slow" />
            <rect x="41" y="42" width="18" height="20" rx="9" fill="#344E41" />
            <circle cx="75" cy="35" r="10" fill="#D4A373" style={{ animationDelay: '0.8s' }} className="animate-pulse-slow" />
            <rect x="68" y="45" width="14" height="18" rx="7" fill="#D4A373" />
          </svg>
        </div>
        
        {/* Mathematical/Analytics Elements - More Visible */}
        <div className="absolute top-1/4 left-1/4 opacity-[0.12]">
          <svg width="200" height="150" viewBox="0 0 200 150">
            {/* Statistics symbols */}
            <text x="10" y="30" fontFamily="Arial" fontSize="24" fill="#344E41" fontWeight="bold">Σ</text>
            <text x="50" y="30" fontFamily="Arial" fontSize="20" fill="#588157">μ</text>
            <text x="80" y="30" fontFamily="Arial" fontSize="22" fill="#344E41">σ</text>
            <text x="110" y="30" fontFamily="Arial" fontSize="18" fill="#588157">π</text>
            {/* Chart axis */}
            <line x1="20" y1="60" x2="180" y2="60" stroke="#344E41" strokeWidth="2" />
            <line x1="20" y1="60" x2="20" y2="20" stroke="#344E41" strokeWidth="2" />
            {/* Data points */}
            <circle cx="40" cy="50" r="3" fill="#588157" />
            <circle cx="70" cy="35" r="3" fill="#588157" />
            <circle cx="100" cy="45" r="3" fill="#588157" />
            <circle cx="130" cy="30" r="3" fill="#588157" />
            <circle cx="160" cy="40" r="3" fill="#588157" />
          </svg>
        </div>
        
        {/* More visible grid pattern overlay */}
        <div className="absolute inset-0 opacity-[0.04]" style={{
          backgroundImage: `linear-gradient(#344E41 1px, transparent 1px),
                           linear-gradient(90deg, #344E41 1px, transparent 1px)`,
          backgroundSize: '50px 50px'
        }}></div>
        
        {/* Animated Abstract geometric shapes for modern feel */}
        <div className="absolute top-20 right-20 w-32 h-32 border border-[#588157]/8 rounded-3xl rotate-12 opacity-30 animate-float"></div>
        <div className="absolute bottom-32 left-16 w-24 h-24 border border-[#D4A373]/8 rounded-2xl -rotate-12 opacity-30 animate-float-delayed"></div>
        <div className="absolute top-1/3 right-1/4 w-16 h-16 border border-[#344E41]/6 rounded-full opacity-30 animate-pulse-slow"></div>
        <div className="absolute top-1/2 left-20 w-20 h-20 border border-[#588157]/6 rounded-full opacity-20 animate-rotate-slow"></div>
        <div className="absolute bottom-1/4 right-1/3 w-28 h-28 border border-[#D4A373]/6 rounded-2xl opacity-25 animate-float" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 py-20">
        {/* Logo/Title Section */}
        <div className="text-center mb-16 animate-fade-in">
          <h1 className="text-6xl md:text-7xl font-bold mb-4 text-[#222] tracking-tight drop-shadow-sm">
            HR Analytics Platform
          </h1>
          <p className="text-xl md:text-2xl text-[#344E41] font-light mt-4">
            Powered by RAG & Semantic Caching
          </p>
          <p className="text-sm text-[#588157] mt-2 font-medium">
            Intelligent • Fast • Context-Aware
          </p>
        </div>

        {/* Quote Section */}
        <div className={`max-w-3xl mb-16 transition-opacity duration-500 ${fadeIn ? 'opacity-100' : 'opacity-0'}`}>
          <div className="bg-white/80 backdrop-blur-sm border border-[#DFE4DD] rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 mt-1">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-[#588157]/20 to-[#344E41]/20 flex items-center justify-center border border-[#588157]/30 shadow-sm">
                  <Sparkles className="w-6 h-6 text-[#588157]" />
                </div>
              </div>
              <div className="flex-1">
                <p className="text-xl md:text-2xl text-[#222] font-medium italic mb-4 leading-relaxed">
                  "{currentQuote.text}"
                </p>
                <p className="text-sm text-[#344E41] font-semibold">
                  — {currentQuote.author}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16 max-w-5xl w-full">
          <div className="bg-white/80 backdrop-blur-sm border border-[#DFE4DD] rounded-xl p-6 shadow-lg hover:shadow-xl hover:border-[#588157]/40 transition-all duration-300 hover:scale-105 hover:-translate-y-1">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-[#588157]/15 to-[#344E41]/10 flex items-center justify-center mb-4 border border-[#588157]/30 shadow-sm">
              <Database className="w-6 h-6 text-[#588157]" />
            </div>
            <h3 className="text-lg font-semibold text-[#222] mb-2">RAG-Enhanced</h3>
            <p className="text-sm text-[#344E41]">
              Understands custom HR terms and complex formulas with Retrieval-Augmented Generation
            </p>
          </div>

          <div className="bg-white/80 backdrop-blur-sm border border-[#DFE4DD] rounded-xl p-6 shadow-lg hover:shadow-xl hover:border-[#D4A373]/40 transition-all duration-300 hover:scale-105 hover:-translate-y-1">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-[#D4A373]/15 to-[#C49463]/10 flex items-center justify-center mb-4 border border-[#D4A373]/30 shadow-sm">
              <Zap className="w-6 h-6 text-[#D4A373]" />
            </div>
            <h3 className="text-lg font-semibold text-[#222] mb-2">Semantic Cache</h3>
            <p className="text-sm text-[#344E41]">
              Lightning-fast responses with intelligent caching of similar queries
            </p>
          </div>

          <div className="bg-white/80 backdrop-blur-sm border border-[#DFE4DD] rounded-xl p-6 shadow-lg hover:shadow-xl hover:border-[#588157]/40 transition-all duration-300 hover:scale-105 hover:-translate-y-1">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-[#588157]/15 to-[#344E41]/10 flex items-center justify-center mb-4 border border-[#588157]/30 shadow-sm">
              <TrendingUp className="w-6 h-6 text-[#588157]" />
            </div>
            <h3 className="text-lg font-semibold text-[#222] mb-2">Smart Insights</h3>
            <p className="text-sm text-[#344E41]">
              AI-powered analytics with visualizations and actionable recommendations
            </p>
          </div>
        </div>

        {/* CTA Button */}
        <button
          onClick={onEnterChat}
          className="group relative px-12 py-5 bg-gradient-to-r from-[#344E41] to-[#588157] rounded-2xl font-semibold text-lg text-white shadow-lg hover:shadow-xl hover:shadow-[#588157]/30 transition-all duration-300 hover:scale-105 transform"
        >
          <span className="relative z-10 flex items-center gap-3">
            <Sparkles className="w-5 h-5 transition-transform group-hover:rotate-12" />
            <span>Start Analyzing with AI</span>
            <svg className="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </span>
        </button>
      </div>
    </div>
  );
};

export default LandingPage;

