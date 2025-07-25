"""
YouTube Video Downloader Backend
A Flask-based API server for downloading YouTube videos using yt-dlp
"""

import os
import uuid
import traceback
import shutil
from pathlib import Path
from flask import Flask, request, send_file, jsonify, after_this_request
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return "YouTube Video Downloader API"

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

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

        quality_map = {
            "best": "best",
            "worst": "worst",
            "720p": "best[height<=720]",
            "1080p": "best[height<=1080]",
            "480p": "best[height<=480]",
            "360p": "best[height<=360]",
            "240p": "best[height<=240]",
            "144p": "best[height<=144]"
        }

        format_selector = requested_quality
        if requested_quality in quality_map:
            format_selector = quality_map[requested_quality]
        elif requested_quality not in [f['format_id'] for f in formats] and requested_quality not in ["best", "worst"]:
            if requested_quality.endswith('p') and requested_quality[:-1].isdigit():
                height = int(requested_quality[:-1])
                format_selector = f"best[height<={height}]"
            else:
                available_qualities = list(quality_map.keys()) + [f['format_id'] for f in formats[:10]]
                return jsonify({"error": f"Requested quality '{requested_quality}' is not available. Available options: {', '.join(available_qualities)}"}), 400

        ydl_opts = {
            "format": format_selector,
            "outtmpl": os.path.join(video_folder, f"%(title)s.%(ext)s"),
            "postprocessors": [],
        }

        if format_ == "mp3":
            ydl_opts["postprocessors"].append({
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video_file = None
        files = list(Path(video_folder).glob(f"*.{format_}"))
        if not files:
            for ext in ['mp4', 'webm', 'mkv', 'avi', 'mov']:
                files = list(Path(video_folder).glob(f"*.{ext}"))
                if files:
                    break
        if not files:
            files = [f for f in Path(video_folder).iterdir() if f.is_file()]
        if not files:
            return jsonify({"error": "Download failed - no files found"}), 500

        video_file = max(files, key=lambda f: f.stat().st_ctime)

        @after_this_request
        def cleanup(response):
            try:
                shutil.rmtree(video_folder)
            except Exception as cleanup_err:
                print("Cleanup error:", cleanup_err)
            return response

        return send_file(str(video_file), as_attachment=True)

    except Exception as e:
        try:
            shutil.rmtree(video_folder)
        except:
            pass
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/formats", methods=["POST"])
def get_formats():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            cleaned_formats = []
            for f in formats:
                if f.get("vcodec") != "none" or f.get("acodec") != "none":
                    cleaned_formats.append({
                        "format_id": f["format_id"],
                        "ext": f.get("ext"),
                        "resolution": f.get("format_note") or f.get("height"),
                        "filesize": f.get("filesize"),
                        "format": f.get("format"),
                        "vcodec": f.get("vcodec"),
                        "acodec": f.get("acodec")
                    })
            return jsonify(cleaned_formats)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)