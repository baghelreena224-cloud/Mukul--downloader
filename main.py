from flask import Flask, render_template_string, request

app = Flask(__name__)

# विभिन्न भाषाओं के लिए शब्दकोश (Translations Dictionary)
TRANSLATIONS = {
    'hi': {
        'title': 'ग्लोबल विशिंग कार्ड जनरेटर',
        'heading': '🌍 Global Wishing Card 🌍',
        'subheading': 'अपनी भाषा और देश चुनें, नाम और ईमेल दर्ज करें',
        'name_label': 'आपका नाम (Your Name):',
        'name_placeholder': 'यहाँ अपना नाम लिखें',
        'email_label': 'आपका ईमेल (Gmail):',
        'email_placeholder': 'example@gmail.com',
        'lang_label': 'भाषा चुनें (Select Language):',
        'country_label': 'अपना देश चुनें (Select Country):',
        'btn_text': 'कार्ड देखें और शेयर करें 🚀',
        'card_title': 'विशेष शुभकामनाएँ!',
        'card_sub': 'की तरफ से आपको और आपके परिवार को हार्दिक शुभकामनाएँ!',
        'msg': 'ईश्वर आपको और आपके पूरे परिवार को ढेर सारी खुशियाँ, सफलता और उत्तम स्वास्थ्य प्रदान करे! इस खूबसूरत ग्रीटिंग कार्ड को अपने दोस्तों के साथ व्हाट्सएप पर शेयर करें।',
        'share_btn': '🟢 WhatsApp पर शेयर करें',
        'back_link': '← अपना खुद का कार्ड बनाएं',
        'share_text': '✨ {name} ({country}) ने आपके लिए एक स्पेशल विशिंग कार्ड भेजा है! देखने के लिए यहाँ क्लिक करें:'
    },
    'en': {
        'title': 'Global Wishing Card Generator',
        'heading': '🌍 Global Wishing Card 🌍',
        'subheading': 'Select language & country, enter your details to create your card',
        'name_label': 'Your Name:',
        'name_placeholder': 'Enter your name here',
        'email_label': 'Your Email (Gmail):',
        'email_placeholder': 'example@gmail.com',
        'lang_label': 'Select Language:',
        'country_label': 'Select Country:',
        'btn_text': 'Create & Share Card 🚀',
        'card_title': 'Special Greetings!',
        'card_sub': 'Wishes you and your family a wonderful time ahead!',
        'msg': 'May God bless you and your family with immense happiness, success, and good health! Share this beautiful greeting card with your friends on WhatsApp.',
        'share_btn': '🟢 Share on WhatsApp',
        'back_link': '← Create your own card',
        'share_text': '✨ {name} from {country} has sent you a special wishing card! Click here to view:'
    },
    'mr': {
        'title': 'ग्लोबल विशिंग कार्ड जनरेटर',
        'heading': '🌍 Global Wishing Card 🌍',
        'subheading': 'भाषा आणि देश निवडा, तपशील प्रविष्ट करा',
        'name_label': 'तुमचे नाव (Your Name):',
        'name_placeholder': 'येथे तुमचे नाव लिहा',
        'email_label': 'तुमचा ईमेल (Gmail):',
        'email_placeholder': 'example@gmail.com',
        'lang_label': 'भाषा निवडा (Select Language):',
        'country_label': 'देश निवडा (Select Country):',
        'btn_text': 'कार्ड पहा आणि शेअर करा 🚀',
        'card_title': 'विशेष शुभेच्छा!',
        'card_sub': 'तर्फे तुम्हाला आणि तुमच्या कुटुंबाला हार्दिक शुभेच्छा!',
        'msg': 'ईश्वर तुम्हाला आणि तुमच्या संपूर्ण कुटुंबाला भरपूर आनंद, यश आणि उत्तम आरोग्य देवो! हे सुंदर ग्रीटिंग कार्ड तुमच्या मित्रांसोबत WhatsApp वर शेअर करा.',
        'share_btn': '🟢 WhatsApp वर शेयर करा',
        'back_link': '← स्वतःचे कार्ड तयार करा',
        'share_text': '✨ {name} ({country}) ने तुमच्यासाठी एक स्पेशल विशिंग कार्ड पाठवले आहे! पाहण्यासाठी येथे क्लिक करा:'
    }
}

# होम पेज - भाषा, देश और इनपुट फॉर्म के साथ
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Wishing Card - Mukul App</title>
    <meta name="description" content="Create multi-language and international custom greeting cards instantly!">
    <meta name="keywords" content="Wishing Card, Greeting Card Maker, International Card, Mukul App">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #11998e, #38ef7d); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .card { background: white; padding: 2.2rem; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; width: 100%; max-width: 420px; }
        h1 { color: #11998e; margin-bottom: 0.5rem; font-size: 24px; }
        p { color: #666; margin-bottom: 1.2rem; font-size: 13px; }
        .input-group { margin-bottom: 0.9rem; text-align: left; }
        label { display: block; margin-bottom: 4px; color: #444; font-weight: bold; font-size: 13px; }
        input[type="text"], input[type="email"], select { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 14px; transition: border 0.3s; background: #fff; }
        input:focus, select:focus { border-color: #11998e; outline: none; }
        button { background: linear-gradient(135deg, #11998e, #38ef7d); color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: opacity 0.3s; width: 100%; margin-top: 10px; }
        button:hover { opacity: 0.9; }
        .footer { margin-top: 1.2rem; color: #888; font-size: 12px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌍 Global Wishing Card 🌍</h1>
        <p>Create your custom greeting card worldwide!</p>
        
        <form action="/card" method="POST">
            <div class="input-group">
                <label>Select Language / भाषा चुनें:</label>
                <select name="language">
                    <option value="en">English</option>
                    <option value="hi" selected>हिन्दी (Hindi)</option>
                    <option value="mr">मराठी (Marathi)</option>
                </select>
            </div>
            
            <div class="input-group">
                <label>Select Country / देश चुनें:</label>
                <select name="country">
                    <option value="India" selected>🇮🇳 India (भारत)</option>
                    <option value="USA">🇺🇸 USA (अमेरिका)</option>
                    <option value="Russia">🇷🇺 Russia (रूस)</option>
                    <option value="UK">🇬🇧 United Kingdom (यूके)</option>
                    <option value="Canada">🇨🇦 Canada (कनाडा)</option>
                    <option value="Other">🌐 Other Country (अन्य देश)</option>
                </select>
            </div>

            <div class="input-group">
                <label>Your Name / आपका नाम:</label>
                <input type="text" name="username" placeholder="Enter your name" required>
            </div>
            <div class="input-group">
                <label>Your Email / आपका ईमेल (Gmail):</label>
                <input type="email" name="useremail" placeholder="example@gmail.com" required>
            </div>
            <button type="submit">Create Card / कार्ड बनाएं 🚀</button>
        </form>
        
        <div class="footer">Created with 🔥 by Mukul</div>
    </div>
</body>
</html>
"""

# कार्ड डिस्प्ले पेज - यूजर का नाम, देश और भाषा के अनुसार टेक्स्ट दिखाएगा
CARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ t.card_title }} - {{ name }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #ff416c, #ff4b2b); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .card { background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 15px 35px rgba(0,0,0,0.3); text-align: center; width: 100%; max-width: 420px; animation: popUp 0.5s ease-out; }
        @keyframes popUp { 0% { transform: scale(0.8); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        h1 { color: #ff416c; margin-bottom: 0.5rem; font-size: 26px; }
        .from-name { color: #2c3e50; font-size: 22px; font-weight: bold; margin: 15px 0; background: #fdf2f4; padding: 10px; border-radius: 8px; border: 2px dashed #ff416c; }
        .country-tag { font-size: 14px; color: #e67e22; font-weight: bold; margin-bottom: 10px; }
        .greeting-msg { font-size: 15px; color: #555; margin: 20px 0; line-height: 1.6; text-align: left; background: #fff9f9; padding: 12px; border-radius: 8px; }
        .whatsapp-btn { background-color: #25D366; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; width: 100%; box-sizing: border-box; margin-top: 10px; box-shadow: 0 4px 10px rgba(37, 211, 102, 0.4); }
        .whatsapp-btn:hover { background-color: #20ba5a; }
        .back-link { display: block; margin-top: 15px; color: #666; text-decoration: none; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌟 {{ t.card_title }} 🌟</h1>
        <p>{{ t.card_sub }}</p>
        
        <div class="from-name">🎁 {{ name }} 🎁</div>
        <div class="country-tag">📍 From: {{ country }}</div>
        
        <div class="greeting-msg">
            <p>{{ t.msg }}</p>
        </div>
        
        <!-- WhatsApp Share Button -->
        <a href="https://api.whatsapp.com/send?text={{ share_text | urlencode }}" target="_blank" class="whatsapp-btn">
            {{ t.share_btn }}
        </a>
        
        <a href="/" class="back-link">{{ t.back_link }}</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/card', methods=['POST'])
def card():
    username = request.form.get('username')
    useremail = request.form.get('useremail')
    lang = request.form.get('language', 'hi')
    country = request.form.get('country', 'India')
    
    # भाषा के अनुसार डिक्शनरी चुनें
    t = TRANSLATIONS.get(lang, TRANSLATIONS['hi'])
    
    # व्हाट्सएप शेयर टेक्स्ट तैयार करना जिसमें नाम और देश शामिल हो
    share_text_template = t['share_text']
    share_text = share_text_template.format(name=username, country=country) + " https://mukul-downloader.onrender.com"
    
    return render_template_string(CARD_TEMPLATE, name=username, country=country, t=t, share_text=share_text)

if __name__ == '__main__':
    app.run(debug=True)
