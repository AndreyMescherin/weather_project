#!/usr/bin/env python3
"""
Главный файл приложения для получения погоды
"""
import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.append(os.path.dirname(__file__))

from weather.parser import create_parser
from weather.commands import handle_command


def main():
    """Основная функция приложения"""
    parser = create_parser()
    args = parser.parse_args()

    try:
        handle_command(args)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()