FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd -r worker && useradd -r -g worker worker

COPY . .

RUN chmod -r 755 /app

RUN mkdir -p /app/reports && chown worker:worker /app/reports 

USER worker

CMD ["python", "script.py"]