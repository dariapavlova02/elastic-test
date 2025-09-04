#!/bin/bash

# Скрипт для полной очистки и перезапуска Docker Compose

echo "🧹 Очищаем все Docker контейнеры и volumes..."

# Остановить все контейнеры
docker-compose -f docker-compose.server.yml down 2>/dev/null || true
docker-compose -f docker-compose.simple.yml down 2>/dev/null || true
docker-compose -f docker-compose.minimal.yml down 2>/dev/null || true

# Удалить все контейнеры проекта
docker container prune -f

# Удалить все неиспользуемые volumes
docker volume prune -f

# Удалить все неиспользуемые сети
docker network prune -f

# Удалить все неиспользуемые образы
docker image prune -f

echo "✅ Очистка завершена"

echo "🚀 Запускаем минимальную версию..."

# Запустить минимальную версию
docker-compose -f docker-compose.minimal.yml up -d --build

echo "⏳ Ожидаем запуска сервисов..."
sleep 30

echo "🏥 Проверяем статус..."
docker-compose -f docker-compose.minimal.yml ps

echo "📋 Логи сервисов:"
docker-compose -f docker-compose.minimal.yml logs --tail=20
