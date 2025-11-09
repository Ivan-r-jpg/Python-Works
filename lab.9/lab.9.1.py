"""
Знайти дані Population, total для України за 1991-2019 роки. Вивести вміст .csv файлу на екран.
Організувати пошук найнижчого та найвищого значень показника та записати результат пошуку у новий .csv файл.
"""

import csv # Підключення модуля для роботи з CSV файлами

try:
    with open("lab.csv", "r", encoding='utf-8') as file: # Відкриття файлу lab.csv у режимі читання, використовуючи конструкцією with
        print("[УВАГА] - Файл lab.csv було відкрито у режимі читання!")
        reader = csv.DictReader(file, delimiter=';') # Зчитування CSV файлу, розділеного крапкою з комою та створення ітератора
        rows = list(reader)  # Перетворення ітератора в список, тепер ітерувати можна кілька разів

    # Формування списку числових значень (ігнорування пустих/нечислових)
    values = []
    print("Вміст CSV файлу:")
    # Додання у список значень зі стовпця Value
    for r in rows:
        print(r)
        v = r.get('Value', '').strip()
        if v != '':
            try:
                values.append(float(v))
            except ValueError:
                print("[ПОМИЛКА] - Виникла критична помилка при виконанні цього блоку коду!")
    # Якщо список не порожній
    if values:
        min_value = min(values) # Знаходження найменшого числа
        max_value = max(values) # Знаходження найбільшого числа
        # Знаходження рядків, в яких лежать найменше і найбільше значення
        min_rows = []
        for r in rows:
            if r.get('Value', '').strip() != '' and float(r['Value']) == min_value:
                min_rows.append(r)
        max_rows = []
        for r in rows:
            if r.get('Value', '').strip() != '' and float(r['Value']) == max_value:
                max_rows.append(r)
        # Проходження по рядку з найменшим значенням
        print("РЕЗУЛЬТАТ:")
        for mr in min_rows:
            min_time = mr.get('Time')
            print(f"Мінімальне значення - {min_value} знайдено у {mr.get('Time')} році")
        # Проходження по рядку з найбільшим значенням
        for ms in max_rows:
            max_time = ms.get('Time')
            print(f"Максимальне значення - {max_value} знайдено у {ms.get('Time')} році")
        try:
            with open("lab9.csv", "w", encoding='utf-8', newline='') as f: # Відкриття файлу lab9.csv у режимі запису, використовуючи конструкцією with
                print("[УВАГА] - Файл lab9.csv було відкрито у режимі запису!")
                fieldnames = ['Time', 'Value'] # Іменування стовпців
                # Створення ітератора для запису та запис даних у новий CSV файл
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerow({'Time': max_time, 'Value': max_value})
                writer.writerow({'Time': min_time, 'Value': min_value})
                print("[УВАГА] - Результат успішно записано у файл lab9.csv!")
        except FileNotFoundError:
            print("[ПОМИЛКА] - Файл 'lab9.csv' не знайдено!")
    else:
        print("[УВАГА] - Не знайдено числових значень у колонці 'Value'!")

except FileNotFoundError:
    print("[ПОМИЛКА] - Файл 'lab.csv' не знайдено!")
