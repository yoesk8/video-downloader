from flask import Flask, request, render_template, send_file, redirect, url_for
from pytube import YouTube
import os
import tempfile

app = Flask(__name__)

# Create a temporary directory for downloads
temp_dir = tempfile.gettempdir()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        video_title = yt.title.replace('/', '_').replace('\\', '_')  # Sanitize filename
        temp_file_path = os.path.join(temp_dir, f"{video_title}.mp4")

        # Download the video to the temporary directory
        stream.download(temp_dir, filename=f"{video_title}.mp4")

        return send_file(temp_file_path, as_attachment=True, download_name=f"{video_title}.mp4")
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
