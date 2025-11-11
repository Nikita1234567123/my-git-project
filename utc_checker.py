import re
from datetime import datetime


class UTCValidator:
    """
    Класс для проверки и поиска времени в формате UTC
    """

    # Основное регулярное выражение для формата UTC (ISO 8601)
    UTC_PATTERN = r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})?\b'

    @staticmethod
    def is_valid_utc(time_string):
        """
        Проверяет, является ли строка корректным временем в формате UTC
        Использует комбинацию regex и валидации datetime
        """
        # Сначала проверяем базовый синтаксис regex
        pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})?$'
        if not re.match(pattern, time_string):
            return False

        try:
            # Для времени с Z в конце
            if time_string.endswith('Z'):
                dt_str = time_string[:-1]  # Убираем Z
                datetime.fromisoformat(dt_str)
                return True

            # Для времени с временной зоной (+HH:MM или -HH:MM)
            if '+' in time_string or '-' in time_string[10:]:  # Ищем + или - после даты
                # Разделяем основное время и временную зону
                if '+' in time_string:
                    parts = time_string.split('+', 1)
                    dt_str = parts[0]
                    tz_str = '+' + parts[1]
                else:
                    # Находим первый минус после даты (после 10-го символа)
                    minus_pos = time_string.find('-', 10)
                    if minus_pos != -1:
                        dt_str = time_string[:minus_pos]
                        tz_str = time_string[minus_pos:]
                    else:
                        return False

                # Проверяем формат временной зоны
                if not re.match(r'^[+-]\d{2}:\d{2}$', tz_str):
                    return False

                # Проверяем значения часов и минут временной зоны
                tz_hours = int(tz_str[1:3])
                tz_minutes = int(tz_str[4:6])
                if tz_hours > 23 or tz_minutes > 59:
                    return False

                # Парсим основное время
                datetime.fromisoformat(dt_str)
                return True

            return False

        except ValueError:
            return False

    @staticmethod
    def find_utc_in_text(text):
        """
        Находит все вхождения времени в формате UTC в тексте
        и возвращает только валидные
        """
        potential_matches = re.findall(UTCValidator.UTC_PATTERN, text)
        valid_matches = []

        for match in potential_matches:
            if UTCValidator.is_valid_utc(match):
                valid_matches.append(match)

        return valid_matches

    @staticmethod
    def validate_utc_from_file(filename):
        """
        Читает файл и находит все валидные UTC времена
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                return UTCValidator.find_utc_in_text(content)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []