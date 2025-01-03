from flask import Flask, render_template, request, jsonify
import yt_dlp
import os
from googleapiclient.discovery import build

app = Flask(__name__)

YOUTUBE_API_KEY = '(your youtube api key here)'

def get_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()
    return response['items'][0]['snippet']['title']

def download_video(url):
    ydl_opts = {
        'quiet': False,
        'outtmpl': os.path.join('corpses', '%(title)s.%(ext)s')  
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video_route():
    video_url = request.form.get('video_url')
    
    video_id = video_url.split("v=")[-1]
    
    try:
        video_title = get_video_details(video_id)
    except Exception as e:
        return jsonify({'message': f'Error fetching video details: {str(e)}'})
    
    try:
        download_video(video_url)
        message = f'Video "{video_title}" downloaded successfully to "corpses/" directory.'
    except Exception as e:
        message = f'Error downloading video: {str(e)}'
    
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)

