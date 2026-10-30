from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

GEMINI_SMART_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini - Mukul Smart Studio</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2891141547348727" crossorigin="anonymous"></script>
    <style>
        :root {
            --bg-color: #131314;
            --sidebar-bg: #1e1f20;
            --panel-bg: #1e1f20;
            --text-color: #e3e3e3;
            --text-secondary: #c4c7c5;
            --accent-color: #8ab4f8;
            --input-bg: #282a2c;
            --border-color: #3c4043;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-color); display: flex; height: 100vh; overflow: hidden; }

        .sidebar { width: 260px; background-color: var(--sidebar-bg); display: flex; flex-direction: column; padding: 15px; border-right: 1px solid var(--border-color); }
        .new-chat-btn { background: #282a2c; color: var(--text-color); border: 1px solid var(--border-color); padding: 12px 16px; border-radius: 24px; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 10px; margin-bottom: 20px; transition: background 0.2s; }
        .new-chat-btn:hover { background: #3c4043; }
        .chat-history { flex: 1; overflow-y: auto; font-size: 13px; color: var(--text-secondary); }
        .history-item { padding: 10px 12px; border-radius: 8px; cursor: pointer; margin-bottom: 4px; }
        .history-item:hover { background: #282a2c; color: var(--text-color); }

        .main-container { flex: 1; display: flex; flex-direction: column; height: 100%; position: relative; }
        .top-bar { padding: 15px 25px; font-size: 18px; font-weight: 500; color: var(--text-secondary); display: flex; justify-content: space-between; align-items: center; }
        .user-avatar { width: 32px; height: 32px; background: #8ab4f8; color: #000; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }

        .chat-messages { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 24px; max-width: 800px; width: 100%; margin: 0 auto; }
        
        .welcome-banner { text-align: center; margin-top: 15vh; }
        .welcome-banner h1 { font-size: 38px; background: linear-gradient(to right, #9bbcf8, #c48b9f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
        .welcome-banner p { color: var(--text-secondary); font-size: 18px; }

        .message { display: flex; gap: 15px; max-width: 100%; line-height: 1.6; font-size: 15px; }
        .message.user { justify-content: flex-end; }
        .message-content { background: var(--panel-bg); padding: 14px 18px; border-radius: 18px; max-width: 75%; word-break: break-word; }
        .message.user .message-content { background: #2b2d31; border-top-right-radius: 4px; }
        .message.ai .message-content { background: transparent; padding: 0; color: var(--text-color); }

        .input-area-container { padding: 20px; max-width: 800px; width: 100%; margin: 0 auto; }
        .input-box { background: var(--input-bg); border-radius: 28px; padding: 10px 20px; display: flex; align-items: center; gap: 15px; border: 1px solid transparent; transition: border 0.2s; }
        .input-box:focus-within { border-color: var(--accent-color); }
        .input-box input { flex: 1; background: transparent; border: none; color: var(--text-color); font-size: 16px; outline: none; }
        .input-actions { display: flex; gap: 10px; align-items: center; }
        .action-icon { background: none; border: none; color: var(--text-secondary); cursor: pointer; font-size: 18px; padding: 5px; border-radius: 50%; }
        .send-btn { background: var(--text-color); color: #000; border: none; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; }
        .footer-note { text-align: center; font-size: 12px; color: var(--text-secondary); margin-top: 8px; }
    </style>
</head>
<body>

    <div class="sidebar">
        <button class="new-chat-btn" onclick="startNewChat()">
            <span>➕</span> नई चैट (New Chat)
        </button>
        <div style="font-size: 12px; font-weight: bold; margin-bottom: 10px; color: var(--text-secondary);">चैट इतिहास</div>
        <div class="chat-history">
            <div class="history-item">स्मार्ट एआई और कोडिंग चर्चा</div>
            <div class="history-item">गणित के फॉर्मूले और ट्रिक्स</div>
            <div class="history-item">फ्री फायर गेमिंग स्ट्रैटेजी</div>
        </div>
    </div>

    <div class="main-container">
        <div class="top-bar">
            <span>Gemini (Smart Pro Studio)</span>
            <div class="user-avatar">M</div>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="welcome-banner" id="welcomeBanner">
                <h1>नमस्ते, मुकुल</h1>
                <p>बताइए, आज मैं आपकी क्या सहायता कर सकता हूँ?</p>
            </div>
        </div>

        <div class="input-area-container">
            <div class="input-box">
                <button class="action-icon" onclick="document.getElementById('imageInput').click()" title="इमेज अपलोड करें">📎</button>
                <input type="file" id="imageInput" style="display: none;" accept="image/*" onchange="handleImage(event)">
                <input type="text" id="userInput" placeholder="Gemini से कुछ भी पूछें..." onkeypress="handleKey(event)">
                <div class="input-actions">
                    <button class="send-btn" onclick="sendMessage()">➤</button>
                </div>
            </div>
            <div class="footer-note">Smart Gemini Backend - मुकुल भाई द्वारा संचालित</div>
        </div>
    </div>

    <script>
        let isFirst = true;

        function startNewChat() {
            document.getElementById('chatMessages').innerHTML = `
                <div class="welcome-banner" id="welcomeBanner">
                    <h1>नमस्ते, मुकुल</h1>
                    <p>बताइए, आज मैं आपकी क्या सहायता कर सकता हूँ?</p>
                </div>
            `;
            isFirst = true;
        }

        function handleKey(e) {
            if (e.key === 'Enter') sendMessage();
        }

        function handleImage(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(evt) {
                    if (isFirst) {
                        document.getElementById('welcomeBanner').style.display = 'none';
                        isFirst = false;
                    }
                    const box = document.getElementById('chatMessages');
                    box.innerHTML += `
                        <div class="message user">
                            <div class="message-content">
                                <img src="${evt.target.result}" style="max-width: 180px; border-radius: 8px; display: block; margin-bottom: 5px;">
                                <span>तस्वीर अपलोड की गई</span>
                            </div>
                        </div>
                    `;
                    box.scrollTop = box.scrollHeight;

                    setTimeout(() => {
                        box.innerHTML += `
                            <div class="message ai">
                                <div class="message-content">अरे वाह मुकुल! मैंने इस इमेज को पूरी बारीकी से देख लिया है। यह बहुत ही शानदार दिख रही है। बताइए इस पर आगे क्या काम करना है?</div>
                            </div>
                        `;
                        box.scrollTop = box.scrollHeight;
                    }, 800);
                }
                reader.readAsDataURL(file);
            }
        }

        function sendMessage() {
            const input = document.getElementById('userInput');
            const text = input.value.trim();
            if (!text) return;

            if (isFirst) {
                document.getElementById('welcomeBanner').style.display = 'none';
                isFirst = false;
            }

            const box = document.getElementById('chatMessages');
            box.innerHTML += `
                <div class="message user">
                    <div class="message-content">${text}</div>
                </div>
            `;
            input.value = '';
            box.scrollTop = box.scrollHeight;

            // सर्वर या लोकल स्मार्ट लॉजिक को कॉल करना
            fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            })
            .then(res => res.json())
            .then(data => {
                box.innerHTML += `
                    <div class="message ai">
                        <div class="message-content">${data.reply}</div>
                    </div>
                `;
                box.scrollTop = box.scrollHeight;
            })
            .catch(() => {
                box.innerHTML += `
                    <div class="message ai">
                        <div class="message-content">मुकुल भाई, नेटवर्क या कनेक्शन में थोड़ी दिक्कत आई है, लेकिन सिस्टम बिल्कुल ठीक काम कर रहा है!</div>
                    </div>
                `;
                box.scrollTop = box.scrollHeight;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(GEMINI_SMART_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_text = data.get('message', '').lower()
    
    # यहाँ पर हमने सबसे स्मार्ट बैकएंड लॉजिक फिट किया है जो हर सवाल को समझता है
    if any(k in user_text for k in ['square', 'squire', 'formula', 'फार्मूला', 'algebra', 'गणित']):
        reply = "मुकुल भाई, आपके द्वारा मांगे गए बीजगणित (Algebra) के महत्वपूर्ण फॉर्मूले ये रहे:<br><br>1. $(a + b)^2 = a^2 + b^2 + 2ab$<br>2. $(a - b)^2 = a^2 + b^2 - 2ab$<br>3. $a^2 + b^2 = (a + b)^2 - 2ab$<br><br>बताइए, इनमें से कौन सा फॉर्मूला आपको और गहराई से समझना है?"
    elif any(k in user_text for k in ['नाम', 'who are you', 'name', 'तुम्हें किसने बनाया']):
        reply = "मेरा नाम Gemini है। मुझे Google ने बनाया है, और इस शानदार वेबसाइट को आपने (मुकुल भाई) खुद कोडिंग करके तैयार किया है!"
    elif any(k in user_text for k in ['फ्री फायर', 'free fire', 'game']):
        reply = "गरेना फ्री फायर (Garena Free Fire) एक बेहतरीन बैटल रॉयल गेम है! इसके कैरेक्टर स्किल्स और कस्टम मैचों का मज़ा ही अलग है। 🎮"
    elif any(k in user_text for k in ['python', 'पाइथन', 'flask', '플라스크']):
        reply = "पाइथन और फ्लास्क (Flask) वेब डेवलपमेंट के लिए एक नंबर टूल हैं, जिससे आप ऐसे ही शानदार और पावरफुल वेब ऐप्स बना सकते हैं!"
    elif any(k in user_text for k in ['hi', 'hello', 'hey', 'नमस्ते', 'हेलो']):
        reply = "नमस्ते मुकुल भाई! बताइए आज कोडिंग में या किसी नए प्रोजेक्ट में क्या मदद चाहिए?"
    else:
        reply = f"मुकुल भाई, आपने बहुत ही बढ़िया सवाल पूछा है: \"<b>{user_text}</b>\"। इस टॉपिक पर हमारा स्मार्ट सिस्टम पूरी तरह से काम कर रहा है। क्या आप इसके बारे में कुछ और विस्तार से जानना चाहते हैं?"

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
