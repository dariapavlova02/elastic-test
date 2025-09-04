#!/bin/bash

echo "🔍 Проверка прогресса загрузки санкционных данных..."
echo "Цель: 20,795 документов"
echo "----------------------------------------"

while true; do
    count=$(curl -s "http://95.217.84.234:9200/sanctions/_count" | grep -o '"count":[0-9]*' | cut -d: -f2)
    if [ -n "$count" ]; then
        percentage=$(echo "scale=1; $count * 100 / 20795" | bc)
        echo "📊 Загружено: $count / 20,795 ($percentage%)"
        
        if [ "$count" -ge 20795 ]; then
            echo "✅ Загрузка завершена!"
            break
        fi
    else
        echo "❌ Ошибка получения данных"
    fi
    
    sleep 10
done
