"""
Модуль для обработки аргументов командной строки
"""
import argparse

def create_parser():
    """Создать парсер аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Получение текущей погоды по городу или координатам",
        epilog="Примеры использования:\n"
               "  python main.py --city Москва\n"
               "  python main.py --coord 55.7558 37.6173\n"
               "  python main.py --city Лондон --cache-info\n"
               "  python main.py --clear-cache",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--city',
        type=str,
        help='Название города (например: "Москва")'
    )
    group.add_argument(
        '--coord',
        nargs=2,
        type=float,
        metavar=('LAT', 'LON'),
        help='Координаты (широта и долгота, например: 55.7558 37.6173)'
    )
    
    parser.add_argument(
        '--cache-info',
        action='store_true',
        help='Показать информацию о кэше'
    )
    
    parser.add_argument(
        '--clear-cache',
        action='store_true',
        help='Очистить кэш'
    )
    
    return parser