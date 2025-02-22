FROM python:3.9-slim

WORKDIR /app

# Встановлення інструментів для компіляції
RUN apt-get update && apt-get install -y gcc

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV PORT 8080

CMD ["python", "bot_menu.py"]