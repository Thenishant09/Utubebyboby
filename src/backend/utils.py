"""
Utility functions for the YouTube Downloader backend
"""

import os
import time
import shutil
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timedelta
from contextlib import suppress

def cleanup_old_downloads(download_folder: Path, hours: int = 24) -> None:
    """Clean up download folders older than specified hours"""
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        for folder in download_folder.iterdir():
            if folder.is_dir():
                folder_time = datetime.fromtimestamp(folder.stat().st_mtime)
                if folder_time < cutoff_time:
                    with suppress(Exception):
                        shutil.rmtree(os.fspath(folder))
                        print(f"Cleaned up old download folder: {folder}")
    except Exception as e:
        print(f"Error during cleanup: {e}")

def get_file_size_mb(file_path: Path) -> float:
    """Get file size in megabytes"""
    try:
        return file_path.stat().st_size / (1024 * 1024)
    except Exception:
        return 0.0

def validate_youtube_url(url: str) -> bool:
    """Validate if the URL is a valid YouTube URL"""
    youtube_domains = [
        'youtube.com',
        'youtu.be',
        'www.youtube.com',
        'm.youtube.com'
    ]
    return any(domain in url.lower() for domain in youtube_domains)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system storage"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    if len(filename) > 200:
        filename = filename[:200]
    return filename.strip()

def format_bytes(bytes_value: int) -> str:
    """Format bytes into human readable format"""
    if bytes_value == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    value = float(bytes_value)
    while value >= 1024 and i < len(size_names) - 1:
        value /= 1024.0
        i += 1
    return f"{value:.1f} {size_names[i]}"

def get_available_formats(info_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract available formats from yt-dlp info dictionary"""
    formats = []
    if 'formats' in info_dict:
        for fmt in info_dict['formats']:
            if fmt.get('vcodec') != 'none' or fmt.get('acodec') != 'none':
                format_info = {
                    'format_id': fmt.get('format_id'),
                    'ext': fmt.get('ext'),
                    'quality': fmt.get('quality'),
                    'filesize': fmt.get('filesize'),
                    'vcodec': fmt.get('vcodec'),
                    'acodec': fmt.get('acodec'),
                    'height': fmt.get('height'),
                    'width': fmt.get('width'),
                    'fps': fmt.get('fps'),
                    'abr': fmt.get('abr'),
                    'vbr': fmt.get('vbr')
                }
                formats.append(format_info)
    return formats

def estimate_download_time(file_size_bytes: int, speed_mbps: float = 10.0) -> str:
    """Estimate download time based on file size and connection speed"""
    if file_size_bytes <= 0 or speed_mbps <= 0:
        return "Unknown"
    speed_bps = (speed_mbps * 1024 * 1024) / 8
    time_seconds = file_size_bytes / speed_bps
    if time_seconds < 60:
        return f"{int(time_seconds)}s"
    elif time_seconds < 3600:
        minutes = int(time_seconds / 60)
        seconds = int(time_seconds % 60)
        return f"{minutes}m {seconds}s"
    else:
        hours = int(time_seconds / 3600)
        minutes = int((time_seconds % 3600) / 60)
        return f"{hours}h {minutes}m"