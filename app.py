from flask import Flask, request, send_file, render_template
import os
import youtube_dl
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
url = request.json.get('url', '')
if not url:
return {"error": "Invalid URL. Please enter a valid YouTube video URL."}, 400

video_path = None
try:
# Set options to ensure robust downloading
ydl_opts = {
'format': 'bestvideo+bestaudio/best',  # Download best video and audio separately, then merge
'outtmpl': '%(title)s.%(ext)s',
'merge_output_format': 'mp4',  # Ensure the output is in MP4
'postprocessors': [{
'key': 'FFmpegVideoConvertor',  # Use FFmpeg to convert
'preferedformat': 'mp4',  # Ensure the final format is MP4
}],
'noplaylist': True,  # Don't download playlists
'quiet': False,  # Show download progress
'logger': logger,  # Use the logger
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
video_info = ydl.extract_info(url, download=True)
video_path = f"{video_info['title']}.mp4"

# Ensure the file is created and exists before sending
if not os.path.exists(video_path):
return {"error": "Video file not found after download."}, 500

return send_file(video_path, as_attachment=True)

except youtube_dl.utils.ExtractorError:
return {"error": "Failed to extract video info. Please check if the URL is valid."}, 400
except youtube_dl.utils.DownloadError:
return {"error": "Failed to download video. This can happen if the video is blocked or private."}, 500
except Exception as e:
return {"error": f"An unexpected error occurred: {str(e)}"}, 500
finally:
# Clean up downloaded file if it exists
if video_path and os.path.exists(video_path):
os.remove(video_path)

if __name__ == '__main__':
app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))
