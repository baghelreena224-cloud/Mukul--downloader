from flask import Flask, render_template_string, request

app = Flask(__name__)

# होम पेज - SEO Meta Tags के साथ
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Special Surprise Quiz - Mukul App</title>
    <!-- Google SEO Optimization Meta Tags -->
    <meta name="description" content="Mukul Special Surprise Quiz App - अपना नाम और ईमेल दर्ज करें और अपने भविष्य के बारे में मजेदार भविष्यवाणी जानें!">
    <meta name="keywords" content="Mukul Quiz, Surprise Quiz, Future Prediction, Fun Quiz App, मज़ेदार क्विज़">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .card { background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; width: 100%; max-width: 420px; }
        h1 { color: #333; margin-bottom: 0.5rem; font-size: 24px; }
        p { color: #666; margin-bottom: 1.5rem; font-size: 14px; }
        .input-group { margin-bottom: 1rem; text-align: left; }
        label { display: block; margin-bottom: 5px; color: #444; font-weight: bold; font-size: 14px; }
        input[type="text"], input[type="email"] { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 15px; transition: border 0.3s; }
        input:focus { border-color: #667eea; outline: none; }
        button { background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: opacity 0.3s; width: 100%; margin-top: 10px; }
        button:hover { opacity: 0.9; }
        .footer { margin-top: 1.5rem; color: #888; font-size: 13px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>✨ जानिए आपके बारे में एक खास राज! ✨</h1>
        <p>अपना नाम और ईमेल दर्ज करें और देखें जादुई परिणाम</p>
        
        <form action="/result" method="POST">
            <div class="input-group">
                <label>आपका नाम (Your Name):</label>
                <input type="text" name="username" placeholder="यहाँ अपना नाम लिखें" required>
            </div>
            <div class="input-group">
                <label>आपका ईमेल (Gmail):</label>
                <input type="email" name="useremail" placeholder="example@gmail.com" required>
            </div>
            <button type="submit">परिणाम देखें 🚀</button>
        </form>
        
        <div class="footer">Created with 🔥 by Mukul</div>
    </div>
</body>
</html>
"""

# रिजल्ट पेज
RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>आपका रिजल्ट - Mukul App</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #11998e, #38ef7d); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .card { background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; width: 100%; max-width: 420px; }
        h1 { color: #2ecc71; margin-bottom: 0.5rem; }
        .name-highlight { color: #e74c3c; font-size: 22px; font-weight: bold; }
        .result-box { background: #f9f9f9; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2ecc71; text-align: left; font-size: 15px; color: #444; }
        .whatsapp-btn { background-color: #25D366; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; width: 100%; box-sizing: border-box; margin-top: 10px; }
        .whatsapp-btn:hover { background-color: #20ba5a; }
        .back-link { display: block; margin-top: 15px; color: #666; text-decoration: none; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>अरे वाह! 🎉</h1>
        <p>नमस्ते, <span class="name-highlight">{{ name }}</span>!</p>
        
        <div class="result-box">
            <p>🎯 <b>आपकी भविष्यवाणी:</b> आने वाले समय में आप एक बहुत बड़े सॉफ्टवेयर डेवलपर और टेक आंत्रप्रेन्योर बनेंगे! आपकी किस्मत के सितारे बहुत बुलंद हैं।</p>
        </div>
        
        <p style="font-size: 14px; color: #555;">इस मजेदार सरप्राइज को अपने दोस्तों के साथ WhatsApp पर शेयर करें:</p>
        
        <!-- WhatsApp Share Button -->
        <a href="https://api.whatsapp.com/send?text=अरे भाई! मैंने अभी अपना भविष्य देखा और सच में हैरान रह गया! तुम भी यहाँ क्लिक करके अपना नाम डालकर चेक करो: https://mukul-downloader.onrender.com" target="_blank" class="whatsapp-btn">
            🟢 WhatsApp पर शेयर करें
        </a>
        
        <a href="/" class="back-link">← दोबारा कोशिश करें</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/result', methods=['POST'])
def result():
    username = request.form.get('username')
    useremail = request.form.get('useremail')
    return render_template_string(RESULT_TEMPLATE, name=username)

if __name__ == '__main__':
    app.run(debug=True)
