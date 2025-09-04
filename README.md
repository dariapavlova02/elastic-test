# Payment Vector Testing - Server Deployment

Система для тестирования векторного поиска по санкционным спискам с использованием Elasticsearch и AI-сервиса.

## Архитектура

- **Сервер**: AI-сервис + Elasticsearch + Search API
- **Локально**: Загрузка данных санкций, отправка запросов для поиска
- **Поток**: Запрос → Нормализация → Векторизация → Поиск → Результаты

## Компоненты

### Серверные файлы
- `server_search_api_final.py` - Основной API для поиска на сервере
- `Dockerfile.server` - Docker-образ для сервера
- `docker-compose.server.yml` - Оркестрация сервисов на сервере
- `nginx/server-nginx.conf` - Конфигурация Nginx

### Локальные файлы
- `final_search_client.py` - Клиент для отправки запросов
- `load_sanctions_to_elasticsearch.py` - Загрузка данных санкций
- `Makefile.final` - Команды для управления

### Исходный код
- `src/` - Основная логика приложения
- `config/` - Конфигурация
- `ai-service/` - AI-сервис для нормализации и векторизации

## Использование

### 1. Деплой сервера
```bash
# Сборка и запуск всех сервисов
make -f Makefile.final build-server
make -f Makefile.final up-server

# Проверка здоровья
make -f Makefile.final health-server
```

### 2. Загрузка данных санкций (локально)
```bash
# Загрузка предварительно векторизованных данных санкций
make -f Makefile.final load-sanctions-local
```

### 3. Тестирование поиска
```bash
# Отправка запроса на поиск
make -f Makefile.final search-server

# Или напрямую
python final_search_client.py --api-url http://localhost:8000 --query "Петро Порошенко"
```

## Пример работы

1. Отправляем запрос: "Петро Порошенко"
2. AI-сервис нормализует и векторизует запрос
3. Elasticsearch ищет похожие векторы в индексе санкций
4. Возвращаем результаты с оценками схожести

## Переменные окружения

- `ELASTICSEARCH_HOSTS` - URL Elasticsearch (по умолчанию: http://localhost:9200)
- `AI_SERVICE_URL` - URL AI-сервиса (по умолчанию: http://localhost:8001)

## Структура проекта

```
.
├── src/                          # Основная логика
├── config/                       # Конфигурация
├── ai-service/                   # AI-сервис
├── nginx/                        # Конфигурация Nginx
├── server_search_api_final.py    # API сервера
├── final_search_client.py        # Клиент поиска
├── load_sanctions_to_elasticsearch.py  # Загрузка данных
├── Dockerfile.server             # Docker для сервера
├── docker-compose.server.yml     # Оркестрация
├── Makefile.final               # Команды управления
└── requirements.txt             # Зависимости Python
```
