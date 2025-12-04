import React, { useState, useEffect } from 'react';
import { Brain, Zap, Database, TrendingUp, Sparkles } from 'lucide-react';

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
    <div className="min-h-screen bg-gradient-to-br from-emerald-950 via-teal-950/40 to-slate-950 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-20 left-10 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-cyan-500/5 rounded-full blur-3xl"></div>
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-6 py-20">
        {/* Logo/Title Section */}
        <div className="text-center mb-16 animate-fade-in">
          <div className="flex items-center justify-center gap-3 mb-6">
            <div className="p-4 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 rounded-2xl border border-emerald-500/30 backdrop-blur-sm">
              <Brain className="w-12 h-12 text-emerald-400" />
            </div>
            <div className="p-4 bg-gradient-to-br from-teal-500/20 to-cyan-500/20 rounded-2xl border border-teal-500/30 backdrop-blur-sm">
              <Database className="w-12 h-12 text-teal-400" />
            </div>
          </div>
          <h1 className="text-6xl md:text-7xl font-bold mb-4 bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 bg-clip-text text-transparent tracking-tight">
            HR Analytics AI
          </h1>
          <p className="text-xl md:text-2xl text-slate-300 font-light mt-4">
            Powered by RAG & Semantic Caching
          </p>
          <p className="text-sm text-emerald-400/70 mt-2 font-medium">
            Intelligent • Fast • Context-Aware
          </p>
        </div>

        {/* Quote Section */}
        <div className={`max-w-3xl mb-16 transition-opacity duration-500 ${fadeIn ? 'opacity-100' : 'opacity-0'}`}>
          <div className="bg-gradient-to-br from-emerald-900/30 to-teal-900/30 border border-emerald-500/20 rounded-2xl p-8 backdrop-blur-sm shadow-2xl">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 mt-1">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-emerald-500/20 to-teal-500/20 flex items-center justify-center border border-emerald-500/30">
                  <Sparkles className="w-6 h-6 text-emerald-400" />
                </div>
              </div>
              <div className="flex-1">
                <p className="text-xl md:text-2xl text-slate-200 font-medium italic mb-4 leading-relaxed">
                  "{currentQuote.text}"
                </p>
                <p className="text-sm text-emerald-400/80 font-semibold">
                  — {currentQuote.author}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16 max-w-5xl w-full">
          <div className="bg-gradient-to-br from-emerald-900/40 to-emerald-800/20 border border-emerald-500/30 rounded-xl p-6 backdrop-blur-sm hover:border-emerald-400/50 transition-all duration-300 hover:scale-105">
            <div className="w-12 h-12 rounded-lg bg-emerald-500/20 flex items-center justify-center mb-4 border border-emerald-500/30">
              <Database className="w-6 h-6 text-emerald-400" />
            </div>
            <h3 className="text-lg font-semibold text-emerald-300 mb-2">RAG-Enhanced</h3>
            <p className="text-sm text-slate-400">
              Understands custom HR terms and complex formulas with Retrieval-Augmented Generation
            </p>
          </div>

          <div className="bg-gradient-to-br from-teal-900/40 to-teal-800/20 border border-teal-500/30 rounded-xl p-6 backdrop-blur-sm hover:border-teal-400/50 transition-all duration-300 hover:scale-105">
            <div className="w-12 h-12 rounded-lg bg-teal-500/20 flex items-center justify-center mb-4 border border-teal-500/30">
              <Zap className="w-6 h-6 text-teal-400" />
            </div>
            <h3 className="text-lg font-semibold text-teal-300 mb-2">Semantic Cache</h3>
            <p className="text-sm text-slate-400">
              Lightning-fast responses with intelligent caching of similar queries
            </p>
          </div>

          <div className="bg-gradient-to-br from-cyan-900/40 to-cyan-800/20 border border-cyan-500/30 rounded-xl p-6 backdrop-blur-sm hover:border-cyan-400/50 transition-all duration-300 hover:scale-105">
            <div className="w-12 h-12 rounded-lg bg-cyan-500/20 flex items-center justify-center mb-4 border border-cyan-500/30">
              <TrendingUp className="w-6 h-6 text-cyan-400" />
            </div>
            <h3 className="text-lg font-semibold text-cyan-300 mb-2">Smart Insights</h3>
            <p className="text-sm text-slate-400">
              AI-powered analytics with visualizations and actionable recommendations
            </p>
          </div>
        </div>

        {/* CTA Button */}
        <button
          onClick={onEnterChat}
          className="group relative px-12 py-5 bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 rounded-2xl font-semibold text-lg text-white shadow-2xl hover:shadow-emerald-500/50 transition-all duration-300 hover:scale-105 transform overflow-hidden"
        >
          <span className="relative z-10 flex items-center gap-3">
            <Sparkles className="w-5 h-5 transition-transform group-hover:rotate-12" />
            <span>Start Analyzing with AI</span>
            <svg className="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </span>
          <div className="absolute inset-0 bg-gradient-to-r from-emerald-700 via-teal-700 to-cyan-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </button>

        {/* Decorative Elements */}
        <div className="absolute bottom-10 left-10 w-2 h-2 bg-emerald-400 rounded-full animate-ping"></div>
        <div className="absolute top-20 right-20 w-3 h-3 bg-teal-400 rounded-full animate-pulse"></div>
        <div className="absolute bottom-32 right-32 w-2 h-2 bg-cyan-400 rounded-full animate-ping delay-1000"></div>
      </div>

      {/* Bottom Wave Decoration */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-slate-950 to-transparent"></div>
    </div>
  );
};

export default LandingPage;

