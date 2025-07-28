import os
import uuid
import traceback
import shutil
from pathlib import Path
from flask import Flask, request, send_file, jsonify, after_this_request
from flask_cors import CORS
import yt_dlp
import tempfile

app = Flask(__name__)
# Configure CORS to allow your Vercel frontend
CORS(app, 
     origins=["https://utubebyboby.vercel.app", "http://localhost:3000", "http://localhost:5173"],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

# Temporary download folder
DOWNLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Handle cookies file - look for local cookies.txt first
COOKIES_FILE = None

# Check for local cookies.txt file first
local_cookies = "cookies.txt"
if os.path.exists(local_cookies):
    COOKIES_FILE = os.path.abspath(local_cookies)
    print(f"Using local cookies file: {COOKIES_FILE}")
else:
    # Fallback to environment variable
    ORIGINAL_COOKIES_PATH = os.environ.get("COOKIES_FILE_PATH", "/etc/secrets/cookies.txt")
    temp_cookies = os.path.join(tempfile.gettempdir(), "cookies.txt")
    
    if os.path.exists(ORIGINAL_COOKIES_PATH):
        try:
            shutil.copy(ORIGINAL_COOKIES_PATH, temp_cookies)
            COOKIES_FILE = temp_cookies
        except Exception as e:
            print(f"Warning: Could not copy cookies file: {e}")
    
print(f"Cookies file: {COOKIES_FILE} (exists: {COOKIES_FILE and os.path.exists(COOKIES_FILE)})") if COOKIES_FILE else print("No cookies file found")

@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "YouTube Downloader API is running"})

@app.route("/status")
def status():
    return jsonify({"status": "ok"})

@app.after_request
def add_cors_headers(response):
    # CORS is handled by flask-cors, but we'll ensure it works
    origin = request.headers.get('Origin')
    if origin in ["https://utubebyboby.vercel.app", "http://localhost:3000", "http://localhost:5173"]:
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
        response.headers["Access-Control-Allow-Origin"] = "https://utubebyboby.vercel.app"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.route("/check-cookies")
def check_cookies():
    exists = COOKIES_FILE and os.path.exists(COOKIES_FILE)
    size = os.path.getsize(COOKIES_FILE) if exists else 0
    return jsonify({
        "cookies_file": COOKIES_FILE,
        "exists": exists,
        "size": size
    })

@app.route("/download", methods=["POST", "OPTIONS"])
def download_video():
    # Handle preflight request
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    data = request.get_json()
    url = data.get("url")
    requested_quality = data.get("quality", "best")
    format_ = data.get("format", "mp4")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    video_id = str(uuid.uuid4())
    video_folder = os.path.join(DOWNLOAD_FOLDER, video_id)
    os.makedirs(video_folder, exist_ok=True)

    common_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        # Use single format downloads to avoid FFmpeg requirement
        quality_map = {
            "best": "best[ext=mp4]/best",
            "worst": "worst",
            "720p": "best[height<=720][ext=mp4]/best[height<=720]",
            "1080p": "best[height<=1080][ext=mp4]/best[height<=1080]", 
            "480p": "best[height<=480][ext=mp4]/best[height<=480]",
            "360p": "best[height<=360][ext=mp4]/best[height<=360]",
            "240p": "best[height<=240][ext=mp4]/best[height<=240]",
            "144p": "best[height<=144][ext=mp4]/best[height<=144]"
        }

        format_selector = quality_map.get(requested_quality, requested_quality)

        ydl_opts = {
            "format": format_selector,
            "outtmpl": os.path.join(video_folder, f"%(title)s.%(ext)s"),
            "merge_output_format": "mp4" if format_ == "mp4" else None,
            "postprocessors": [],
            "quiet": False,
            "headers": common_headers,
            "extractor_args": {
                "youtube": {
                    "skip": ["hls", "dash"],
                    "player_skip": ["configs"],
                    "innertube_host": "studio.youtube.com",
                    "innertube_key": None,
                    "visitor_data": None,
                }
            },
            "http_chunk_size": 10485760,  # 10MB chunks
            "retries": 5,  # Increased retries
            "fragment_retries": 5,
            "ignoreerrors": False,
            "no_warnings": False,
            "sleep_interval": 1,  # Add delay between requests
            "embed_subs": False,
            "writesubtitles": False,
            "writeautomaticsub": False,
        }

        used_cookies = False
        if COOKIES_FILE and os.path.exists(COOKIES_FILE):
            ydl_opts["cookiefile"] = COOKIES_FILE
            used_cookies = True

        if format_ == "mp3":
            # For MP3, try to get audio-only formats first to avoid FFmpeg requirement
            format_selector = "bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio"
            ydl_opts["format"] = format_selector
            # Only add FFmpeg processor if we want to convert
            # For now, we'll just download the audio format available
            pass

        # Try multiple download strategies
        download_success = False
        last_error = None
        
        # Strategy 1: Try with cookies
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            download_success = True
        except Exception as e:
            last_error = str(e)
            print(f"Strategy 1 failed: {e}")
            
            # Strategy 2: Try without cookies if bot detection
            if "bot" in str(e).lower():
                print("Trying without cookies...")
                ydl_opts_no_cookies = ydl_opts.copy()
                if "cookiefile" in ydl_opts_no_cookies:
                    del ydl_opts_no_cookies["cookiefile"]
                
                try:
                    with yt_dlp.YoutubeDL(ydl_opts_no_cookies) as ydl:
                        ydl.download([url])
                    download_success = True
                    used_cookies = False
                except Exception as e2:
                    print(f"Strategy 2 failed: {e2}")
                    last_error = str(e2)
                    
                    # Strategy 3: Try with basic options
                    print("Trying with minimal options...")
                    basic_opts = {
                        "format": "best[height<=480]/best",
                        "outtmpl": os.path.join(video_folder, f"%(title)s.%(ext)s"),
                        "quiet": True,
                    }
                    
                    try:
                        with yt_dlp.YoutubeDL(basic_opts) as ydl:
                            ydl.download([url])
                        download_success = True
                        used_cookies = False
                    except Exception as e3:
                        print(f"Strategy 3 failed: {e3}")
                        last_error = str(e3)
        
        if not download_success:
            return jsonify({
                "error": f"All download strategies failed. Last error: {last_error}",
                "cookies_used": used_cookies
            }), 500

        files = [f for f in Path(video_folder).glob("*") if f.is_file()]
        if not files:
            return jsonify({
                "error": "Download failed - no files found",
                "cookies_used": used_cookies
            }), 500

        video_file = max(files, key=lambda f: f.stat().st_ctime)

        @after_this_request
        def cleanup(response):
            try:
                shutil.rmtree(video_folder)
            except Exception as cleanup_err:
                print("Cleanup error:", cleanup_err)
            return response

        mimetype = "video/mp4" if video_file.suffix == ".mp4" else (
            "audio/mpeg" if video_file.suffix == ".mp3" else "application/octet-stream"
        )
        return send_file(
            str(video_file),
            as_attachment=True,
            download_name=video_file.name,
            mimetype=mimetype
        )

    except Exception as e:
        try:
            shutil.rmtree(video_folder)
        except:
            pass
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "cookies_used": COOKIES_FILE and os.path.exists(COOKIES_FILE)
        }), 500

@app.route("/formats", methods=["POST"])
def get_formats():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    common_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        opts = {"quiet": True, "headers": common_headers}
        used_cookies = False
        if COOKIES_FILE and os.path.exists(COOKIES_FILE):
            opts["cookiefile"] = COOKIES_FILE
            used_cookies = True

        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            cleaned_formats = [
                {
                    "format_id": f["format_id"],
                    "ext": f.get("ext"),
                    "resolution": f.get("format_note") or f.get("height"),
                    "filesize": f.get("filesize"),
                    "format": f.get("format"),
                    "vcodec": f.get("vcodec"),
                    "acodec": f.get("acodec")
                }
                for f in formats if f.get("vcodec") != "none" or f.get("acodec") != "none"
            ]
            return jsonify({"cookies_used": used_cookies, "formats": cleaned_formats})
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "cookies_used": COOKIES_FILE and os.path.exists(COOKIES_FILE)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
