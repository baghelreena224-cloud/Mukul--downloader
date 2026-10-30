from flask import Flask, render_template_string

app = Flask(__name__)

OFFLINE_PWA_TEMPLATE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mukul Chrome Offline Games Zone</title>
    <style>
        :root {
            --bg-color: #121212;
            --card-bg: #1e1e1e;
            --text-color: #ffffff;
            --accent-color: #00e676;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-color); display: flex; flex-direction: column; align-items: center; min-height: 100vh; padding: 20px; }

        h1 { margin-bottom: 5px; color: var(--accent-color); font-size: 26px; text-align: center; }
        p.subtitle { color: #aaa; margin-bottom: 20px; font-size: 14px; text-align: center; }

        .game-selector { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab-btn { background: var(--card-bg); color: #fff; border: 1px solid #333; padding: 10px 18px; border-radius: 20px; cursor: pointer; font-size: 14px; font-weight: bold; }
        .tab-btn.active { background: var(--accent-color); color: #000; border-color: var(--accent-color); }

        .game-container { background: var(--card-bg); border-radius: 12px; padding: 15px; border: 1px solid #333; display: flex; flex-direction: column; align-items: center; width: 100%; max-width: 500px; }
        canvas { background: #222; border-radius: 8px; border: 2px solid #444; width: 100%; height: auto; }

        .controls { margin-top: 15px; display: flex; gap: 10px; }
        .btn { background: #333; color: #fff; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; }
        .btn:hover { background: #444; }

        .game-box { display: none; text-align: center; width: 100%; }
        .game-box.active { display: block; }
    </style>
</head>
<body>

    <h1>🎮 मुकुल क्रोम ऑफलाइन गेम जोन</h1>
    <p class="subtitle">नेट बंद होने पर भी क्रोम में बिना अटके मजे से खेलें!</p>

    <div class="game-selector">
        <button class="tab-btn active" onclick="switchGame('dino')">🦖 डाइनो रनर</button>
        <button class="tab-btn" onclick="switchGame('snake')">🐍 स्नेक गेम</button>
    </div>

    <div class="game-container">
        <!-- 1. DINO GAME -->
        <div id="dinoGameBox" class="game-box active">
            <canvas id="dinoCanvas" width="400" height="200"></canvas>
            <div class="controls">
                <button class="btn" onclick="jumpDino()">जंप (Jump / Space)</button>
                <button class="btn" onclick="restartDino()">रिफ्रेश</button>
            </div>
            <p style="margin-top:10px; font-size:12px; color:#aaa;">स्क्रीन पर टैप करें या Spacebar दबाएं</p>
        </div>

        <!-- 2. SNAKE GAME -->
        <div id="snakeGameBox" class="game-box">
            <canvas id="snakeCanvas" width="400" height="400"></canvas>
            <div class="controls">
                <button class="btn" onclick="restartSnake()">नया गेम</button>
            </div>
            <p style="margin-top:10px; font-size:12px; color:#aaa;">एरो कीज (Arrow Keys) से चलाएं</p>
        </div>
    </div>

    <script>
        // PWA Offline Service Worker Registration
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW registration failed:', err));
            });
        }

        function switchGame(game) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.game-box').forEach(box => box.classList.remove('active'));

            if (game === 'dino') {
                event.target.classList.add('active');
                document.getElementById('dinoGameBox').classList.add('active');
            } else {
                event.target.classList.add('active');
                document.getElementById('snakeGameBox').classList.add('active');
            }
        }

        /* --- DINO GAME LOGIC --- */
        const dinoCanvas = document.getElementById('dinoCanvas');
        const dCtx = dinoCanvas.getContext('2d');
        let dinoY = 140, dinoVY = 0, isJumping = false;
        let obstacleX = 400, score = 0, dinoGameOver = false;

        function updateDino() {
            if (dinoGameOver) return;

            dinoVY += 0.8;
            dinoY += dinoVY;

            if (dinoY > 140) { dinoY = 140; dinoVY = 0; isJumping = false; }

            obstacleX -= 5;
            if (obstacleX < -20) { obstacleX = 400; score += 10; }

            if (obstacleX < 60 && obstacleX > 30 && dinoY > 100) {
                dinoGameOver = true;
            }

            dCtx.clearRect(0, 0, 400, 200);
            dCtx.fillStyle = '#666'; dCtx.fillRect(0, 180, 400, 2); // Ground
            dCtx.fillStyle = '#00e676'; dCtx.fillRect(40, dinoY, 25, 40); // Dino
            dCtx.fillStyle = '#ff5252'; dCtx.fillRect(obstacleX, 140, 20, 40); // Obstacle

            dCtx.fillStyle = '#fff'; dCtx.font = '14px sans-serif';
            dCtx.fillText('Score: ' + score, 320, 25);

            if (dinoGameOver) {
                dCtx.fillStyle = '#ff5252'; dCtx.font = '20px sans-serif';
                dCtx.fillText('GAME OVER!', 140, 100);
            } else {
                requestAnimationFrame(updateDino);
            }
        }

        function jumpDino() {
            if (!isJumping && !dinoGameOver) { dinoVY = -12; isJumping = true; }
        }

        function restartDino() {
            dinoY = 140; dinoVY = 0; obstacleX = 400; score = 0; dinoGameOver = false;
            updateDino();
        }

        window.addEventListener('keydown', e => { if (e.code === 'Space') jumpDino(); });
        dinoCanvas.addEventListener('touchstart', jumpDino);
        updateDino();

        /* --- SNAKE GAME LOGIC --- */
        const snakeCanvas = document.getElementById('snakeCanvas');
        const sCtx = snakeCanvas.getContext('2d');
        let snake = [{x: 10, y: 10}], food = {x: 15, y: 15}, dx = 1, dy = 0, snakeScore = 0;

        function updateSnake() {
            const head = {x: snake[0].x + dx, y: snake[0].y + dy};

            if (head.x < 0 || head.x >= 20 || head.y < 0 || head.y >= 20) return;

            snake.unshift(head);
            if (head.x === food.x && head.y === food.y) {
                snakeScore += 5;
                food = {x: Math.floor(Math.random()*20), y: Math.floor(Math.random()*20)};
            } else {
                snake.pop();
            }

            sCtx.clearRect(0, 0, 400, 400);
            sCtx.fillStyle = '#ff5252'; sCtx.fillRect(food.x*20, food.y*20, 18, 18);
            sCtx.fillStyle = '#00e676';
            snake.forEach(part => sCtx.fillRect(part.x*20, part.y*20, 18, 18));
        }

        setInterval(updateSnake, 160);

        window.addEventListener('keydown', e => {
            if (e.key === 'ArrowUp' && dy === 0) { dx = 0; dy = -1; }
            if (e.key === 'ArrowDown' && dy === 0) { dx = 0; dy = 1; }
            if (e.key === 'ArrowLeft' && dx === 0) { dx = -1; dy = 0; }
            if (e.key === 'ArrowRight' && dx === 0) { dx = 1; dy = 0; }
        });

        function restartSnake() { snake = [{x: 10, y: 10}]; dx = 1; dy = 0; }
    </script>
</body>
</html>
"""

# Service Worker Code जो ऑफलाइन सेव करता है
SW_CODE = """
const CACHE_NAME = 'mukul-offline-v1';
self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(['/']))
    );
});

self.addEventListener('fetch', e => {
    e.respondWith(
        caches.match(e.request).then(res => res || fetch(e.request))
    );
});
"""

@app.route('/')
def home():
    return render_template_string(OFFLINE_PWA_TEMPLATE)

@app.route('/sw.js')
def service_worker():
    return app.response_class(SW_CODE, mimetype='application/javascript')

if __name__ == '__main__':
    app.run(debug=True)
