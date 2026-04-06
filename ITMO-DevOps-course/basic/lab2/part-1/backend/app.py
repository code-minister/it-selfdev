import os
import sys
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Функция для подключения к БД (читаем переменные окружения)
def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', '5432'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        dbname=os.environ.get('DB_NAME', 'voting_app')
    )

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    animal = data.get('animal')
    
    if animal not in ['cats', 'dogs', 'giraffes']: 
        return jsonify({"error": "Invalid animal"}), 400


    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Обновляем счетчик
        cur.execute(
            "UPDATE votes SET votes_count = votes_count + 1 WHERE animal_type = %s;",
            (animal,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": f"Vote for {animal} counted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/results', methods=['GET'])
def results():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT animal_type, votes_count FROM votes;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        # Превращаем результат из БД в удобный JSON {"cats": 10, "dogs": 5}
        result = {row[0]: row[1] for row in rows}
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint для проверки здоровья (Liveness/Readiness probe в K8s)
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

# Endpoint для тестирования самовосстановления K8s
@app.route('/crash', methods=['GET'])
def crash():
    print("Crash requested! Shutting down...", flush=True)
    os._exit(1) # Жесткое завершение процесса с ошибкой

if __name__ == '__main__':
    # Бэкенд запускается на порту 8080
    app.run(host='0.0.0.0', port=8080)