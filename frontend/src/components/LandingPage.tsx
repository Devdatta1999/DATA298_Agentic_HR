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
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950/30 to-slate-950 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Floating orbs */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-3xl animate-pulse delay-2000"></div>
        
        {/* Grid pattern overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 py-20">
        {/* Logo/Title Section */}
        <div className="text-center mb-16 animate-fade-in">
          <h1 className="text-6xl md:text-7xl font-bold mb-4 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent tracking-tight">
            HR Analytics Platform
          </h1>
          <p className="text-xl md:text-2xl text-slate-400 font-light mt-4">
            Transform HR Data into Strategic Insights
          </p>
        </div>

        {/* Quote Section */}
        <div className="max-w-3xl w-full mb-16">
          <div className={`bg-gradient-to-br from-slate-800/80 to-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-3xl p-8 md:p-12 shadow-2xl transition-opacity duration-500 ${fadeIn ? 'opacity-100' : 'opacity-0'}`}>
            <div className="flex items-start gap-4">
              <div className="text-4xl text-purple-400 mt-2">"</div>
              <div className="flex-1">
                <p className="text-2xl md:text-3xl font-light text-slate-200 leading-relaxed mb-6">
                  {currentQuote.text}
                </p>
                <p className="text-lg text-slate-400 font-medium text-right">
                  — {currentQuote.author}
                </p>
              </div>
              <div className="text-4xl text-purple-400 mt-2 rotate-180">"</div>
            </div>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl w-full mb-16">
          <div className="bg-gradient-to-br from-purple-900/20 to-blue-900/20 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6 hover:border-purple-500/40 transition-all duration-300 hover:scale-105">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-semibold text-slate-200 mb-2">Smart Analytics</h3>
            <p className="text-slate-400 text-sm">AI-powered insights from your HR data</p>
          </div>
          
          <div className="bg-gradient-to-br from-blue-900/20 to-cyan-900/20 backdrop-blur-xl border border-blue-500/20 rounded-2xl p-6 hover:border-blue-500/40 transition-all duration-300 hover:scale-105">
            <div className="text-4xl mb-4">💬</div>
            <h3 className="text-xl font-semibold text-slate-200 mb-2">Natural Language</h3>
            <p className="text-slate-400 text-sm">Ask questions in plain English</p>
          </div>
          
          <div className="bg-gradient-to-br from-cyan-900/20 to-purple-900/20 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6 hover:border-cyan-500/40 transition-all duration-300 hover:scale-105">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-semibold text-slate-200 mb-2">Real-time Insights</h3>
            <p className="text-slate-400 text-sm">Get instant answers and visualizations</p>
          </div>
        </div>

        {/* CTA Button */}
        <button
          onClick={onEnterChat}
          className="group relative px-12 py-5 bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 rounded-2xl font-semibold text-lg text-white shadow-2xl hover:shadow-purple-500/50 transition-all duration-300 hover:scale-105 transform overflow-hidden"
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
          <div className="absolute inset-0 bg-gradient-to-r from-purple-700 via-blue-700 to-cyan-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </button>

        {/* Decorative Elements */}
        <div className="mt-16 flex items-center gap-2 text-slate-500 text-sm">
          <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></div>
          <span>Powered by AI</span>
          <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse delay-300"></div>
        </div>
      </div>

      {/* Bottom Wave Decoration */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-slate-950 to-transparent"></div>
    </div>
  );
};

export default LandingPage;

