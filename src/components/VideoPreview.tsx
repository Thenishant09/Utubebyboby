import React, { useState } from 'react';
import { Download, Play, Eye, Clock, User, Calendar, FileText } from 'lucide-react';
import { VideoInfo, QualityOption, FormatOption } from '../Types';

interface VideoPreviewProps {
  video: VideoInfo;
  onDownload: (video: VideoInfo, format: string, quality: string) => void;
}

export const VideoPreview: React.FC<VideoPreviewProps> = ({ video, onDownload }) => {
  const [selectedFormat, setSelectedFormat] = useState('mp4');
  const [selectedQuality, setSelectedQuality] = useState('720p');

  const qualities: QualityOption[] = [
    { value: '1080p', label: '1080p HD', size: '~150MB' },
    { value: '720p', label: '720p HD', size: '~80MB' },
    { value: '480p', label: '480p SD', size: '~40MB' },
    { value: '360p', label: '360p', size: '~25MB' }
  ];

  const formats: FormatOption[] = [
    { value: 'mp4', label: 'MP4 Video', icon: '🎥' },
    { value: 'mp3', label: 'MP3 Audio', icon: '🎵' },
    { value: 'webm', label: 'WebM Video', icon: '📹' }
  ];

  const handleDownload = () => {
    onDownload(video, selectedFormat, selectedQuality);
  };

  return (
    <div className="glass-card rounded-3xl p-8 mb-8 animate-fade-in">
      <div className="grid lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="relative group">
            <img
              src={video.thumbnail}
              alt={video.title}
              className="w-full aspect-video object-cover rounded-2xl shadow-2xl"
            />
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-all duration-300 rounded-2xl flex items-center justify-center">
              <div className="bg-white/20 backdrop-blur-sm rounded-full p-4">
                <Play className="w-12 h-12 text-white" />
              </div>
            </div>
            <div className="absolute bottom-4 right-4 bg-black/80 text-white px-3 py-1 rounded-lg font-medium">
              {video.duration}
            </div>
          </div>
          
          <div className="space-y-4">
            <h3 className="text-2xl font-bold text-white leading-tight">{video.title}</h3>
            
            <div className="grid grid-cols-2 gap-4 text-gray-300">
              <div className="flex items-center space-x-2">
                <User className="w-4 h-4 text-blue-400" />
                <span className="text-sm">{video.author}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Eye className="w-4 h-4 text-green-400" />
                <span className="text-sm">{video.views}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-purple-400" />
                <span className="text-sm">{video.duration}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Calendar className="w-4 h-4 text-pink-400" />
                <span className="text-sm">{video.uploadDate}</span>
              </div>
            </div>
            
            <div className="bg-white/5 rounded-xl p-4 border border-white/10">
              <div className="flex items-start space-x-2">
                <FileText className="w-4 h-4 text-gray-400 mt-1 flex-shrink-0" />
                <p className="text-gray-300 text-sm leading-relaxed">{video.description}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-2xl p-6 border border-purple-500/20">
            <h4 className="text-xl font-bold text-white mb-6 flex items-center space-x-2">
              <Download className="w-6 h-6 text-purple-400" />
              <span>Download Options</span>
            </h4>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-300 mb-3">
                  Choose Format
                </label>
                <div className="grid grid-cols-1 gap-3">
                  {formats.map((format) => (
                    <label
                      key={format.value}
                      className={`flex items-center space-x-3 p-4 rounded-xl border-2 cursor-pointer transition-all duration-200 ${
                        selectedFormat === format.value
                          ? 'border-purple-500 bg-purple-500/10'
                          : 'border-white/20 bg-white/5 hover:border-white/30'
                      }`}
                    >
                      <input
                        type="radio"
                        name="format"
                        value={format.value}
                        checked={selectedFormat === format.value}
                        onChange={(e) => setSelectedFormat(e.target.value)}
                        className="sr-only"
                      />
                      <span className="text-2xl">{format.icon}</span>
                      <span className="text-white font-medium">{format.label}</span>
                    </label>
                  ))}
                </div>
              </div>
              
              {selectedFormat !== 'mp3' && (
                <div>
                  <label className="block text-sm font-semibold text-gray-300 mb-3">
                    Select Quality
                  </label>
                  <div className="space-y-2">
                    {qualities.map((quality) => (
                      <label
                        key={quality.value}
                        className={`flex items-center justify-between p-3 rounded-xl border cursor-pointer transition-all duration-200 ${
                          selectedQuality === quality.value
                            ? 'border-pink-500 bg-pink-500/10'
                            : 'border-white/20 bg-white/5 hover:border-white/30'
                        }`}
                      >
                        <div className="flex items-center space-x-3">
                          <input
                            type="radio"
                            name="quality"
                            value={quality.value}
                            checked={selectedQuality === quality.value}
                            onChange={(e) => setSelectedQuality(e.target.value)}
                            className="sr-only"
                          />
                          <span className="text-white font-medium">{quality.label}</span>
                        </div>
                        <span className="text-gray-400 text-sm">{quality.size}</span>
                      </label>
                    ))}
                  </div>
                </div>
              )}
              
              <button
                onClick={handleDownload}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-bold py-4 px-6 rounded-2xl transition-all duration-300 transform hover:scale-[1.02] flex items-center justify-center space-x-3 shadow-2xl"
              >
                <Download className="w-6 h-6" />
                <span>Download {selectedFormat.toUpperCase()}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};