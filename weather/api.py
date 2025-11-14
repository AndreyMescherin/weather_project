"""
Модуль для работы с API погоды
"""
import requests
import json
from datetime import datetime

class WeatherAPI:
    """Класс для работы с Open-Meteo API"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    @staticmethod
    def get_weather_by_coords(latitude, longitude):
        """
        Получить погоду по координатам
        """
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current_weather': 'true',
                'timezone': 'auto'
            }
            
            response = requests.get(WeatherAPI.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка API запроса: {e}")
    
    @staticmethod
    def get_coordinates_by_city(city_name):
        """
        Получить координаты по названию города
        Используем Open-Meteo Geocoding API
        """
        try:
            geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
            params = {
                'name': city_name,
                'count': 1,
                'language': 'ru',
                'format': 'json'
            }
            
            response = requests.get(geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('results'):
                raise Exception(f"Город '{city_name}' не найден")
            
            location = data['results'][0]
            return {
                'latitude': location['latitude'],
                'longitude': location['longitude'],
                'name': location['name'],
                'country': location.get('country', 'N/A')
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка геокодирования: {e}")