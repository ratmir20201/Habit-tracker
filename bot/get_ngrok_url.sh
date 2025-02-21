#!/bin/bash
echo "Ожидание ngrok..."

# Ждем, пока ngrok запустится и создаст туннель
while true; do
    NGROK_URL=$(curl -s http://ngrok:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | cut -d'"' -f4)

    if [[ -n "$NGROK_URL" ]]; then
        echo "NGROK URL: $NGROK_URL"
        break
    fi

    sleep 2
done

# Сохранение в .env
echo "TG__WEBHOOK_URL=$NGROK_URL" > /bot/.env

# Запуск основного бота
exec python main.py
