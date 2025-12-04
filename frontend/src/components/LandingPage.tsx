import React, { useState, useEffect } from 'react';

interface LandingPageProps {
  onEnterChat: () => void;
}

const HR_QUOTES = [
  {
    text: "People are not your most important asset. The right people are.",
    author: "Jim Collins"
  },
  {
    text: "The way to get started is to quit talking and begin doing.",
    author: "Walt Disney"
  },
  {
    text: "Your employees are your company's real competitive advantage.",
    author: "Richard Branson"
  },
  {
    text: "Take care of your employees and they'll take care of your business.",
    author: "Richard Branson"
  },
  {
    text: "The best way to find out if you can trust somebody is to trust them.",
    author: "Ernest Hemingway"
  },
  {
    text: "Innovation distinguishes between a leader and a follower.",
    author: "Steve Jobs"
  }
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
    <div className="min-h-screen relative overflow-hidden" style={{ backgroundColor: '#0A0F1F' }}>
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Floating orbs */}
        <div className="absolute top-20 left-10 w-72 h-72 rounded-full blur-3xl animate-pulse" style={{ backgroundColor: 'rgba(249, 162, 63, 0.1)' }}></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 rounded-full blur-3xl animate-pulse delay-1000" style={{ backgroundColor: 'rgba(110, 193, 228, 0.08)' }}></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full blur-3xl animate-pulse delay-2000" style={{ backgroundColor: 'rgba(249, 162, 63, 0.05)' }}></div>
        
        {/* Grid pattern overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808008_1px,transparent_1px),linear-gradient(to_bottom,#80808008_1px,transparent_1px)] bg-[size:24px_24px]"></div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 py-20">
        {/* Logo/Title Section */}
        <div className="text-center mb-16 animate-fade-in">
          <h1 className="text-6xl md:text-7xl font-bold mb-4 tracking-tight" style={{ 
            background: 'linear-gradient(to right, #F9A23F, #6EC1E4)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            HR Analytics Platform
          </h1>
          <p className="text-xl md:text-2xl font-light mt-4" style={{ color: '#B6C2CC' }}>
            Transform HR Data into Strategic Insights
          </p>
        </div>

        {/* Quote Section */}
        <div className="max-w-3xl w-full mb-16">
          <div className={`backdrop-blur-xl rounded-3xl p-8 md:p-12 shadow-2xl transition-opacity duration-500 ${fadeIn ? 'opacity-100' : 'opacity-0'}`} style={{ 
            backgroundColor: '#11182A',
            border: '1px solid rgba(30, 42, 64, 0.5)'
          }}>
            <div className="flex items-start gap-4">
              <div className="text-4xl mt-2" style={{ color: '#F9A23F' }}>"</div>
              <div className="flex-1">
                <p className="text-2xl md:text-3xl font-light leading-relaxed mb-6" style={{ color: '#FFFFFF' }}>
                  {currentQuote.text}
                </p>
                <p className="text-lg font-medium text-right" style={{ color: '#B6C2CC' }}>
                  — {currentQuote.author}
                </p>
              </div>
              <div className="text-4xl mt-2 rotate-180" style={{ color: '#F9A23F' }}>"</div>
            </div>
          </div>
        </div>

        {/* Feature Cards - Unified Navy Gradients */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl w-full mb-16">
          <div className="backdrop-blur-xl rounded-2xl p-6 transition-all duration-300 hover:scale-105 hover:shadow-xl" style={{ 
            background: 'linear-gradient(135deg, #11182A 0%, #1E2A40 100%)',
            border: '1px solid rgba(30, 42, 64, 0.6)'
          }}>
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-semibold mb-2" style={{ color: '#FFFFFF' }}>Smart Analytics</h3>
            <p className="text-sm" style={{ color: '#B6C2CC' }}>AI-powered insights from your HR data</p>
          </div>
          
          <div className="backdrop-blur-xl rounded-2xl p-6 transition-all duration-300 hover:scale-105 hover:shadow-xl" style={{ 
            background: 'linear-gradient(135deg, #11182A 0%, #1E2A40 100%)',
            border: '1px solid rgba(30, 42, 64, 0.6)'
          }}>
            <div className="text-4xl mb-4">💬</div>
            <h3 className="text-xl font-semibold mb-2" style={{ color: '#FFFFFF' }}>Natural Language</h3>
            <p className="text-sm" style={{ color: '#B6C2CC' }}>Ask questions in plain English</p>
          </div>
          
          <div className="backdrop-blur-xl rounded-2xl p-6 transition-all duration-300 hover:scale-105 hover:shadow-xl" style={{ 
            background: 'linear-gradient(135deg, #11182A 0%, #1E2A40 100%)',
            border: '1px solid rgba(30, 42, 64, 0.6)'
          }}>
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold mb-2" style={{ color: '#FFFFFF' }}>Real-time Insights</h3>
            <p className="text-sm" style={{ color: '#B6C2CC' }}>Get instant answers and visualizations</p>
          </div>
        </div>

        {/* CTA Button - Gold */}
        <button
          onClick={onEnterChat}
          className="group relative px-12 py-5 rounded-2xl font-semibold text-lg shadow-2xl transition-all duration-300 hover:scale-105 transform overflow-hidden"
          style={{ 
            background: '#F9A23F',
            color: '#0A0F1F'
          }}
        >
          <span className="relative z-10 flex items-center gap-3">
            <span>Start Analyzing</span>
            <svg 
              className="w-5 h-5 transition-transform group-hover:translate-x-1" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </span>
          <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" style={{ backgroundColor: 'rgba(249, 162, 63, 0.8)' }}></div>
        </button>

        {/* Decorative Elements */}
        <div className="mt-16 flex items-center gap-2 text-sm" style={{ color: '#B6C2CC' }}>
          <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: '#F9A23F' }}></div>
          <span>Powered by AI</span>
          <div className="w-2 h-2 rounded-full animate-pulse delay-300" style={{ backgroundColor: '#6EC1E4' }}></div>
        </div>
      </div>

      {/* Bottom Wave Decoration */}
      <div className="absolute bottom-0 left-0 right-0 h-32" style={{ background: 'linear-gradient(to top, #0A0F1F, transparent)' }}></div>
    </div>
  );
};

export default LandingPage;

