FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd -r backend && useradd --no-log-init -r -g backend backend

COPY . .

RUN chmod -R 755 /app

USER backend

CMD ["python", "app.py"]