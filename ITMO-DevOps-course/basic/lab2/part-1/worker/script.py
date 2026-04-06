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
        
        # Получаем данные из базы
        cur.execute("SELECT animal_type, votes_count FROM votes;")
        rows = cur.fetchall()
        
        # Преобразуем результат в удобный словарь
        results = {row[0]: row[1] for row in rows}
        cats_votes = results.get('cats', 0)
        dogs_votes = results.get('dogs', 0)
        
        cur.close()
        conn.close()

        # Определяем победителя
        if cats_votes > dogs_votes:
            winner = "Котики"
        elif dogs_votes > cats_votes:
            winner = "Собачки"
        else:
            winner = "Ничья"

        # Формируем строку отчета
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_line = f"[{now}] Победитель: {winner}. Счет: {cats_votes}-{dogs_votes}\n"

        # Убеждаемся, что папка существует (на случай локального тестирования)
        os.makedirs(os.path.dirname(REPORT_FILE_PATH), exist_ok=True)

        # Открываем файл в режиме дозаписи ('a' - append)
        with open(REPORT_FILE_PATH, 'a', encoding='utf-8') as f:
            f.write(report_line)

        print(f"Отчет успешно сохранен: {report_line.strip()}")

    except Exception as e:
        print(f"Ошибка при генерации отчета: {e}", file=sys.stderr)
        # Если произошла ошибка (например, БД недоступна), завершаем скрипт с кодом 1.
        # Kubernetes увидит ошибку и пометит запуск CronJob как Failed.
        sys.exit(1)

if __name__ == '__main__':
    generate_report()
    # Успешное завершение работы
    sys.exit(0)