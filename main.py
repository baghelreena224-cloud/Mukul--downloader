from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# सुंदर UI जिसमें अब असली डाउनलोड का फॉर्म और प्राइवेसी/अबाउट सेक्शन दोनों हैं
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2891141547348727"
     crossorigin="anonymous"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Viral Video Downloader</title>
    <style>
        body { font-family: sans-serif; background-color: #f4f4f9; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .container { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; width: 90%; max-width: 500px; margin-top: 20px; }
        h1 { color: #333; margin-bottom: 1.5rem; }
        input[type="text"] { width: 100%; padding: 12px; margin-bottom: 1rem; border: 2px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 16px; }
        input[type="text"]:focus { border-color: #28a745; outline: none; }
        button { background-color: #28a745; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 16px; cursor: pointer; transition: background 0.3s; width: 100%; }
        button:hover { background-color: #218838; }
        .footer { margin-top: 1rem; color: #777; font-size: 14px; }
        .content-section { margin-top: 30px; padding: 20px; background: #fff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: left; color: #333; width: 90%; max-width: 500px; box-sizing: border-box; }
        .content-section h3 { color: #2c3e50; margin-top: 0; }
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

    <!-- निर्देश और प्राइवेसी पॉलिसी सेक्शन -->
    <div class="content-section">
        <h3>Mukul Video Downloader का उपयोग कैसे करें? (How to Use)</h3>
        <ol>
            <li>जिस भी वीडियो को आप डाउनलोड करना चाहते हैं, उसका लिंक (URL) यहाँ कॉपी करके पेस्ट करें।</li>
            <li>डाउनलोड बटन पर क्लिक करें।</li>
            <li>अपनी पसंदीदा वीडियो क्वालिटी चुनकर इसे सेव करें।</li>
        </ol>
        
        <h3>हमारे बारे में (About Us)</h3>
        <p>Mukul Downloader एक आसान और तेज ऑनलाइन टूल है जो उपयोगकर्ताओं को उनके वीडियो लिंक मैनेज करने और डाउनलोड करने में मदद करता है। यह टूल शैक्षणिक और व्यक्तिगत उपयोग के लिए बनाया गया है।</p>
        
        <p style="margin-top: 20px; text-align: center;">
            <a href="/privacy-policy" style="color: #007bff; text-decoration: none; font-weight: bold;">Privacy Policy</a>
        </p>
    </div>
</body>
</html>
"""

PRIVACY_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Mukul Downloader</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; color: #333; background: #f4f4f4; }
        .container { background: #fff; padding: 30px; border-radius: 8px; max-width: 800px; margin: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1, h2 { color: #2c3e50; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Privacy Policy</h1>
        <p>हमारी वेबसाइट पर आपकी गोपनीयता हमारे लिए बहुत महत्वपूर्ण है। यह प्राइवेसी पॉलिसी दस्तावेज बताता है कि हमारी वेबसाइट किस प्रकार की जानकारी एकत्र करती है और उसका उपयोग कैसे करती है।</p>
        
        <h2>Cookies (कुकीज़)</h2>
        <p>हमारी वेबसाइट विज्ञापनों को दिखाने के लिए थर्ड-पार्टी वेंडर (जैसे Google AdSense) का उपयोग करती है। गूगल कुकीज़ का उपयोग करके उपयोगकर्ताओं को उनकी पिछली मुलाकातों के आधार पर विज्ञापन दिखाता है।</p>
        
        <h2>सहमति</h2>
        <p>हमारी वेबसाइट का उपयोग करके, आप हमारी प्राइवेसी पॉलिसी से सहमत होते हैं।</p>
        
        <p style="margin-top: 30px;"><a href="/" style="color: #007bff; text-decoration: none; font-weight: bold;">← वापस होम पेज पर जाएं</a></p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/privacy-policy')
def privacy_policy():
    return render_template_string(PRIVACY_TEMPLATE)

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    
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
