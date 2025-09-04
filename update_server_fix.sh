#!/bin/bash

echo "🚀 Обновление сервера с исправленным AI service..."

# 1. Обновить код на сервере
echo "�� Обновление кода..."
ssh root@95.217.84.234 "cd /root/elastic-test && git pull"

# 2. Перезапустить контейнеры
echo "🔄 Перезапуск контейнеров..."
ssh root@95.217.84.234 "cd /root/elastic-test && docker-compose -f docker-compose.simple.yml down && docker-compose -f docker-compose.simple.yml up -d --build"

# 3. Ждать запуска
echo "⏳ Ожидание запуска сервисов..."
sleep 30

# 4. Проверить статус
echo "🧪 Проверка статуса..."
curl -X GET http://95.217.84.234/health

echo "✅ Обновление завершено!"
