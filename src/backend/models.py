"""
Data models for the YouTube Downloader backend
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum

class DownloadStatus(Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class VideoFormat(Enum):
    MP4 = "mp4"
    MP3 = "mp3"
    WEBM = "webm"

class VideoQuality(Enum):
    QUALITY_1080P = "1080p"
    QUALITY_720P = "720p"
    QUALITY_480P = "480p"
    QUALITY_360P = "360p"

@dataclass
class VideoInfo:
    """Video information data model"""
    id: str
    title: str
    thumbnail: Optional[str]
    duration: str
    author: str
    views: str
    upload_date: str
    description: str
    url: str
    formats: List[Dict[str, Any]]

@dataclass
class DownloadRequest:
    """Download request data model"""
    url: str
    format: VideoFormat
    quality: Optional[VideoQuality]
    download_id: str

@dataclass
class DownloadProgress:
    """Download progress data model"""
    download_id: str
    status: DownloadStatus
    progress: float
    speed: str
    eta: str
    filename: Optional[str] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

@dataclass
class ApiResponse:
    """Standard API response model"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None

class DownloadManager:
    """Manages download operations and progress tracking"""
    
    def __init__(self):
        self.downloads: Dict[str, DownloadProgress] = {}
    
    def create_download(self, download_id: str) -> DownloadProgress:
        """Create a new download progress entry"""
        progress = DownloadProgress(
            download_id=download_id,
            status=DownloadStatus.PENDING,
            progress=0.0,
            speed="0 MB/s",
            eta="Calculating...",
            started_at=datetime.now()
        )
        self.downloads[download_id] = progress
        return progress
    
    def update_progress(self, download_id: str, **kwargs) -> Optional[DownloadProgress]:
        """Update download progress"""
        if download_id in self.downloads:
            progress = self.downloads[download_id]
            for key, value in kwargs.items():
                if hasattr(progress, key):
                    setattr(progress, key, value)
            return progress
        return None
    
    def get_progress(self, download_id: str) -> Optional[DownloadProgress]:
        """Get download progress"""
        return self.downloads.get(download_id)
    
    def complete_download(self, download_id: str, filename: str):
        """Mark download as completed"""
        if download_id in self.downloads:
            self.downloads[download_id].status = DownloadStatus.COMPLETED
            self.downloads[download_id].progress = 100.0
            self.downloads[download_id].filename = filename
            self.downloads[download_id].completed_at = datetime.now()
            self.downloads[download_id].speed = "0 MB/s"
            self.downloads[download_id].eta = "Complete"
    
    def error_download(self, download_id: str, error: str):
        """Mark download as error"""
        if download_id in self.downloads:
            self.downloads[download_id].status = DownloadStatus.ERROR
            self.downloads[download_id].error = error
            self.downloads[download_id].speed = "0 MB/s"
            self.downloads[download_id].eta = "Error"
    
    def remove_download(self, download_id: str):
        """Remove download from tracking"""
        if download_id in self.downloads:
            del self.downloads[download_id]
    
    def get_all_downloads(self) -> List[DownloadProgress]:
        """Get all downloads"""
        return list(self.downloads.values())
    
    def cleanup_completed(self, older_than_hours: int = 24):
        """Clean up completed downloads older than specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        to_remove = []
        
        for download_id, progress in self.downloads.items():
            if (progress.status == DownloadStatus.COMPLETED and 
                progress.completed_at and 
                progress.completed_at < cutoff_time):
                to_remove.append(download_id)
        
        for download_id in to_remove:
            self.remove_download(download_id)

# Global download manager instance
download_manager = DownloadManager()