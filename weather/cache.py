"""
Модуль для кэширования погодных данных
"""
import json
import os
from datetime import datetime, timedelta

class WeatherCache:
    """Класс для управления кэшем погодных данных"""
    
    CACHE_FILE = "weather_cache.json"
    CACHE_DURATION = timedelta(minutes=30)  # Кэшируем на 30 минут
    
    @classmethod
    def _load_cache(cls):
        """Загрузить кэш из файла"""
        try:
            if os.path.exists(cls.CACHE_FILE):
                with open(cls.CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Предупреждение: не удалось загрузить кэш: {e}")
        return {}
    
    @classmethod
    def _save_cache(cls, cache_data):
        """Сохранить кэш в файл"""
        try:
            with open(cls.CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Предупреждение: не удалось сохранить кэш: {e}")
    
    @classmethod
    def get_cached_weather(cls, key):
        """
        Получить кэшированные данные по ключу
        Возвращает None если данных нет или они устарели
        """
        cache = cls._load_cache()
        
        if key in cache:
            cached_data = cache[key]
            cache_time = datetime.fromisoformat(cached_data['timestamp'])
            
            if datetime.now() - cache_time < cls.CACHE_DURATION:
                return cached_data['data']
            else:
                # Удаляем устаревшие данные
                del cache[key]
                cls._save_cache(cache)
        
        return None
    
    @classmethod
    def set_cached_weather(cls, key, data):
        """Сохранить данные в кэш"""
        cache = cls._load_cache()
        
        cache[key] = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        cls._save_cache(cache)