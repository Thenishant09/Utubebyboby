import React from 'react';
import { Sparkles, Zap, Shield } from 'lucide-react';

export const Hero: React.FC = () => {
  return (
    <section className="text-center py-12 mb-8">
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-pink-600/20 blur-3xl rounded-full"></div>
        <div className="relative">
          <h2 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Download YouTube Videos
            <span className="gradient-text block">In Seconds</span>
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
            The fastest and most reliable YouTube video downloader. 
            Support for all formats and qualities, completely free and secure.
          </p>
          
          <div className="flex flex-wrap justify-center gap-6 text-sm">
            <div className="flex items-center space-x-2 text-purple-300">
              <Zap className="w-5 h-5" />
              <span>Lightning Fast</span>
            </div>
            <div className="flex items-center space-x-2 text-pink-300">
              <Sparkles className="w-5 h-5" />
              <span>High Quality</span>
            </div>
            <div className="flex items-center space-x-2 text-green-300">
              <Shield className="w-5 h-5" />
              <span>100% Secure</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};