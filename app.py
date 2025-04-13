from flask import Flask, request, send_file, render_template
import os
import ytdl_core

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    if not url or not ytdl_core.YoutubeDL().extract_info(url, download=False):
        return {"error": "Invalid URL"}, 400

    video_path = None
    try:
        video_info = ytdl_core.YoutubeDL().extract_info(url, download=True)
        video_path = f"{video_info['title']}.mp4"
        return send_file(video_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))
