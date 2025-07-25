version: '3.8'

services:
  youtube-downloader-backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-production-secret-key
      - DOWNLOAD_FOLDER=/app/downloads
      - MAX_DOWNLOAD_SIZE=1073741824
      - CLEANUP_AFTER_HOURS=24
      - RATE_LIMIT_PER_MINUTE=10
      - CORS_ORIGINS=http://localhost:3000
    volumes:
      - ./downloads:/app/downloads
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - youtube-downloader-backend
    restart: unless-stopped