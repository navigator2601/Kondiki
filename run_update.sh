git add .
git commit -m "Оновлення додатку та Dockerfile для забезпечення сумісності з asyncpg"
git push origin main
docker build -t gcr.io/kondiki/telegram-bot .
docker push gcr.io/kondiki/telegram-bot
gcloud run deploy telegram-bot --image gcr.io/kondiki/telegram-bot --platform managed --region europe-west3 --set-env-vars TELEGRAM_BOT_TOKEN=8177185933:AAGvnm0JmuTxucr8VqU0nzGd4WrNkn5VHpU
