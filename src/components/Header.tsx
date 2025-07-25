import React from 'react';
import { Download, Youtube, Star, Users } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="bg-black/30 backdrop-blur-md border-b border-white/10 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-r from-red-600 to-red-500 p-2 rounded-xl shadow-lg">
              <Youtube className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">YouTube Downloader Pro</h1>
              <p className="text-gray-300 text-sm">Fast, Free & Secure Downloads</p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-yellow-400">
              <Star className="w-4 h-4 fill-current" />
              <span className="text-sm font-medium">4.9/5</span>
            </div>
            <div className="flex items-center space-x-2 text-blue-400">
              <Users className="w-4 h-4" />
              <span className="text-sm font-medium">2M+ Users</span>
            </div>
            <div className="flex items-center space-x-2 text-green-400">
              <Download className="w-4 h-4" />
              <span className="text-sm font-medium">Free & Secure</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};