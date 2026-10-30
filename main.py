
from flask import Flask, render_template_string

app = Flask(__name__)

CANVA_EDITOR_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Festival Wishes - Canva Studio</title>
    <!-- AdSense Verification Code -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2891141547348727" crossorigin="anonymous"></script>
    
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }
        body { background: #1f1f2e; color: #fff; min-height: 100vh; padding: 15px; }
        
        .header { text-align: center; margin-bottom: 20px; }
        .header h1 { color: #00c4cc; font-size: 26px; }
        .header p { color: #aaa; font-size: 14px; }

        .editor-container { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; align-items: flex-start; max-width: 1100px; margin: 0 auto; }
        
        /* Left Panel - Controls */
        .controls-panel { background: #2b2b3d; padding: 20px; border-radius: 12px; width: 100%; max-width: 400px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; margin-bottom: 6px; font-size: 13px; color: #ddd; font-weight: bold; }
        .input-group input, .input-group select, .input-group textarea { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #444; background: #1f1f2e; color: #fff; font-size: 14px; }
        .color-pickers { display: flex; gap: 10px; }
        .color-pickers div { flex: 1; }
        
        /* Right Panel - Canva Preview */
        .preview-panel { display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 500px; }
        canvas { background: #ffffff; border-radius: 12px; box-shadow: 0 12px 30px rgba(0,0,0,0.5); max-width: 100%; height: auto; }
        
        .action-buttons { display: flex; gap: 10px; width: 100%; margin-top: 15px; }
        .btn { flex: 1; padding: 12px; border: none; border-radius: 8px; font-weight: bold; font-size: 15px; cursor: pointer; text-align: center; text-decoration: none; transition: 0.3s; }
        .btn-download { background: #00c4cc; color: #fff; }
        .btn-download:hover { background: #00a0a6; }
        .btn-whatsapp { background: #25d366; color: #fff; }
        .btn-whatsapp:hover { background: #1ebd59; }
    </style>
</head>
<body>

    <div class="header">
        <h1>🎨 Canva Festival Studio 🎨</h1>
        <p>अपना मनपसंद फेस्टिवल विशिंग कार्ड खुद डिज़ाइन करें</p>
    </div>

    <div class="editor-container">
        <!-- डिज़ाइन कंट्रोल पैनल -->
        <div class="controls-panel">
            <div class="input-group">
                <label>आपका नाम (Name):</label>
                <input type="text" id="userName" value="मुकुल बघेल" oninput="drawCard()">
            </div>

            <div class="input-group">
                <label>शुभकामना संदेश (Message):</label>
                <textarea id="userMsg" rows="3" oninput="drawCard()">आपको और आपके परिवार को इस पावन पर्व की हार्दिक शुभकामनाएँ! 🌟</textarea>
            </div>

            <div class="input-group">
                <label>राज्य और देश (State & Country):</label>
                <input type="text" id="userLocation" value="उत्तर प्रदेश, भारत" oninput="drawCard()">
            </div>

            <div class="input-group">
                <label>रंग चुनें (Background & Text Colors):</label>
                <div class="color-pickers">
                    <div>
                        <label style="font-size: 11px;">बैकग्राउंड</label>
                        <input type="color" id="bgColor" value="#ff9966" onchange="drawCard()">
                    </div>
                    <div>
                        <label style="font-size: 11px;">हेडिंग कलर</label>
                        <input type="color" id="titleColor" value="#ffffff" onchange="drawCard()">
                    </div>
                    <div>
                        <label style="font-size: 11px;">टेक्स्ट कलर</label>
                        <input type="color" id="textColor" value="#333333" onchange="drawCard()">
                    </div>
                </div>
            </div>

            <div class="input-group">
                <label>कार्ड बॉर्डर/फ्रेम स्टाइल्स:</label>
                <select id="frameStyle" onchange="drawCard()">
                    <option value="gold">👑 रॉयल गोल्ड फ्रेम (Royal Gold)</option>
                    <option value="modern">⚡ मॉडर्न बॉर्डर (Modern Line)</option>
                    <option value="none">कोई फ्रेम नहीं (Simple)</option>
                </select>
            </div>
        </div>

        <!-- कैनवा लाइव प्रीव्यू -->
        <div class="preview-panel">
            <canvas id="cardCanvas" width="500" height="600"></canvas>
            
            <div class="action-buttons">
                <button class="btn btn-download" onclick="downloadImage()">📥 इमेज डाउनलोड करें</button>
                <a id="whatsappBtn" href="#" target="_blank" class="btn btn-whatsapp">🟢 WhatsApp शेयर</a>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('cardCanvas');
        const ctx = canvas.getContext('2d');

        function drawCard() {
            const name = document.getElementById('userName').value || 'आपका नाम';
            const msg = document.getElementById('userMsg').value || 'शुभकामनाएँ!';
            const location = document.getElementById('userLocation').value || 'भारत';
            const bgColor = document.getElementById('bgColor').value;
            const titleColor = document.getElementById('titleColor').value;
            const textColor = document.getElementById('textColor').value;
            const frameStyle = document.getElementById('frameStyle').value;

            // 1. बैकग्राउंड सेट करना
            ctx.fillStyle = bgColor;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // 2. कार्ड का वाइट सेंटर बॉक्स
            ctx.fillStyle = "#ffffff";
            ctx.roundRect(30, 40, 440, 520, 16);
            ctx.fill();

            // 3. बॉर्डर स्टाइल (Canva Frame)
            if (frameStyle === 'gold') {
                ctx.strokeStyle = "#d4af37";
                ctx.lineWidth = 6;
                ctx.strokeRect(45, 55, 410, 490);
            } else if (frameStyle === 'modern') {
                ctx.strokeStyle = "#00c4cc";
                ctx.lineWidth = 4;
                ctx.strokeRect(40, 50, 420, 500);
            }

            // 4. हेडिंग - शुभ संदेश
            ctx.fillStyle = titleColor === '#ffffff' ? bgColor : titleColor;
            ctx.font = "bold 28px 'Segoe UI', sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("✨ विशेष शुभकामनाएँ ✨", 250, 110);

            // 5. भेजने वाले का नाम (From Box)
            ctx.fillStyle = "#f4f4f9";
            ctx.fillRect(70, 140, 360, 60);
            ctx.strokeStyle = bgColor;
            ctx.lineWidth = 2;
            ctx.strokeRect(70, 140, 360, 60);

            ctx.fillStyle = textColor;
            ctx.font = "bold 22px 'Segoe UI', sans-serif";
            ctx.fillText("🎁 " + name + " 🎁", 250, 178);

            // 6. लोकेशन (राज्य / देश)
            ctx.fillStyle = "#e67e22";
            ctx.font = "bold 14px 'Segoe UI', sans-serif";
            ctx.fillText("📍 " + location, 250, 230);

            // 7. विशिंग मैसेज (Wrap Text)
            ctx.fillStyle = textColor;
            ctx.font = "16px 'Segoe UI', sans-serif";
            wrapText(ctx, msg, 250, 280, 340, 26);

            // 8. फुटर ब्रांडिंग
            ctx.fillStyle = "#888888";
            ctx.font = "12px 'Segoe UI', sans-serif";
            ctx.fillText("Created with Festival Wishes Studio", 250, 530);

            // व्हाट्सएप शेयर लिंक अपडेट करना
            const shareText = `✨ ${name} (${location}) ने आपके लिए एक स्पेशल विशिंग कार्ड भेजा है! देखें: https://festival-wishes.onrender.com`;
            document.getElementById('whatsappBtn').href = `https://api.whatsapp.com/send?text=${encodeURIComponent(shareText)}`;
        }

        // टेक्स्ट को ऑटो-रैप (लाइन तोड़ने) के लिए फंक्शन
        function wrapText(context, text, x, y, maxWidth, lineHeight) {
            const words = text.split(' ');
            let line = '';
            for (let n = 0; n < words.length; n++) {
                let testLine = line + words[n] + ' ';
                let metrics = context.measureText(testLine);
                let testWidth = metrics.width;
                if (testWidth > maxWidth && n > 0) {
                    context.fillText(line, x, y);
                    line = words[n] + ' ';
                    y += lineHeight;
                } else {
                    line = testLine;
                }
            }
            context.fillText(line, x, y);
        }

        // डायरेक्ट PNG इमेज डाउनलोड फंक्शन
        function downloadImage() {
            const image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
            const link = document.createElement('a');
            link.download = 'Festival_Wishing_Card.png';
            link.href = image;
            link.click();
        }

        // पहली बार कार्ड ड्रॉ करना
        window.onload = drawCard;
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(CANVA_EDITOR_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
