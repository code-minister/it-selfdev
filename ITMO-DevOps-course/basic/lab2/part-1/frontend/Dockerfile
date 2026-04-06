FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd -r frontend && useradd --no-log-init -r -g frontend frontend 

COPY . .

RUN chmod -R 755 /app

USER frontend

CMD ["python", "app.py"]
