from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import subprocess
import uuid

app = Flask(__name__)

def download_video(url, format, output_path):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]+bestvideo[ext=mp4]/best[ext=mp4]' if format == 'mp4' else 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else [],
        'merge_output_format': 'mp4' if format == 'mp4' else None,
        'ffmpeg_location': '/usr/local/bin/ffmpeg',  # Adjust path if needed
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True, None
    except Exception as e:
        return False, str(e)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    format = data.get('format')
    output_path = 'downloads'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    success, error = download_video(url, format, output_path)

    if success:
        filename = os.path.join(output_path, f"{uuid.uuid4()}.{format}")
        return send_file(filename, as_attachment=True, download_name="download.mp4")
    else:
        return jsonify({"error": error}), 500

if __name__ == '__main__':
    app.run(debug=True)
