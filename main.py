from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

GEMINI_CLONE_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini - Mukul AI Studio</title>
    <!-- Google AdSense Code -->
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

        /* Sidebar */
        .sidebar { width: 260px; background-color: var(--sidebar-bg); display: flex; flex-direction: column; padding: 15px; border-right: 1px solid var(--border-color); transition: transform 0.3s ease; }
        .new-chat-btn { background: #282a2c; color: var(--text-color); border: 1px solid var(--border-color); padding: 12px 16px; border-radius: 24px; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 10px; margin-bottom: 20px; transition: background 0.2s; }
        .new-chat-btn:hover { background: #3c4043; }
        .chat-history { flex: 1; overflow-y: auto; font-size: 13px; color: var(--text-secondary); }
        .history-item { padding: 10px 12px; border-radius: 8px; cursor: pointer; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .history-item:hover { background: #282a2c; color: var(--text-color); }

        /* Main Chat Area */
        .main-container { flex: 1; display: flex; flex-direction: column; height: 100%; position: relative; }
        .top-bar { padding: 15px 25px; font-size: 18px; font-weight: 500; color: var(--text-secondary); display: flex; justify-content: space-between; align-items: center; }
        .user-avatar { width: 32px; height: 32px; background: #8ab4f8; color: #000; border-radius: 50%; display: flex; align-items: center; justify-content: font-weight: bold; }

        .chat-messages { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 24px; max-width: 800px; width: 100%; margin: 0 auto; }
        
        .welcome-banner { text-align: center; margin-top: 15vh; }
        .welcome-banner h1 { font-size: 40px; background: linear-gradient(to right, #9bbcf8, #c48b9f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
        .welcome-banner p { color: var(--text-secondary); font-size: 18px; }

        .message { display: flex; gap: 15px; max-width: 100%; line-height: 1.6; font-size: 15px; }
        .message.user { justify-content: flex-end; }
        .message-content { background: var(--panel-bg); padding: 14px 18px; border-radius: 18px; max-width: 75%; word-break: break-word; }
        .message.user .message-content { background: #2b2d31; border-top-right-radius: 4px; }
        .message.ai .message-content { background: transparent; padding: 0; color: var(--text-color); }

        /* Input Area */
        .input-area-container { padding: 20px; max-width: 800px; width: 100%; margin: 0 auto; }
        .input-box { background: var(--input-bg); border-radius: 28px; padding: 10px 20px; display: flex; align-items: center; gap: 15px; border: 1px solid transparent; transition: border 0.2s; }
        .input-box:focus-within { border-color: var(--accent-color); }
        .input-box input { flex: 1; background: transparent; border: none; color: var(--text-color); font-size: 16px; outline: none; }
        .input-actions { display: flex; gap: 10px; align-items: center; }
        .action-icon { background: none; border: none; color: var(--text-secondary); cursor: pointer; font-size: 18px; padding: 5px; border-radius: 50%; transition: color 0.2s; }
        .action-icon:hover { color: var(--text-color); }
        .send-btn { background: var(--text-color); color: #000; border: none; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: font-weight: bold; transition: opacity 0.2s; }
        .send-btn:hover { opacity: 0.9; }

        .footer-note { text-align: center; font-size: 12px; color: var(--text-secondary); margin-top: 8px; }
    </style>
</head>
<body>

    <!-- साइडबार (Sidebar) -->
    <div class="sidebar">
        <button class="new-chat-btn" onclick="startNewChat()">
            <span>➕</span> नई चैट (New Chat)
        </button>
        <div style="font-size: 12px; font-weight: bold; margin-bottom: 10px; color: var(--text-secondary);">हाल की बातचीत</div>
        <div class="chat-history">
            <div class="history-item">फ्री फायर टिप्स और ट्रिक्स</div>
            <div class="history-item">थंबनेल डिजाइनिंग आइडियाज</div>
            <div class="history-item">पाइथन फ्लास्क ऐप प्रोजेक्ट</div>
        </div>
    </div>

    <!-- मुख्य चैट एरिया (Main Chat Container) -->
    <div class="main-container">
        <div class="top-bar">
            <span>Gemini (Mukul Pro)</span>
            <div class="user-avatar" title="Mukul">M</div>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="welcome-banner" id="welcomeBanner">
                <h1>नमस्ते, मुकुल</h1>
                <p>आज मैं आपकी क्या मदद कर सकता हूँ?</p>
            </div>
        </div>

        <!-- इनपुट एरिया -->
        <div class="input-area-container">
            <div class="input-box">
                <button class="action-icon" title="इमेज अपलोड करें" onclick="document.getElementById('imageInput').click()">📎</button>
                <input type="file" id="imageInput" style="display: none;" accept="image/*" onchange="handleImageUpload(event)">
                
                <input type="text" id="userInput" placeholder="Gemini से कुछ भी पूछें..." onkeypress="handleKeyPress(event)">
                
                <div class="input-actions">
                    <button class="action-icon" title="बोलकर पूछें">🎤</button>
                    <button class="send-btn" onclick="sendMessage()">➤</button>
                </div>
            </div>
            <div class="footer-note">Gemini जैसी वेबसाइट - Mukul AI Studio द्वारा निर्मित</div>
        </div>
    </div>

    <script>
        let isFirstMessage = true;

        function startNewChat() {
            document.getElementById('chatMessages').innerHTML = `
                <div class="welcome-banner" id="welcomeBanner">
                    <h1>नमस्ते, मुकुल</h1>
                    <p>आज मैं आपकी क्या मदद कर सकता हूँ?</p>
                </div>
            `;
            isFirstMessage = true;
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function handleImageUpload(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    appendImageMessage(e.target.result);
                }
                reader.readAsDataURL(file);
            }
        }

        function appendImage(src) {
            if (isFirstMessage) {
                document.getElementById('welcomeBanner').style.display = 'none';
                isFirstMessage = false;
            }
            const chatContainer = document.getElementById('chatMessages');
            chatContainer.innerHTML += `
                <div class="message user">
                    <div class="message-content">
                        <img src="${src}" style="max-width: 200px; border-radius: 8px; display: block; margin-bottom: 5px;">
                        <span>इमेज अपलोड की गई</span>
                    </div>
                </div>
            `;
            chatContainer.scrollTop = chatContainer.scrollHeight;

            // AI रिस्पॉन्स सिमुलेशन
        setTimeout(() => {
                chatContainer.innerHTML += `
                    <div class="message ai">
                        <div class="message-content">वाओ मुकुल! यह तस्वीर बहुत बढ़िया है। मैं इसे देख पा रहा हूँ। आप इसके बारे में क्या जानना चाहते हैं?</div>
                    </div>
                `;
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }, 1000);
        }

        function appendImageMessage(src) {
            appendImage(src);
        }

        function sendMessage() {
            const inputField = document.getElementById('userInput');
            const text = inputField.value.trim();
            if (!text) return;

            if (isFirstMessage) {
                document.getElementById('welcomeBanner').style.display = 'none';
                isFirstMessage = false;
            }

            const chatContainer = document.getElementById('chatMessages');
            
            // यूजर का मैसेज जोड़ना
            chatContainer.innerHTML += `
                <div class="message user">
                    <div class="message-content">${text}</div>
                </div>
            `;
            
            inputField.value = '';
            chatContainer.scrollTop = chatContainer.scrollHeight;

            // स्मार्ट एआई रिस्पॉन्स जनरेट करना
            setTimeout(() => {
                let aiReply = "मुकुल भाई, आपका यह सवाल बहुत ही बढ़िया है! मैं इस पर पूरी तरह काम कर रहा हूँ।";
                if(text.toLowerCase().includes('फ्री फायर') || text.toLowerCase().includes('free fire')) {
                    aiReply = "गरेना फ्री फायर एक बहुत ही लोकप्रिय बैटल रॉयल गेम है! इसके कस्टम और करैक्टर स्किल्स कमाल के होते हैं। 🎮";
                } else if(text.toLowerCase().includes('नाम') || text.toLowerCase().includes('name')) {
                    aiReply = "मेरा नाम Gemini है और इसे Google ने बनाया है, और इस शानदार वेबसाइट को आपने (मुकुल ने) डिजाइन किया है! 🚀";
                } else if(text.toLowerCase().includes('पाइथन') || text.toLowerCase().includes('python')) {
                    aiReply = "पाइथन एक बहुत ही पावरफुल लैंग्वेज है, जिसकी मदद से आप Flask और Web Apps आसानी से बना सकते हैं।";
                }

                chatContainer.innerHTML += `
                    <div class="message ai">
                        <div class="message-content">${aiReply}</div>
                    </div>
                `;
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }, 800);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(GEMINI_CLONE_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
