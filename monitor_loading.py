#!/usr/bin/env python3
"""
Скрипт для мониторинга загрузки санкционных данных
"""

import requests
import time
import sys

def get_document_count():
    """Получить количество документов в индексе"""
    try:
        response = requests.get("http://95.217.84.234:9200/sanctions/_count")
        if response.status_code == 200:
            data = response.json()
            return data.get('count', 0)
        else:
            return 0
    except Exception as e:
        print(f"Ошибка получения количества документов: {e}")
        return 0

def main():
    """Основная функция мониторинга"""
    print("🔍 Мониторинг загрузки санкционных данных...")
    print("Цель: 20,795 документов")
    print("-" * 50)
    
    start_time = time.time()
    last_count = 0
    no_progress_count = 0
    
    while True:
        current_count = get_document_count()
        elapsed_time = time.time() - start_time
        
        if current_count > last_count:
            no_progress_count = 0
            rate = current_count / elapsed_time if elapsed_time > 0 else 0
            remaining = 20795 - current_count
            eta = remaining / rate if rate > 0 else 0
            
            print(f"📊 Загружено: {current_count:,} / 20,795 ({current_count/20795*100:.1f}%)")
            print(f"⏱️  Время: {elapsed_time/60:.1f} мин | Скорость: {rate:.1f} док/сек")
            print(f"🕐 Осталось: {eta/60:.1f} мин")
            print("-" * 50)
            
            last_count = current_count
            
            if current_count >= 20795:
                print("✅ Загрузка завершена!")
                break
        else:
            no_progress_count += 1
            if no_progress_count > 10:
                print(f"⚠️  Нет прогресса {no_progress_count} проверок подряд")
                if no_progress_count > 30:
                    print("❌ Загрузка остановлена - нет прогресса")
                    break
        
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Мониторинг остановлен пользователем")
        sys.exit(0)
