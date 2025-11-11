import unittest
from utc_checker import UTCValidator


class TestUTCValidator(unittest.TestCase):
    """Тесты для валидатора UTC времени"""

    def test_valid_utc_formats(self):
        """Тестирование валидных форматов UTC"""
        valid_cases = [
            "2023-12-25T14:30:00Z",
            "2023-12-25T14:30:00+03:00",
            "2023-12-25T14:30:00-05:00",
            "2023-12-25T14:30:00.123Z",
            "2023-12-25T14:30:00.456789+03:00",
            "2023-12-25T00:00:00Z",
            "2023-12-25T23:59:59Z",
            "2023-12-25T14:30:00+00:00",  # UTC+0
            "2023-02-28T14:30:00Z",  # Валидная дата (не високосный год)
        ]

        for case in valid_cases:
            with self.subTest(case=case):
                self.assertTrue(UTCValidator.is_valid_utc(case), f"Ошибка в случае: {case}")

    def test_invalid_utc_formats(self):
        """Тестирование невалидных форматов UTC"""
        invalid_cases = [
            "2023-12-25 14:30:00",  # пробел вместо T
            "2023-12-25T14:30:00",  # отсутствует зона
            "2023-12-25T25:30:00Z",  # неверный час (25)
            "2023-12-25T14:60:00Z",  # неверные минуты (60)
            "2023-12-25T14:30:99Z",  # неверные секунды (99)
            "2023-13-25T14:30:00Z",  # неверный месяц (13)
            "2023-12-32T14:30:00Z",  # неверный день (32)
            "2023-12-25T14:30:00+25:00",  # неверная временная зона (+25)
            "2023-12-25T14:30:00+00:60",  # неверные минуты в зоне (60)
            "hello world",  # произвольный текст
            "12345",  # числа
            "2023/12/25T14:30:00Z",  # неправильный разделитель даты
            "2023-02-30T14:30:00Z",  # 30 февраля
            "2023-04-31T14:30:00Z",  # 31 апреля
        ]

        for case in invalid_cases:
            with self.subTest(case=case):
                self.assertFalse(UTCValidator.is_valid_utc(case), f"Ошибка в случае: {case}")

    def test_find_utc_in_text(self):
        """Тестирование поиска UTC в тексте"""
        test_text = """
        Лог событий:
        2023-12-25T14:30:00Z - событие 1
        2023-12-25T15:45:00+03:00 - событие 2
        Невалидное время: 2023-12-25T25:30:00Z (не должно найтись)
        Еще одно: 2023-12-25T10:30:00.123Z
        И еще невалидное: 2023-12-25T14:30:00 (без зоны)
        """

        results = UTCValidator.find_utc_in_text(test_text)
        expected = [
            "2023-12-25T14:30:00Z",
            "2023-12-25T15:45:00+03:00",
            "2023-12-25T10:30:00.123Z"
        ]

        self.assertEqual(results, expected)
        # Проверим, что невалидные не попали в результаты
        self.assertNotIn("2023-12-25T25:30:00Z", results)
        self.assertNotIn("2023-12-25T14:30:00", results)

    def test_empty_text(self):
        """Тестирование пустого текста"""
        self.assertEqual(UTCValidator.find_utc_in_text(""), [])
        self.assertEqual(UTCValidator.find_utc_in_text("   "), [])

    def test_no_matches(self):
        """Тестирование текста без совпадений"""
        text = "Это текст без времени в формате UTC"
        self.assertEqual(UTCValidator.find_utc_in_text(text), [])


if __name__ == '__main__':
    unittest.main()
