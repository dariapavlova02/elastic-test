#!/bin/bash

# Скрипт для быстрого деплоя Payment Vector Testing на сервере

set -e

echo "🚀 Начинаем деплой Payment Vector Testing..."

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и повторите попытку."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose и повторите попытку."
    exit 1
fi

# Проверка Git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите Git и повторите попытку."
    exit 1
fi

echo "✅ Все зависимости установлены"

# Клонирование репозитория (если не существует)
if [ ! -d "elastic-test" ]; then
    echo "📥 Клонируем репозиторий..."
    git clone https://github.com/dariapavlova02/elastic-test.git
    cd elastic-test
else
    echo "📁 Репозиторий уже существует, обновляем..."
    cd elastic-test
    git pull
fi

# Сборка и запуск сервисов
echo "🔨 Собираем Docker образы..."
make -f Makefile.final simple-build

echo "🚀 Запускаем сервисы..."
make -f Makefile.final simple-up

# Ожидание запуска сервисов
echo "⏳ Ожидаем запуска сервисов..."
sleep 30

# Проверка здоровья
echo "🏥 Проверяем здоровье сервисов..."
if make -f Makefile.final health-server > /dev/null 2>&1; then
    echo "✅ API сервис работает!"
else
    echo "❌ API сервис не отвечает. Проверьте логи:"
    make -f Makefile.final logs-server
    exit 1
fi

# Проверка Elasticsearch
echo "🔍 Проверяем Elasticsearch..."
if curl -s http://localhost:9200/_cluster/health > /dev/null 2>&1; then
    echo "✅ Elasticsearch работает!"
else
    echo "❌ Elasticsearch не отвечает. Проверьте логи:"
    docker-compose -f docker-compose.server.yml logs elasticsearch
    exit 1
fi

echo ""
echo "🎉 Деплой завершен успешно!"
echo ""
echo "📋 Информация о сервисах:"
echo "   • Search API: http://localhost:8000"
echo "   • Elasticsearch: http://localhost:9200"
echo "   • Kibana: http://localhost:5601"
echo ""
echo "🔧 Полезные команды:"
echo "   • Просмотр логов: make -f Makefile.final logs-server"
echo "   • Остановка: make -f Makefile.final down-server"
echo "   • Перезапуск: make -f Makefile.final restart-server"
echo ""
echo "📖 Подробная документация: DEPLOYMENT.md"
echo ""
echo "🧪 Для тестирования выполните:"
echo "   python final_search_client.py --api-url http://localhost:8000 --query 'Петро Порошенко'"
