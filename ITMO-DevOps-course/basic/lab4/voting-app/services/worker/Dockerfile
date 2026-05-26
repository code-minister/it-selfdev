FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd -r worker && useradd -r -g worker worker

COPY . .

RUN chmod -R 755 /app

RUN mkdir -p /app/reports && chown worker:worker /app/reports 

USER worker

CMD ["python", "script.py"]