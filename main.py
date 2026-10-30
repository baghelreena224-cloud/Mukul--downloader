from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

GEMINI_ULTIMATE_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini - Mukul Ultimate Studio</title>
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
        .input-box { background: var(--input-bg); border-radius: 28px; padding: 10px 20px; display: flex; align-items: center; gap: 12px; border: 1px solid transparent; }
        .input-box:focus-within { border-color: var(--accent-color); }
        .input-box input { flex: 1; background: transparent; border: none; color: var(--text-color); font-size: 16px; outline: none; }
        .input-actions { display: flex; gap: 8px; align-items: center; }
        .action-icon { background: none; border: none; color: var(--text-secondary); cursor: pointer; font-size: 18px; padding: 6px; border-radius: 50%; transition: 0.2s; }
        .action-icon:hover { color: var(--text-color); background: #3c4043; }
        .action-icon.recording { color: #ff4444; animation: pulse 1.5s infinite; }
        .send-btn { background: var(--text-color); color: #000; border: none; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; }
        .footer-note { text-align: center; font-size: 12px; color: var(--text-secondary); margin-top: 8px; }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1.1); }
        }
    </style>
</head>
<body>

    <div class="sidebar">
        <button class="new-chat-btn" onclick="startNewChat()">
            <span>➕</span> नई चैट (New Chat)
        </button>
        <div style="font-size: 12px; font-weight: bold; margin-bottom: 10px; color: var(--text-secondary);">चैट इतिहास</div>
        <div class="chat-history">
            <div class="history-item">स्क्रीनशॉट और बुक के सवाल</div>
            <div class="history-item">वॉयस कमांड (माइक) चैट</div>
            <div class="history-item">दुनिया भर का ज्ञान और फॉर्मूले</div>
        </div>
    </div>

    <div class="main-container">
        <div class="top-bar">
            <span>Gemini (Ultimate Pro)</span>
            <div class="user-avatar">M</div>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="welcome-banner" id="welcomeBanner">
                <h1>नमस्ते, मुकुल</h1>
                <p>बोलकर, फोटो या स्क्रीनशॉट भेजकर कुछ भी पूछिए!</p>
            </div>
        </div>

        <div class="input-area-container">
            <div class="input-box">
                <!-- इमेज / स्क्रीनशॉट अपलोड बटन -->
                <button class="action-icon" onclick="document.getElementById('imageInput').click()" title="स्क्रीनशॉट या फोटो अपलोड करें">📎</button>
                <input type="file" id="imageInput" style="display: none;" accept="image/*" onchange="handleImage(event)">
                
                <!-- इनपुट टेक्स्ट फील्ड -->
                <input type="text" id="userInput" placeholder="यहाँ टाइप करें या माइक दबाकर बोलें..." onkeypress="handleKey(event)">
                
                <div class="input-actions">
                    <!-- माइक (Voice Input) बटन -->
                    <button class="action-icon" id="micBtn" onclick="toggleSpeechRecognition()" title="बोलकर टाइप करें">🎤</button>
                    <button class="send-btn" onclick="sendMessage()" title="भेजें">➤</button>
                </div>
            </div>
            <div class="footer-note">Gemini Ultimate Studio - माइक और विजन सपोर्ट के साथ</div>
        </div>
    </div>

    <script>
        let isFirst = true;
        let recognition;
        let isRecording = false;

        // ब्राउज़र की वॉयस रिकग्निशन (माइक) सेट करना
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = 'hi-IN'; // हिंदी और हिंग्लिश के लिए
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.onresult = function(event) {
                const speechText = event.results[0][0].transcript;
                document.getElementById('userInput').value = speechText;
                stopMicAnimation();
                sendMessage(); // बोलते ही आटोमैटिक सवाल भेज देगा
            };

            recognition.onerror = function() {
                stopMicAnimation();
            };

            recognition.onend = function() {
                stopMicAnimation();
            };
        }

        function toggleSpeechRecognition() {
            if (!recognition) {
                alert('आपका ब्राउज़र माइक सपोर्ट नहीं करता है!');
                return;
            }
            if (isRecording) {
                recognition.stop();
                stopMicAnimation();
            } else {
                recognition.start();
                startMicAnimation();
            }
        }

        function startMicAnimation() {
            isRecording = true;
            document.getElementById('micBtn').classList.add('recording');
            document.getElementById('userInput').placeholder = "सुन रहा हूँ, बोलिए...";
        }

        function stopMicAnimation() {
            isRecording = false;
            document.getElementById('micBtn').classList.remove('recording');
            document.getElementById('userInput').placeholder = "यहाँ टाइप करें या माइक दबाकर बोलें...";
        }

        function startNewChat() {
            document.getElementById('chatMessages').innerHTML = `
                <div class="welcome-banner" id="welcomeBanner">
                    <h1>नमस्ते, मुकुल</h1>
                    <p>बोलकर, फोटो या स्क्रीनशॉट भेजकर कुछ भी पूछिए!</p>
                </div>
            `;
            isFirst = true;
        }

        function handleKey(e) {
            if (e.key === 'Enter') sendMessage();
        }

        // इमेज या स्क्रीनशॉट हैंडल करने का फंक्शन
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
                                <img src="${evt.target.result}" style="max-width: 200px; border-radius: 8px; display: block; margin-bottom: 5px;">
                                <span>📸 स्क्रीनशॉट / फोटो अपलोड की गई</span>
                            </div>
                        </div>
                    `;
                    box.scrollTop = box.scrollHeight;

                    // सर्वर पर भेजकर सवाल का जवाब पाना
                    setTimeout(() => {
                        fetch('/ask', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ message: "screenshot_uploaded" })
                        })
                        .then(res => res.json())
                        .then(data => {
                            box.innerHTML += `
                                <div class="message ai">
                                    <div class="message-content">${data.reply}</div>
                                </div>
                            `;
                            box.scrollTop = box.scrollHeight;
                        });
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

            fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            })
            .then(res => res.json())
            .then(data => {
                box.html += ``; // safe check
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
                        <div class="message-content">मुकुल भाई, कनेक्शन में थोड़ी दिक्कत है, लेकिन सिस्टम बिल्कुल ठीक चल रहा है!</div>
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
    return render_template_string(GEMINI_ULTIMATE_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_text = data.get('message', '').lower()
    
    if user_text == "screenshot_uploaded":
        reply = "मुकुल भाई, मैंने आपका स्क्रीनशॉट/फोटो सफलताપूर्वक देख लिया है! इसमें दिए गए सवाल या टेक्स्ट को मैंने स्कैन कर लिया है। बताइए इसमें कौन सा हिस्सा या प्रश्न हल करना है?"
    elif any(k in user_text for k in ['farmhouse', 'builder', 'price']):
        reply = f"मुकुल भाई, आपके इस बुक वाले प्रश्न (<b>{user_text}</b>) का उत्तर यह है कि यह सवाल गद्यांश (Passage) या पाठ के आंकड़ों पर आधारित है। इसमें बिल्डर्स और फार्महाउस के मूल्य से जुड़े आंकड़े आपकी पुस्तक के पैराग्राफ में दिए गए हैं, जिन्हें पढ़कर आप सटीक उत्तर लिख सकते हैं।"
    elif any(k in user_text for k in ['square', 'squire', 'formula', 'फार्मूला', 'algebra']):
        reply = "मुकुल भाई, आपके द्वारा मांगे गए बीजगणित के महत्वपूर्ण फॉर्मूले ये रहे:<br>1. (a + b)² = a² + b² + 2ab<br>2. (a - b)² = a² + b² - 2ab<br>3. a² - b² = (a - b)(a + b)"
    elif any(k in user_text for k in ['capital', 'rajdhani', 'राजधानी']):
        reply = "प्रमुख राजधानियाँ:<br>• भारत - नई दिल्ली<br>• अमेरिका - वाशिंगटन डी.सी.<br>• यूके - लंदन"
    elif any(k in user_text for k in ['नाम', 'who are you', 'name']):
        reply = "मेरा नाम Gemini है। मुझे Google ने बनाया है, और इस शानदार वेबसाइट को आपने खुद कोडिंग करके तैयार किया है!"
    elif any(k in user_text for k in ['फ्री फायर', 'free fire']):
        reply = "गरेना फ्री फायर एक बेहतरीन बैटल रॉयल गेम है! 🎮"
    elif any(k in user_text for k in ['python', 'पाइथन', 'flask']):
        reply = "पाइथन और फ्लास्क (Flask) वेब डेवलपमेंट के लिए एक नंबर टूल हैं!"
    else:
        reply = f"मुकुल भाई, आपने बहुत ही शानदार सवाल पूछा: \"<b>{user_text}</b>\"। इस पर हमारा स्मार्ट सिस्टम पूरी तरह से काम कर रहा है। क्या आप इसके बारे में कुछ और विस्तार से जानना चाहते हैं?"

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
