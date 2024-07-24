from flask import current_app as app, request, send_file, render_template_string
import yt_dlp
import os
import re

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        video_file = download_tiktok_video(url)
        if video_file:
            return send_file(video_file, as_attachment=True)
        else:
            return "Failed to download the video. Please check the URL and try again."
    return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Download TikTok Video</title>
          </head>
          <body>
            <div style="text-align:center; margin-top: 50px;">
              <h1>Download TikTok Video</h1>
              <form method="POST">
                <input type="text" name="url" placeholder="Enter TikTok video URL" required>
                <button type="submit">Download</button>
              </form>
            </div>
          </body>
        </html>
    ''')

def sanitize_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    return filename[:255]

def download_tiktok_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'verbose': True,
    }

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'video')
            video_extension = info_dict.get('ext', 'mp4')
            sanitized_title = sanitize_filename(video_title)
            ydl_opts['outtmpl'] = f'downloads/{sanitized_title}.{video_extension}'
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            ydl.download([url])
            return ydl.prepare_filename(info_dict)
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None
