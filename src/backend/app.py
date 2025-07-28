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
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# Temporary download folder
DOWNLOAD_FOLDER = os.path.join(tempfile.gettempdir(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Path to cookies.txt (check env var first for Render Secret File)
COOKIES_FILE = os.environ.get("COOKIES_FILE_PATH", os.path.join(os.path.dirname(__file__), "cookies.txt"))

@app.route("/")
def index():
    return jsonify({"status": "ok", "message": "YouTube Downloader API is running"})

@app.route("/status")
def status():
    return jsonify({"status": "ok"})

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

@app.route("/check-cookies")
def check_cookies():
    exists = os.path.exists(COOKIES_FILE)
    size = os.path.getsize(COOKIES_FILE) if exists else 0
    return jsonify({
        "cookies_file": COOKIES_FILE,
        "exists": exists,
        "size": size
    })

@app.route("/download", methods=["POST"])
def download_video():
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
        quality_map = {
            "best": "bestvideo+bestaudio/best",
            "worst": "worst",
            "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
            "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
            "240p": "bestvideo[height<=240]+bestaudio/best[height<=240]",
            "144p": "bestvideo[height<=144]+bestaudio/best[height<=144]"
        }

        format_selector = quality_map.get(requested_quality, requested_quality)

        ydl_opts = {
            "format": format_selector,
            "outtmpl": os.path.join(video_folder, f"%(title)s.%(ext)s"),
            "merge_output_format": "mp4" if format_ == "mp4" else None,
            "postprocessors": [],
            "quiet": False,  # enable logs for debugging
            "headers": common_headers,
        }

        used_cookies = False
        if os.path.exists(COOKIES_FILE):
            ydl_opts["cookiefile"] = COOKIES_FILE
            used_cookies = True

        if format_ == "mp3":
            ydl_opts["postprocessors"].append({
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

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
            "cookies_used": os.path.exists(COOKIES_FILE)
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
        if os.path.exists(COOKIES_FILE):
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
            "cookies_used": os.path.exists(COOKIES_FILE)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
