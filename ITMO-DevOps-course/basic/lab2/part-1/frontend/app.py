import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Читаем конфигурацию из переменных окружения (ConfigMap)
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8080')
BG_COLOR = os.environ.get('BACKGROUND_COLOR', 'white')

# Простая HTML-страничка (прямо в коде, чтобы не плодить файлы)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Котики, Собачки и Жирафы</title>
    <style>
        body { background-color: {{ bg_color }}; font-family: Arial, sans-serif; text-align: center; padding-top: 50px; transition: background-color 0.5s; }
        .btn { padding: 15px 30px; font-size: 20px; margin: 10px; cursor: pointer; border-radius: 8px; border: none; color: white; font-weight: bold;}
        .btn-cat { background-color: #2196F3; }
        .btn-cat:hover { background-color: #0b7dda; }
        .btn-dog { background-color: #4CAF50; }
        .btn-dog:hover { background-color: #46a049; }
        .btn-giraffe { background-color: #FF9800; }  /* Оранжевый цвет для жирафов */
        .btn-giraffe:hover { background-color: #e68a00; }
        .results { margin-top: 30px; font-size: 24px; }
        .results span { font-weight: bold; font-size: 30px;}
    </style>
</head>
<body>
    <h1>Голосование: Выбери любимца</h1>
    
    <div>
        <button class="btn btn-cat" onclick="vote('cats')">🐱 Котики</button>
        <button class="btn btn-dog" onclick="vote('dogs')">🐶 Собачки</button>
        <button class="btn btn-giraffe" onclick="vote('giraffes')">🦒 Жирафы</button>
    </div>

    <div class="results">
        <p>Котики: <span id="cats-count">0</span></p>
        <p>Собачки: <span id="dogs-count">0</span></p>
        <p>Жирафы: <span id="giraffes-count">0</span></p>
    </div>

    <script>
        function loadResults() {
            fetch('/api/results')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('cats-count').innerText = data.cats !== undefined ? data.cats : '0';
                    document.getElementById('dogs-count').innerText = data.dogs !== undefined ? data.dogs : '0';
                    document.getElementById('giraffes-count').innerText = data.giraffes !== undefined ? data.giraffes : '0';
                }).catch(err => console.error("Error loading results:", err));
        }

        function vote(animal) {
            fetch('/api/vote', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ animal: animal })
            }).then(() => loadResults());
        }

        loadResults();
        setInterval(loadResults, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Отдаем HTML, подставляя цвет фона из переменной окружения
    return render_template_string(HTML_TEMPLATE, bg_color=BG_COLOR)

# --- ПРОКСИ-МАРШРУТЫ (Frontend -> Backend) ---

@app.route('/api/vote', methods=['POST'])
def proxy_vote():
    try:
        # Пересылаем запрос от браузера во внутренний Backend
        response = requests.post(f"{BACKEND_URL}/vote", json=request.json, timeout=5)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": "Cannot connect to backend"}), 500

@app.route('/api/results', methods=['GET'])
def proxy_results():
    try:
        # Запрашиваем данные у внутреннего Backend'а
        response = requests.get(f"{BACKEND_URL}/results", timeout=5)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": "Cannot connect to backend"}), 500

if __name__ == '__main__':
    # Фронтенд запускается на порту 3000
    app.run(host='0.0.0.0', port=3000)