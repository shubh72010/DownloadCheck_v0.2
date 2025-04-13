from flask import Flask, request, send_file, render_template
import os
import youtube_dl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    if not url:
        return {"error": "Invalid URL"}, 400

    video_path = None
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',  # Saves video with its title
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            video_path = f"{video_info['title']}.mp4"
        
        return send_file(video_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))