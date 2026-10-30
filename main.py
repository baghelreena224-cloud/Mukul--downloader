from flask import Flask, render_template_string, request

app = Flask(__name__)

# दुनिया भर की प्रमुख भाषाओं के लिए शब्दकोश (Translations Dictionary for Multiple Languages)
TRANSLATIONS = {
    'hi': {
        'title': 'ग्लोबल विशिंग कार्ड जनरेटर',
        'heading': '🌍 Global Wishing Card 🌍',
        'subheading': 'अपनी भाषा, देश और डिज़ाइन चुनें, नाम दर्ज करें',
        'name_label': 'आपका नाम (Your Name):',
        'email_label': 'आपका ईमेल (Gmail):',
        'lang_label': 'भाषा चुनें (Select Language):',
        'country_label': 'अपना देश चुनें (Select Country):',
        'theme_label': 'डिज़ाइन थीम चुनें (Select Theme):',
        'btn_text': 'कार्ड बनाएं और शेयर करें 🚀',
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
        'subheading': 'Select language, country & design theme, enter your details',
        'name_label': 'Your Name:',
        'email_label': 'Your Email (Gmail):',
        'lang_label': 'Select Language:',
        'country_label': 'Select Country:',
        'theme_label': 'Select Design Theme:',
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
        'subheading': 'भाषा, देश आणि डिझाइन निवडा, तपशील प्रविष्ट करा',
        'name_label': 'तुमचे नाव (Your Name):',
        'email_label': 'तुमचा ईमेल (Gmail):',
        'lang_label': 'भाषा निवडा (Select Language):',
        'country_label': 'देश निवडा (Select Country):',
        'theme_label': 'डिझाइन थीम निवडा (Select Theme):',
        'btn_text': 'कार्ड तयार करा आणि शेअर करा 🚀',
        'card_title': 'विशेष शुभेच्छा!',
        'card_sub': 'तर्फे तुम्हाला आणि तुमच्या कुटुंबाला हार्दिक शुभेच्छा!',
        'msg': 'ईश्वर तुम्हाला आणि तुमच्या संपूर्ण कुटुंबाला भरपूर आनंद, यश आणि उत्तम आरोग्य देवो! हे सुंदर ग्रीटिंग कार्ड तुमच्या मित्रांसोबत WhatsApp वर शेअर करा.',
        'share_btn': '🟢 WhatsApp वर शेयर करा',
        'back_link': '← स्वतःचे कार्ड तयार करा',
        'share_text': '✨ {name} ({country}) ने तुमच्यासाठी एक स्पेशल विशिंग कार्ड पाठवले आहे! पाहण्यासाठी येथे क्लिक करा:'
    },
    'es': {
        'title': 'Generador de Tarjetas de Deseos',
        'heading': '🌍 Tarjeta de Deseos Global 🌍',
        'subheading': 'Selecciona idioma, país y diseño, ingresa tus datos',
        'name_label': 'Tu Nombre:',
        'email_label': 'Tu Correo (Gmail):',
        'lang_label': 'Seleccionar Idioma:',
        'country_label': 'Seleccionar País:',
        'theme_label': 'Seleccionar Tema:',
        'btn_text': 'Crear y Compartir Tarjeta 🚀',
        'card_title': '¡Saludos Especiales!',
        'card_sub': '¡Te desea a ti y a tu familia lo mejor!',
        'msg': '¡Que Dios te bendiga a ti y a tu familia con inmensa felicidad, éxito y buena salud! Comparte esta hermosa tarjeta con tus amigos en WhatsApp.',
        'share_btn': '🟢 Compartir en WhatsApp',
        'back_link': '← Crear tu propia tarjeta',
        'share_text': '✨ ¡{name} de {country} te ha enviado una tarjeta de deseos especial! Haz clic aquí:'
    },
    'fr': {
        'title': 'Générateur de Cartes de Vœux',
        'heading': '🌍 Carte de Vœux Globale 🌍',
        'subheading': 'Sélectionnez la langue, le pays et le thème, entrez vos détails',
        'name_label': 'Votre Nom:',
        'email_label': 'Votre E-mail (Gmail):',
        'lang_label': 'Sélectionner la Langue:',
        'country_label': 'Sélectionner le Pays:',
        'theme_label': 'Sélectionner le Thème:',
        'btn_text': 'Créer et Partager 🚀',
        'card_title': 'Salutations Spéciales !',
        'card_sub': 'Vous souhaite ainsi qu\'à votre famille un merveilleux moment !',
        'msg': 'Que Dieu vous bénisse, vous et votre famille, avec bonheur et santé ! Partagez cette belle carte sur WhatsApp.',
        'share_btn': '🟢 Partager sur WhatsApp',
        'back_link': '← Créer votre propre carte',
        'share_text': '✨ {name} de {country} vous a envoyé une carte de vœux spéciale ! Cliquez ici :'
    },
    'de': {
        'title': 'Globaler Wunschkarten-Generator',
        'heading': '🌍 Globale Wunschkarte 🌍',
        'subheading': 'Sprache, Land und Design wählen, Details eingeben',
        'name_label': 'Ihr Name:',
        'email_label': 'Ihre E-Mail (Gmail):',
        'lang_label': 'Sprache wählen:',
        'country_label': 'Land wählen:',
        'theme_label': 'Design-Thema wählen:',
        'btn_text': 'Karte erstellen & teilen 🚀',
        'card_title': 'Besondere Grüße!',
        'card_sub': 'Wünscht Ihnen und Ihrer Familie eine wunderbare Zeit!',
        'msg': 'Möge Gott Sie und Ihre Familie mit Glück und Gesundheit segnen! Teilen Sie diese schöne Karte auf WhatsApp.',
        'share_btn': '🟢 Auf WhatsApp teilen',
        'back_link': '← Erstellen Sie Ihre eigene Karte',
        'share_text': '✨ {name} aus {country} hat Ihnen eine spezielle Wunschkarte geschickt! Klicken Sie hier:'
    },
    'ja': {
        'title': 'グローバルグリーティングカードジェネレーター',
        'heading': '🌍 グローバルウィッシングカード 🌍',
        'subheading': '言語、国、デザインを選んで詳細を入力してください',
        'name_label': 'お名前:',
        'email_label': 'メールアドレス (Gmail):',
        'lang_label': '言語を選択:',
        'country_label': '国を選択:',
        'theme_label': 'デザインテーマを選択:',
        'btn_text': 'カードを作成して共有 🚀',
        'card_title': '特別なご挨拶！',
        'card_sub': 'あなたとご家族に素晴らしい時間が訪れますように！',
        'msg': '神様があなたとご家族に多くの幸せと健康をもたらしてくださいますように！この美しいカードをWhatsAppでシェアしましょう。',
        'share_btn': '🟢 WhatsAppでシェア',
        'back_link': '← 自分のカードを作成する',
        'share_text': '✨ {name} ({country}) から特別なウィッシングカードが届きました！ここをクリックしてご覧ください:'
    },
    'ru': {
        'title': 'Генератор открыток',
        'heading': '🌍 Глобальная открытка 🌍',
        'subheading': 'Выберите язык, страну и дизайн, введите данные',
        'name_label': 'Ваше имя:',
        'email_label': 'Ваш Email (Gmail):',
        'lang_label': 'Выберите язык:',
        'country_label': 'Выберите страну:',
        'theme_label': 'Выберите тему дизайна:',
        'btn_text': 'Создать и поделиться 🚀',
        'card_title': 'Особые поздравления!',
        'card_sub': 'Желает вам и вашей семье прекрасного настроения!',
        'msg': 'Пусть Бог благословит вас и вашу семью огромным счастьем и здоровьем! Поделитесь этой красивой открыткой в WhatsApp.',
        'share_btn': '🟢 Поделиться в WhatsApp',
        'back_link': '← Создать свою открытку',
        'share_text': '✨ {name} из {country} отправил вам специальную открытку! Нажмите здесь, чтобы посмотреть:'
    },
    'zh': {
        'title': '全球祝福卡生成器',
        'heading': '🌍 全球祝福卡 🌍',
        'subheading': '选择语言、国家和设计主题，输入您的信息',
        'name_label': '您的姓名:',
        'email_label': '您的邮箱 (Gmail):',
        'lang_label': '选择语言:',
        'country_label': '选择国家:',
        'theme_label': '选择设计主题:',
        'btn_text': '创建并分享卡片 🚀',
        'card_title': '特别问候！',
        'card_sub': '祝您和您的家人度过美好的时光！',
        'msg': '愿上帝保佑您和您的家人幸福安康、万事如意！在 WhatsApp 上与您的朋友分享这张美丽的贺卡。',
        'share_btn': '🟢 在 WhatsApp 上分享',
        'back_link': '← 创建您自己的卡片',
        'share_text': '✨ 来自 {country} 的 {name} 给您发送了一张特别的祝福卡！点击此处查看：'
    },
    'ar': {
        'title': 'مولد بطاقات التهنئة العالمية',
        'heading': '🌍 بطاقة تهنئة عالمية 🌍',
        'subheading': 'اختر اللغة والدولة وسمة التصميم، وأدخل تفاصيلك',
        'name_label': 'اسمك:',
        'email_label': 'بريدك الإلكتروني:',
        'lang_label': 'اختر اللغة:',
        'country_label': 'اختر الدولة:',
        'theme_label': 'اختر سمة التصميم:',
        'btn_text': 'إنشاء ومشاركة البطاقة 🚀',
        'card_title': 'تحيات خاصة!',
        'card_sub': 'يتمنى لك ولعائلتك أوقاتاً رائعة!',
        'msg': 'بارك الله فيك وفي عائلتك بالكثير من السعادة والنجاح والصحة الجيدة! شارك هذه البطاقة الجميلة مع أصدقائك على واتساب.',
        'share_btn': '🟢 مشاركة عبر واتساب',
        'back_link': '← أنشئ بطاقتك الخاصة',
        'share_text': '✨ أرسل لك {name} من {country} بطاقة تهنئة خاصة! انقر هنا للمشاهدة:'
    }
}

# थीम डिज़ाइन डिक्शनरी (Canva Style Themes)
THEMES = {
    'festival': {
        'bg': 'linear-gradient(135deg, #ff9966, #ff5e62)',
        'card_bg': '#ffffff',
        'heading_color': '#ff5e62',
        'btn_bg': 'linear-gradient(135deg, #ff9966, #ff5e62)',
        'border': '2px solid #ff5e62'
    },
    'royal': {
        'bg': 'linear-gradient(135deg, #2b5876, #4e4376)',
        'card_bg': '#fffef0',
        'heading_color': '#d4af37',
        'btn_bg': 'linear-gradient(135deg, #d4af37, #aa771c)',
        'border': '2px solid #d4af37'
    },
    'neon': {
        'bg': 'linear-gradient(135deg, #0f2027, #203a43, #2c5364)',
        'card_bg': '#1a1a1a',
        'heading_color': '#00ffcc',
        'text_color': '#ffffff',
        'btn_bg': 'linear-gradient(135deg, #00ffcc, #0077ff)',
        'border': '2px solid #00ffcc'
    },
    'nature': {
        'bg': 'linear-gradient(135deg, #134e5e, #71b280)',
        'card_bg': '#f4fff4',
        'heading_color': '#2e7d32',
        'btn_bg': 'linear-gradient(135deg, #2e7d32, #66bb6a)',
        'border': '2px solid #2e7d32'
    }
}

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2891141547348727" crossorigin="anonymous"></script>
    <title>Global Wishing Card - Pro Studio</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #11998e, #38ef7d); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .card { background: white; padding: 2.2rem; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; width: 100%; max-width: 450px; }
        h1 { color: #11998e; margin-bottom: 0.5rem; font-size: 24px; }
        p { color: #666; margin-bottom: 1.2rem; font-size: 13px; }
        .input-group { margin-bottom: 0.9rem; text-align: left; }
        label { display: block; margin-bottom: 4px; color: #444; font-weight: bold; font-size: 13px; }
        input[type="text"], input[type="email"], select { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 14px; background: #fff; }
        button { background: linear-gradient(135deg, #11998e, #38ef7d); color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 10px; }
        .footer { margin-top: 1.2rem; color: #888; font-size: 12px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌍 Global Wishing Studio 🌍</h1>
        <p>Create stunning international festival cards instantly!</p>
        
        <form action="/card" method="POST">
            <div class="input-group">
                <label>Select Language / भाषा चुनें:</label>
                <select name="language">
                    <option value="en" selected>English</option>
                    <option value="hi">हिन्दी (Hindi)</option>
                    <option value="mr">मराठी (Marathi)</option>
                    <option value="es">Español (Spanish)</option>
                    <option value="fr">Français (French)</option>
                    <option value="de">Deutsch (German)</option>
                    <option value="ja">日本語 (Japanese)</option>
                    <option value="ru">Русский (Russian)</option>
                    <option value="zh">中文 (Chinese)</option>
                    <option value="ar">العربية (Arabic)</option>
                </select>
            </div>
            
            <div class="input-group">
                <label>Select Country / देश चुनें:</label>
                <select name="country">
                    <option value="India" selected>🇮🇳 India (भारत)</option>
                    <option value="USA">🇺🇸 USA</option>
                    <option value="UK">🇬🇧 United Kingdom</option>
                    <option value="Canada">🇨🇦 Canada</option>
                    <option value="UAE">🇦🇪 UAE</option>
                    <option value="Japan">🇯🇵 Japan</option>
                    <option value="Germany">🇩🇪 Germany</option>
                    <option value="France">🇫🇷 France</option>
                    <option value="Global">🌐 Worldwide</option>
                </select>
            </div>

            <div class="input-group">
                <label>Select Design Theme / डिज़ाइन थीम चुनें:</label>
                <select name="theme">
                    <option value="festival" selected>🔥 Festival Vibrant (रंगीन)</option>
                    <option value="royal">👑 Royal Gold (रॉयल)</option>
                    <option value="neon">⚡ Neon Dark (नियोन)</option>
                    <option value="nature">🌿 Nature Fresh (प्राकृतिक)</option>
                </select>
            </div>

            <div class="input-group">
                <label>Your Name / आपका नाम:</label>
                <input type="text" name="username" placeholder="Enter your name" required>
            </div>
            <div class="input-group">
                <label>Your Email / आपका ईमेल:</label>
                <input type="email" name="useremail" placeholder="example@gmail.com" required>
            </div>
            <button type="submit">Create Card / कार्ड बनाएं 🚀</button>
        </form>
        
        <div class="footer">Designed & Developed by Mukul</div>
    </div>
</body>
</html>
"""

CARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2891141547348727" crossorigin="anonymous"></script>
    <title>{{ t.card_title }} - {{ name }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: {{ theme.bg }}; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .card { background: {{ theme.card_bg }}; color: {{ theme.text_color | default('#333') }}; padding: 2.5rem; border-radius: 16px; box-shadow: 0 15px 35px rgba(0,0,0,0.3); text-align: center; width: 100%; max-width: 450px; border: {{ theme.border }}; animation: popUp 0.5s ease-out; }
        @keyframes popUp { 0% { transform: scale(0.8); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        h1 { color: {{ theme.heading_color }}; margin-bottom: 0.5rem; font-size: 26px; }
        .from-name { font-size: 22px; font-weight: bold; margin: 15px 0; background: rgba(0,0,0,0.05); padding: 12px; border-radius: 8px; border: 2px dashed {{ theme.heading_color }}; }
        .country-tag { font-size: 14px; color: #e67e22; font-weight: bold; margin-bottom: 10px; }
        .greeting-msg { font-size: 15px; margin: 20px 0; line-height: 1.6; text-align: left; background: rgba(0,0,0,0.03); padding: 12px; border-radius: 8px; }
        .whatsapp-btn { background-color: #25D366; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; display: inline-block; width: 100%; box-sizing: border-box; margin-top: 10px; box-shadow: 0 4px 10px rgba(37, 211, 102, 0.4); }
        .whatsapp-btn:hover { background-color: #20ba5a; }
        .back-link { display: block; margin-top: 15px; color: inherit; text-decoration: none; font-size: 14px; opacity: 0.8; }
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
    lang = request.form.get('language', 'en')
    country = request.form.get('country', 'India')
    selected_theme = request.form.get('theme', 'festival')
    
    t = TRANSLATIONS.get(lang, TRANSLATIONS['en'])
    theme = THEMES.get(selected_theme, THEMES['festival'])
    
    share_text_template = t['share_text']
    share_text = share_text_template.format(name=username, country=country) + " https://festival-wishes.onrender.com"
    
    return render_template_string(CARD_TEMPLATE, name=username, country=country, t=t, theme=theme, share_text=share_text)

if __name__ == '__main__':
    app.run(debug=True)
