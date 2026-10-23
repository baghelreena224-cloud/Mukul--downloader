from flask import Flask, render_template_string, request

app = Flask(__name__)

# वेबसाइट का सुंदर चेहरा (UI) - यह आपके सफ़ेद पेज को बदल देगा
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
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
        <p>Viral Video Downloader is Live!</p>
        
        <!-- यहाँ है वह पेस्ट बॉक्स और बटन -->
        <input type="text" id="videoLink" placeholder="यहाँ वीडियो लिंक पेस्ट करें (URL)">
        <button onclick="alert('डाउनलोडिंग का कोड जल्द आ रहा है!')">वीडियो डाउनलोड करें</button>
        
        <div class="footer">Created with ❤️ by Mukul</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # अब यह साफ़ सफ़ेद पेज नहीं, बल्कि ऊपर वाला सुंदर UI दिखाएगा
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
