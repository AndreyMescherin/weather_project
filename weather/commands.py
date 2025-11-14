"""
Модуль для обработки команд и вывода результатов
"""
import os
import json
import sys

# Абсолютные импорты
try:
    from api import WeatherAPI
    from cache import WeatherCache
except ImportError:
    # Если не работает, пробуем другой путь
    from weather.api import WeatherAPI
    from weather.cache import WeatherCache

def handle_command(args):
    """Обработать команду на основе аргументов"""

    # Если не передано никаких аргументов, показываем справку
    if not any(vars(args).values()):
        print("Для получения справки используйте: python main.py --help")
        print("\nОсновные команды:")
        print("  python main.py --city Москва          # Погода по городу")
        print("  python main.py --coord 55.7558 37.6173 # Погода по координатам")
        print("  python main.py --cache-info           # Информация о кэше")
        print("  python main.py --clear-cache          # Очистить кэш")
        return

    if args.clear_cache:
        clear_cache()
        return

    if args.cache_info:
        show_cache_info()
        return

    # Если не указаны ни город, ни координаты, но есть другие аргументы
    if not args.city and not args.coord:
        print("❌ Для получения погоды укажите --city или --coord")
        print("ℹ️  Используйте --help для просмотра всех опций")
        return

    if args.city:
        get_weather_by_city(args.city)
    elif args.coord:
        latitude, longitude = args.coord
        get_weather_by_coords(latitude, longitude)


def get_weather_by_city(city_name):
    """Получить погоду по названию города"""
    # Сначала получаем координаты города
    print(f"🔍 Поиск координат для города: {city_name}")

    cache_key = f"coords_{city_name.lower()}"
    cached_coords = WeatherCache.get_cached_weather(cache_key)

    if cached_coords:
        print("📍 Координаты найдены в кэше")
        location = cached_coords
    else:
        try:
            location = WeatherAPI.get_coordinates_by_city(city_name)
            WeatherCache.set_cached_weather(cache_key, location)
            print("📍 Координаты получены из API")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return

    print(f"📍 Местоположение: {location['name']}, {location['country']}")
    print(f"📌 Координаты: {location['latitude']:.4f}, {location['longitude']:.4f}")

    # Теперь получаем погоду по координатам
    get_weather_by_coords(location['latitude'], location['longitude'])


def get_weather_by_coords(latitude, longitude):
    """Получить погоду по координатам"""
    cache_key = f"weather_{latitude:.4f}_{longitude:.4f}"
    cached_weather = WeatherCache.get_cached_weather(cache_key)

    if cached_weather:
        print("🌤️  Данные о погоде загружены из кэша")
        weather_data = cached_weather
    else:
        print("🌤️  Запрос данных о погоде...")
        try:
            weather_data = WeatherAPI.get_weather_by_coords(latitude, longitude)
            WeatherCache.set_cached_weather(cache_key, weather_data)
            print("✅ Данные о погоде получены из API")
        except Exception as e:
            print(f"❌ Ошибка при получении погоды: {e}")
            return

    display_weather(weather_data)


def display_weather(weather_data):
    """Отобразить информацию о погоде"""
    current = weather_data['current_weather']

    print("\n" + "=" * 40)
    print("📊 ТЕКУЩАЯ ПОГОДА")
    print("=" * 40)

    temperature = current['temperature']
    windspeed = current['windspeed']
    winddirection = current['winddirection']
    weathercode = current['weathercode']
    time = current['time']

    print(f"🌡️  Температура: {temperature}°C")
    print(f"💨 Скорость ветра: {windspeed} км/ч")
    print(f"🧭 Направление ветра: {winddirection}°")
    print(f"📝 Код погоды: {weathercode}")
    print(f"🕒 Время: {time}")

    # Расшифровка кодов погоды
    weather_description = get_weather_description(weathercode)
    print(f"☁️  Описание: {weather_description}")
    print("=" * 40)


def get_weather_description(weathercode):
    """Получить текстовое описание по коду погоды"""
    codes = {
        0: "Ясно",
        1: "Преимущественно ясно",
        2: "Переменная облачность",
        3: "Пасмурно",
        45: "Туман",
        48: "Туман с инеем",
        51: "Лекая морось",
        53: "Умеренная морось",
        55: "Сильная морось",
        61: "Небольшой дождь",
        63: "Умеренный дождь",
        65: "Сильный дождь",
        80: "Ливень",
        95: "Гроза"
    }
    return codes.get(weathercode, "Неизвестно")


def show_cache_info():
    """Показать информацию о кэше"""
    if not os.path.exists(WeatherCache.CACHE_FILE):
        print("📭 Кэш пуст")
        return

    try:
        with open(WeatherCache.CACHE_FILE, 'r', encoding='utf-8') as f:
            cache = json.load(f)

        print("📊 ИНФОРМАЦИЯ О КЭШЕ")
        print("=" * 30)
        print(f"📁 Файл кэша: {WeatherCache.CACHE_FILE}")
        print(f"📈 Количество записей: {len(cache)}")
        print("\n🗂️  Ключи в кэше:")
        for key in cache.keys():
            cached_time = cache[key]['timestamp']
            print(f"  - {key} (кэшировано: {cached_time})")
    except Exception as e:
        print(f"❌ Ошибка при чтении кэша: {e}")


def clear_cache():
    """Очистить кэш"""
    try:
        if os.path.exists(WeatherCache.CACHE_FILE):
            os.remove(WeatherCache.CACHE_FILE)
            print("✅ Кэш успешно очищен")
        else:
            print("ℹ️  Файл кэша не существует")
    except Exception as e:
        print(f"❌ Ошибка при очистке кэша: {e}")