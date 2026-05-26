import os
import sys
import psycopg2
from datetime import datetime

# Путь, по которому мы будем сохранять файл.
# В Kubernetes мы примонтируем (подключим) виртуальный диск именно в эту папку!
REPORT_FILE_PATH = '/app/reports/report.txt'

def get_db_connection():
    """Подключаемся к БД, используя переменные окружения"""
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', '5432'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        dbname=os.environ.get('DB_NAME', 'voting_app')
    )

def generate_report():
    print("Начинаю генерацию отчета...")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT animal_type, votes_count FROM votes;")
        rows = cur.fetchall()
        
        results = {row[0]: row[1] for row in rows}
        cats_votes = results.get('cats', 0)
        dogs_votes = results.get('dogs', 0)
        giraffes_votes = results.get('giraffes', 0) # Достаем жирафов
        
        cur.close()
        conn.close()

        # Красивая логика поиска победителя из любого количества участников
        score_dict = {
            'Котики': cats_votes, 
            'Собачки': dogs_votes, 
            'Жирафы': giraffes_votes
        }
        
        # Находим максимальное количество голосов
        max_votes = max(score_dict.values())
        
        # Ищем всех, у кого столько же голосов (на случай ничьей)
        winners =[animal for animal, votes in score_dict.items() if votes == max_votes]
        
        if len(winners) == 1:
            winner = winners[0]
        else:
            winner = "Ничья между: " + " и ".join(winners)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_line = f"[{now}] Победитель: {winner}. Счет (К-С-Ж): {cats_votes}-{dogs_votes}-{giraffes_votes}\n"

        os.makedirs(os.path.dirname(REPORT_FILE_PATH), exist_ok=True)
        with open(REPORT_FILE_PATH, 'a', encoding='utf-8') as f:
            f.write(report_line)

        print(f"Отчет успешно сохранен: {report_line.strip()}")

    except Exception as e:
        print(f"Ошибка при генерации отчета: {e}", file=sys.stderr)
        sys.exit(1)