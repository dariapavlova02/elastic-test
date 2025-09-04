# Инструкция по запуску сервера

## 1. Подготовка на сервере

```bash
# Клонируем репозиторий
git clone <your-repo-url>
cd elastic-test-clean

# Создаем необходимые директории для volumes
mkdir -p logs
mkdir -p nginx/ssl
```

## 2. Запуск с volumes (полная версия)

```bash
# Запускаем все сервисы с volumes
docker-compose -f docker-compose.simple.yml up -d --build

# Проверяем статус
docker-compose -f docker-compose.simple.yml ps

# Смотрим логи
docker-compose -f docker-compose.simple.yml logs -f
```

## 3. Проверка работы

```bash
# Проверяем health
curl http://localhost/health

# Проверяем API напрямую
curl http://localhost:8000/health

# Тестируем поиск
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Петро Порошенко", "limit": 5}'
```

## 4. Загрузка данных

```bash
# Создаем индекс санкций
python create_sanctions_index.py

# Загружаем данные через API
python load_sanctions_via_api.py --batch-size 10 --delay 1
```

## 5. Управление

```bash
# Остановка
docker-compose -f docker-compose.simple.yml down

# Перезапуск
docker-compose -f docker-compose.simple.yml restart

# Полная очистка и перезапуск
docker-compose -f docker-compose.simple.yml down -v
docker-compose -f docker-compose.simple.yml up -d --build
```

## 6. Troubleshooting

### Если spacy не работает:
```bash
# Заходим в контейнер
docker exec -it server-api-server bash

# Проверяем установку spacy
python -c "import spacy; print('spacy OK')"

# Если не работает, пересобираем контейнер
docker-compose -f docker-compose.simple.yml down
docker-compose -f docker-compose.simple.yml up -d --build --force-recreate
```

### Если volumes не работают:
```bash
# Используем минимальную версию без volumes
docker-compose -f docker-compose.minimal.yml up -d --build
```

## 7. Структура volumes

- `./logs` - логи приложения
- `./nginx/ssl` - SSL сертификаты (если нужны)
- `elasticsearch_data` - данные Elasticsearch

## 8. Порты

- `80` - Nginx (основной API)
- `8000` - FastAPI напрямую
- `9200` - Elasticsearch
