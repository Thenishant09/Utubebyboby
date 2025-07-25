"""
Configuration settings for the YouTube Downloader backend
"""

import os
from pathlib import Path

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Download settings
    DOWNLOAD_FOLDER = Path(os.environ.get('DOWNLOAD_FOLDER', 'downloads'))
    MAX_DOWNLOAD_SIZE = int(os.environ.get('MAX_DOWNLOAD_SIZE', 1024 * 1024 * 1024))  # 1GB default
    ALLOWED_FORMATS = ['mp4', 'mp3', 'webm']
    ALLOWED_QUALITIES = ['1080p', '720p', '480p', '360p']
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 10))
    
    # Cleanup settings
    CLEANUP_AFTER_HOURS = int(os.environ.get('CLEANUP_AFTER_HOURS', 24))
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}