from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# सुंदर UI जिसमें अब असली डाउनलोड का फॉर्म है
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2891141547348727"
     crossorigin="anonymous"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Viral Video Downloader</title>
    <style>
        body { font-family: sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; width: 90%; max-width: 400px; }
        h1 { color: #333; margin-bottom: 1.5rem; }
        input[type="text"] { width: 100%; padding: 12px; margin-bottom: 1rem; border: 2px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 16px; }
        input[type="text"]:focus { border-color: #28a745; outline: none; }
        button { background-color: #28a745; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 16px; cursor: pointer; transition: background 0.3s; width: 100%; }
        button:hover { background-color: #218838; }
        .footer { margin-top: 1rem; color: #777; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Viral Video Downloader</h1>
        
        <!-- असली डाउनलोड फॉर्म जो बैकएंड पर लिंक भेजेगा -->
        <form action="/download" method="POST">
            <input type="text" name="url" placeholder="यहाँ वीडियो लिंक पेस्ट करें (URL)" required>
            <button type="submit">वीडियो डाउनलोड करें</button>
        </form>
        
        <div class="footer">Created with ❤️ by Mukul</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    
    # yt-dlp की सेटिंग वीडियो डाउनलोड करने के लिए
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)
            
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"डाउनलोड करने में एरर आया है: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
