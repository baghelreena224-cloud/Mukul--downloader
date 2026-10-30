from flask import Flask, render_template_string

app = Flask(__name__)

GEMINI_TWIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini - AI Twin Studio</title>
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
        .new-chat-btn { background: #282a2c; color: var(--text-color); border: 1px solid var(--border-color); padding: 12px 16px; border-radius: 24px; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
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
        .input-box { background: var(--input-bg); border-radius: 28px; padding: 10px 20px; display: flex; align-items: center; gap: 15px; border: 1px solid transparent; }
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
            <div class="history-item">फ्री फायर गेमिंग चर्चा</div>
            <div class="history-item">पायथन फ्लास्क प्रोजेक्ट</div>
        </div>
    </div>

    <div class="main-container">
        <div class="top-bar">
            <span>Gemini (Twin Edition)</span>
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
                <button class="action-icon" onclick="document.getElementById('imageInput').click()">📎</button>
                <input type="file" id="imageInput" style="display: none;" accept="image/*" onchange="handleImage(event)">
                <input type="text" id="userInput" placeholder="Gemini से कुछ भी पूछें या टाइप करें..." onkeypress="handleKey(event)">
                <div class="input-actions">
                    <button class="send-btn" onclick="sendMessage()">➤</button>
                </div>
            </div>
            <div class="footer-note">Gemini Twin AI - मुकुल भाई के लिए विशेष रूप से तैयार</div>
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
                                <div class="message-content">अरे वाह मुकुल! मैंने इस इमेज को देख लिया है। यह बहुत बढ़िया है। बताइए इसमें आगे क्या करना है?</div>
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

            // यह पहचानता है कि यूजर ने हिंदी में लिखा है या अंग्रेजी में और वैसी ही भाषा में जवाब देता है
            setTimeout(() => {
                let reply = "";
                const lower = text.toLowerCase();
                
                // चेक करें कि टेक्स्ट अंग्रेजी में है या हिंदी में
                const isEnglish = /^[a-zA-Z0-9\s.,?!]+$/.test(text);

                if (isEnglish) {
                    if (lower.includes('name')) {
                        reply = "I am Gemini, created by Google, and this custom twin studio is built by Mukul!";
                    } else if (lower.includes('python') || lower.includes('flask')) {
                        reply = "Python and Flask make a powerful combo for building web applications like this one!";
                    } else {
                        reply = "Got it, Mukul! I am processing your request in English just like you asked. How else can I help you?";
                    }
                } else {
                    if (lower.includes('नाम')) {
                        reply = "मेरा नाम Gemini है और इसे Google ने बनाया है, और इस शानदार वेबसाइट को आपने (मुकुल भाई) खुद डिज़ाइन किया है!";
                    } else if (lower.includes('फ्री फायर') || lower.includes('free fire')) {
                        reply = "गरेना फ्री फायर एक बहुत ही बेहतरीन बैटल रॉयल गेम है! क्या आप इसके बारे में कुछ और जानना चाहते हैं?";
                    } else {
                        reply = "बिल्कुल मुकुल भाई! आपने एकदम सही कहा। मैं आपकी हर बात समझ रहा हूँ और बिल्कुल वैसी ही मदद कर रहा हूँ जैसी आपको चाहिए।";
                    }
                }

                box.innerHTML += `
                    <div class="message ai">
                        <div class="message-content">${reply}</div>
                    </div>
                `;
                box.scrollTop = box.scrollHeight;
            }, 700);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(GEMINI_TWIN_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
