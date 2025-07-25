export interface VideoInfo {
  id: string;
  title: string;
  thumbnail: string;
  duration: string;
  author: string;
  views: string;
  uploadDate: string;
  description: string;
  url: string;
}

export interface DownloadItem {
  id: string;
  video: VideoInfo;
  format: string;
  quality: string;
  status: 'pending' | 'downloading' | 'completed' | 'error' | 'paused';
  progress: number;
  downloadSpeed: string;
  estimatedTime: string;
}

export interface QualityOption {
  value: string;
  label: string;
  size?: string;
}

export interface FormatOption {
  value: string;
  label: string;
  icon: string;
}