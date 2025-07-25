#!/usr/bin/env python3
"""
Production runner for the YouTube Downloader backend
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app import app
from config import config
from utils import cleanup_old_downloads
import threading
import time

def cleanup_worker():
    """Background worker to clean up old downloads"""
    while True:
        try:
            cleanup_old_downloads(
                download_folder=Path("downloads"),
                hours=24
            )
            # Sleep for 1 hour before next cleanup
            time.sleep(3600)
        except Exception as e:
            print(f"Cleanup worker error: {e}")
            time.sleep(300)  # Sleep 5 minutes on error

if __name__ == '__main__':
    # Get configuration
    config_name = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Create downloads directory
    download_folder = Path("downloads")
    download_folder.mkdir(exist_ok=True)
    
    # Start cleanup worker in background
    cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
    cleanup_thread.start()
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"Starting YouTube Downloader Backend on {host}:{port}")
    print(f"Configuration: {config_name}")
    print(f"Download folder: {download_folder.absolute()}")
    
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG']
    )