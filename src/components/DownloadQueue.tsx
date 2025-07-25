import React from 'react';
import { Download, CheckCircle, AlertCircle, X, Loader, Pause, Trash2 } from 'lucide-react';
import { DownloadItem } from '../Types';

interface DownloadQueueProps {
  items: DownloadItem[];
  onRemove: (id: string) => void;
  onClearCompleted: () => void;
}

export const DownloadQueue: React.FC<DownloadQueueProps> = ({ items, onRemove, onClearCompleted }) => {
  const getStatusIcon = (status: DownloadItem['status']) => {
    switch (status) {
      case 'pending':
        return <Download className="w-5 h-5 text-yellow-400" />;
      case 'downloading':
        return <Loader className="w-5 h-5 text-blue-400 animate-spin" />;
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-400" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-400" />;
      case 'paused':
        return <Pause className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusText = (status: DownloadItem['status']) => {
    switch (status) {
      case 'pending':
        return 'Pending';
      case 'downloading':
        return 'Downloading';
      case 'completed':
        return 'Completed';
      case 'error':
        return 'Error';
      case 'paused':
        return 'Paused';
    }
  };

  const getStatusColor = (status: DownloadItem['status']) => {
    switch (status) {
      case 'pending':
        return 'text-yellow-400';
      case 'downloading':
        return 'text-blue-400';
      case 'completed':
        return 'text-green-400';
      case 'error':
        return 'text-red-400';
      case 'paused':
        return 'text-gray-400';
    }
  };

  const completedItems = items.filter(item => item.status === 'completed');

  return (
    <div className="glass-card rounded-3xl p-8 mb-8">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold text-white flex items-center space-x-3">
          <Download className="w-7 h-7 text-purple-400" />
          <span>Download Queue</span>
          <span className="bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full text-sm font-medium">
            {items.length}
          </span>
        </h3>
        
        {completedItems.length > 0 && (
          <button
            onClick={onClearCompleted}
            className="flex items-center space-x-2 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-300 hover:text-red-200 rounded-xl transition-all duration-200 border border-red-500/30"
          >
            <Trash2 className="w-4 h-4" />
            <span className="text-sm font-medium">Clear Completed</span>
          </button>
        )}
      </div>
      
      <div className="space-y-4">
        {items.map((item) => (
          <div
            key={item.id}
            className="bg-white/5 rounded-2xl p-6 border border-white/10 hover:border-white/20 transition-all duration-200"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-start space-x-4 flex-1 min-w-0">
                <img
                  src={item.video.thumbnail}
                  alt={item.video.title}
                  className="w-20 h-12 object-cover rounded-lg flex-shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <h4 className="text-white font-semibold truncate mb-1">
                    {item.video.title}
                  </h4>
                  <div className="flex items-center space-x-4 text-sm text-gray-400">
                    <span>{item.format.toUpperCase()}</span>
                    {item.format !== 'mp3' && <span>{item.quality}</span>}
                    <span>{item.video.author}</span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center space-x-4">
                <div className="text-right">
                  <div className={`flex items-center space-x-2 ${getStatusColor(item.status)}`}>
                    {getStatusIcon(item.status)}
                    <span className="text-sm font-medium">
                      {getStatusText(item.status)}
                    </span>
                  </div>
                  {item.status === 'downloading' && (
                    <div className="text-xs text-gray-400 mt-1">
                      <div>{item.downloadSpeed}</div>
                      <div>{item.estimatedTime}</div>
                    </div>
                  )}
                </div>
                
                <button
                  onClick={() => onRemove(item.id)}
                  className="text-gray-400 hover:text-red-400 transition-colors duration-200 p-2 hover:bg-red-500/10 rounded-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>
            
            {item.status === 'downloading' && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Progress</span>
                  <span className="text-white font-medium">{Math.round(item.progress)}%</span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-500 relative overflow-hidden"
                    style={{ width: `${item.progress}%` }}
                  >
                    <div className="absolute inset-0 bg-white/20 animate-pulse"></div>
                  </div>
                </div>
              </div>
            )}
            
            {item.status === 'completed' && (
              <div className="bg-green-500/10 border border-green-500/20 rounded-xl p-3 mt-3">
                <div className="flex items-center justify-between">
                  <span className="text-green-300 text-sm font-medium">Download completed successfully!</span>
                  <button className="text-green-400 hover:text-green-300 text-sm font-medium hover:underline">
                    Open File
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};