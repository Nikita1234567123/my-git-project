from utc_checker import UTCValidator
import requests
import os
import re


def user_input_mode():
    """Режим пользовательского ввода"""
    print("\n=== Режим пользовательского ввода ===")
    text = input("Введите текст для поиска времени в формате UTC: ")

    # Находим ВСЕ потенциальные совпадения (и валидные и невалидные)
    potential_matches = re.findall(r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})?\b', text)

    if potential_matches:
        print(f"\nНайдено {len(potential_matches)} потенциальных совпадений:")
        valid_count = 0

        for i, match in enumerate(potential_matches, 1):
            is_valid = UTCValidator.is_valid_utc(match)
            status = "✓ ВАЛИДНО" if is_valid else "✗ НЕВАЛИДНО"
            print(f"{i}. {match} - {status}")

            if is_valid:
                valid_count += 1

        print(f"\nИтого: {valid_count} валидных из {len(potential_matches)} найденных")
    else:
        print("Потенциальных совпадений не найдено.")


def url_mode():
    """Режим поиска на веб-странице"""
    print("\n=== Режим поиска на веб-странице ===")
    url = input("Введите URL веб-страницы: ")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        results = UTCValidator.find_utc_in_text(response.text)

        if results:
            print(f"\nНайдено {len(results)} совпадений на странице:")
            for i, match in enumerate(results[:10], 1):  # Показываем первые 10
                is_valid = UTCValidator.is_valid_utc(match)
                status = "✓ ВАЛИДНО" if is_valid else "✗ НЕВАЛИДНО"
                print(f"{i}. {match} - {status}")

            if len(results) > 10:
                print(f"... и еще {len(results) - 10} совпадений")
        else:
            print("Совпадений не найдено.")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")


def file_mode():
    """Режим поиска в файле"""
    print("\n=== Режим поиска в файле ===")
    filename = input("Введите имя файла: ")

    if not os.path.exists(filename):
        print("Файл не найден!")
        return

    results = UTCValidator.validate_utc_from_file(filename)

    if results:
        print(f"\nНайдено {len(results)} совпадений в файле:")
        for i, match in enumerate(results, 1):
            is_valid = UTCValidator.is_valid_utc(match)
            status = "✓ ВАЛИДНО" if is_valid else "✗ НЕВАЛИДНО"
            print(f"{i}. {match} - {status}")
    else:
        print("Совпадений не найдено.")


def main():
    """Главная функция программы"""
    print("🔍 UTC Time Validator")
    print("=" * 30)

    while True:
        print("\nВыберите режим работы:")
        print("1 - Пользовательский ввод")
        print("2 - Поиск на веб-странице")
        print("3 - Поиск в файле")
        print("0 - Выход")

        choice = input("\nВаш выбор: ").strip()

        if choice == '1':
            user_input_mode()
        elif choice == '2':
            url_mode()
        elif choice == '3':
            file_mode()
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()