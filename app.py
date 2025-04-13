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
        return {"error": "Invalid URL. Please enter a valid YouTube video URL."}, 400

    video_path = None
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',  # Save video with its title
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            video_path = f"{video_info['title']}.mp4"

        return send_file(video_path, as_attachment=True)

    except youtube_dl.utils.ExtractorError:
        return {"error": "Failed to extract video info. Please check if the URL is valid."}, 400
    except youtube_dl.utils.DownloadError:
        return {"error": "Failed to download video. Please try again later."}, 500
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}, 500
    finally:
        # Clean up downloaded file
        if video_path and os.path.exists(video_path):
            os.remove(video_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))