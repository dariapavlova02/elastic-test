# Деплой на сервере - Payment Vector Testing

## Подготовка сервера

### 1. Установка Docker и Docker Compose
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# CentOS/RHEL
sudo yum install -y docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Перелогиниться или выполнить
newgrp docker
```

### 2. Установка Git
```bash
# Ubuntu/Debian
sudo apt install -y git

# CentOS/RHEL
sudo yum install -y git
```

### 3. Установка Python (для локальной загрузки данных)
```bash
# Ubuntu/Debian
sudo apt install -y python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install -y python3 python3-pip
```

## Деплой на сервере

### 1. Клонирование репозитория
```bash
git clone https://github.com/dariapavlova02/elastic-test.git
cd elastic-test
```

### 2. Запуск сервисов
```bash
# Сборка и запуск всех сервисов
make -f Makefile.final build-server
make -f Makefile.final up-server

# Или напрямую через docker-compose
docker-compose -f docker-compose.server.yml up -d --build
```

### 3. Проверка статуса
```bash
# Проверка логов
make -f Makefile.final logs-server

# Проверка здоровья API
make -f Makefile.final health-server

# Или напрямую
curl http://localhost:8000/health
```

### 4. Настройка Nginx (опционально)
```bash
# Копирование конфигурации Nginx
sudo cp nginx/server-nginx.conf /etc/nginx/sites-available/payment-vector
sudo ln -s /etc/nginx/sites-available/payment-vector /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Загрузка данных санкций (локально)

### 1. Подготовка локальной среды
```bash
# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Загрузка данных
```bash
# Загрузка санкций в Elasticsearch на сервере
python load_sanctions_to_elasticsearch.py --es-host http://YOUR_SERVER_IP:9200

# Или через Makefile
make -f Makefile.final load-sanctions-local ELASTICSEARCH_HOST=http://YOUR_SERVER_IP:9200
```

## Тестирование

### 1. Проверка API
```bash
# Проверка здоровья
curl http://YOUR_SERVER_IP:8000/health

# Тест поиска
curl -X POST http://YOUR_SERVER_IP:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Петро Порошенко"}'
```

### 2. Использование клиента
```bash
# Запуск клиента поиска
python final_search_client.py --api-url http://YOUR_SERVER_IP:8000 --query "Петро Порошенко"

# Или через Makefile
make -f Makefile.final search-server SERVER_API_URL=http://YOUR_SERVER_IP:8000
```

## Управление сервисами

### Остановка
```bash
make -f Makefile.final down-server
# или
docker-compose -f docker-compose.server.yml down
```

### Перезапуск
```bash
make -f Makefile.final restart-server
# или
docker-compose -f docker-compose.server.yml restart
```

### Обновление
```bash
git pull
make -f Makefile.final build-server
make -f Makefile.final up-server
```

## Мониторинг

### Логи
```bash
# Все сервисы
make -f Makefile.final logs-server

# Конкретный сервис
docker-compose -f docker-compose.server.yml logs -f server_api
docker-compose -f docker-compose.server.yml logs -f ai_service
docker-compose -f docker-compose.server.yml logs -f elasticsearch
```

### Статус контейнеров
```bash
docker-compose -f docker-compose.server.yml ps
```

### Использование ресурсов
```bash
docker stats
```

## Порты

- **8000** - Search API (основной)
- **9200** - Elasticsearch
- **5601** - Kibana (опционально)
- **8001** - AI Service (внутренний)

## Переменные окружения

Создайте файл `.env` для настройки:
```bash
# .env
ELASTICSEARCH_HOSTS=http://elasticsearch:9200
AI_SERVICE_URL=http://ai_service:8001
PYTHONUNBUFFERED=1
```

## Troubleshooting

### Проблемы с памятью Elasticsearch
```bash
# Увеличить лимиты памяти в docker-compose.server.yml
ES_JAVA_OPTS=-Xms1g -Xmx1g
```

### Проблемы с AI Service
```bash
# Проверить установку зависимостей
docker-compose -f docker-compose.server.yml exec ai_service poetry install
docker-compose -f docker-compose.server.yml exec ai_service python -m spacy download en_core_web_sm
```

### Проблемы с сетью
```bash
# Проверить доступность портов
netstat -tlnp | grep :8000
netstat -tlnp | grep :9200
```

## Безопасность

### Firewall
```bash
# Открыть только необходимые порты
sudo ufw allow 8000/tcp  # Search API
sudo ufw allow 9200/tcp  # Elasticsearch (если нужен внешний доступ)
sudo ufw allow 5601/tcp  # Kibana (если нужен внешний доступ)
```

### SSL (опционально)
Настройте SSL сертификаты в Nginx для HTTPS доступа.

## Масштабирование

### Горизонтальное масштабирование
```bash
# Запуск нескольких экземпляров API
docker-compose -f docker-compose.server.yml up -d --scale server_api=3
```

### Кластер Elasticsearch
Для продакшена рекомендуется настроить кластер Elasticsearch с несколькими нодами.
