from flask import Flask, request, jsonify, send_file
import yt_dlp
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download():
    try:
        # Parse input
        data = request.json
        video_url = data.get('url')
        format_type = data.get('format')  # 'mp3' or 'mp4'

        if not video_url or not format_type:
            return jsonify({"error": "Missing url or format"}), 400

        # Temporary unique file names
        temp_id = str(uuid.uuid4())
        output_file = f"{temp_id}.{format_type}"

        # yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best' if format_type == 'mp3' else 'bestvideo+bestaudio/best',
            'outtmpl': f'{temp_id}.%(ext)s',
            'quiet': True
        }

        # Download media
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)

        # Convert using FFmpeg if mp3
        if format_type == 'mp3':
            input_file = f"{temp_id}.{info['ext']}"
            subprocess.run(['ffmpeg', '-i', input_file, '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', output_file], check=True)
            os.remove(input_file)  # Clean up intermediate file

        # Serve file directly (no JSON for successful file download)
        return send_file(output_file, as_attachment=True, download_name=f"download.{format_type}")

    except Exception as e:
        # Return a JSON error response in case of failure
        return jsonify({"error": str(e)}), 500
    finally:
        # Cleanup files
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == '__main__':
    app.run(debug=True)
