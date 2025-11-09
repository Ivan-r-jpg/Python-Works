"""
Задано дані про зріст n=10 учнів класу, впорядковані за зменшенням
(немає жодної пари учнів, які мають однаковий зріст).
Скласти програму, яка визначає чи перевищує сумарний зріст дівчат у класі зріст хлопців.
"""
import json # Підключення модуля для роботи з json файлами

def search(students):
    while True:
        try:
            choose = int(input("-----ПІДМЕНЮ:-----\nОберіть за яким полем бажаєте знайти учня:\n1 - За прізвищем;\n2 - За ростом;\n0 - Вийти з підменю.\nОберіть пункт підменю: "))
            if choose == 1:
                lastname = str(input("Введіть прізвище учня: "))
                if lastname in students:
                    value = students[lastname]
                    print(f"{lastname} - {value.get('Стать')}, {value.get('Зріст')} см")
                else:
                    print("[УВАГА] - Такого учня не існує!")
            elif choose == 2:
                height = int(input("Введіть зріст учня: "))
                found = False
                print("\n[РЕЗУЛЬТАТИ ПОШУКУ]:")
                for name, info in students.items():
                    if info.get("Зріст") == height:
                        found = True
                        print(f"{name} — {info['Стать']}, {info['Зріст']} см")
                if not found:
                    print("[Увага] -Учнів із таким ростом не знайдено!")
            elif choose == 0:
                break
            else: print("[УВАГА] - Обрано неіснуючий варіант\nВведіть, будь ласка, ще раз!")
        except ValueError:
            print("[ПОМИЛКА] - Виникла критична помилка при виконанні цього блоку коду!")
"""
Функція search(), необхідна для пошуку учня за вибраним критерієм.
Оброблює виключні ситуації.
У аргументах приймає словник. 
"""

def print_dict(student):
    for key, value in student.items():
        print(f"{key}:")
        print(f"Зріст: {value.get("Зріст")}\nСтать: {value.get("Стать")}")
"""
Функція print_dict(), необхідна для виведення словника.
У аргументах приймає словник. 
"""

def input_student(student):
    # Введення прізвища учня
    name = input("Введіть прізвище учня, якого бажаєте додати: ").strip()
    while name in student:
        print("[Увага] - Учень із таким прізвищем уже існує!")
        name = input("Введіть інше прізвище: ").strip()

    # Введення зросту

    try:
        height = int(input(f"Введіть зріст учня {name} (у см): "))

        # Створення списку зростів
        existing_heights = []
        for info in student.values():
            existing_heights.append(info.get("Зріст"))

        while height <= 0 or height in existing_heights:
            if height <= 0:
                print("[ПОМИЛКА] - Ріст має бути додатнім числом!")
            elif height in existing_heights:
                print("[ПОМИЛКА] - Учень із таким ростом уже існує!")

            height = int(input(f"Введіть зріст учня {name} (у см): "))

    except ValueError:
        print("[ПОМИЛКА] - введіть ціле число (наприклад, 175)!")
    # Введення статі
    while True:
        sex = input(f"Введіть стать учня {name} (М/Ж): ").strip().capitalize()
        if sex in ["М", "Ж"]:
            break
        else:
            print("[ПОМИЛКА] - Введіть лише 'Ч' або 'Ж'!")

    # Додавання у словник у правильному форматі
    student[name] = {"Зріст": height, "Стать": sex}
    print(f"Учня {name} ({sex}, {height} см) успішно додано!")
"""
Функція input_student(), необхідна для вставки учня у словник.
Оброблює виключні ситуації.
У аргументах приймає словник. 
"""

def delete(student):
    name = str(input("Введіть прізвище учня, інформацію про якого бажаєте видалити: ")) # Введення ім'я учня, якого треба видалити
    try:
        del student[name] # Видалення учня
        print(f"Учня {name} успішно видалено!")
    except KeyError:
        print(f"[УВАГА] - Учня з прізвищем {name} не знайдено!")
"""
Функція delete(), необхідна для видалення учня зі словника.
Оброблює виключні ситуації.
У аргументах приймає словник. 
"""

def sorted_student(student):
    student = dict(sorted(student.items(), key=lambda x: x[1]["Зріст"], reverse=True)) # Сортування словника за оберненим порядком
    return student # Повернення результату
"""
Функція sorted_student(), необхідна для сортування словника за спаданням критерію росту.
У аргументах приймає словник. 
"""

def sum_height(student):
    # Ініціалізація змінних для збереження сум
    sum_girls = 0
    sum_boys = 0
    # Визначення статі учня
    for key, value in student.items():
        if value.get("Стать")=="Ч":
            sum_boys+=value.get("Зріст")
        elif value.get("Стать")=="Ж":
            sum_girls+=value.get("Зріст")
    print(f"Сумарний зріст дівчаток: {sum_girls}\nСумарний зріст хлопчиків: {sum_boys}")
    if(sum_girls > sum_boys):
        print("Зріст дівчаток перевищує зріст хлопчиків")
    elif (sum_boys > sum_girls):
        print("Зріст хлопчиків перевищує зріст дівчаток")
    else:
        print("Сумарний зріст однаковий")
"""
Функція sum_height(), необхідна для визначення перевагу в рості серед хлопчиків та дівчаток.
У аргументах приймає словник. 
"""


def main():
    try:
        with open("student.json", "r", encoding="utf-8") as f: # Відкриття файлу student.json у режимі читання, використовуючи конструкцією with
            print("[УВАГА] - Файл student.json було відкрито у режимі читання!")
            data = json.load(f) # Зчитування файлу
            while True:
                print("-----ГОЛОВНЕ МЕНЮ:-----\n1 - Вивести відсортований словник на екран;\n2 - Додати учня до словника;\n3 - Видалити учня;\n4 - Знайти учня за значенням на вибір;\n5 - Визначити перевагу в рості дітей;\n0 - Завершити програму.\n")
                choose = str((input("Введіть пункт меню: ")))
                if choose == "1":
                    sorted_data = sorted_student(data)
                    print_dict(sorted_data)
                elif choose == "2":
                    input_student(data)
                elif choose == "3":
                    delete(data)
                elif choose == "4":
                    search(data)
                elif choose == "5":
                    sum_height(data)
                elif choose == "0":
                    with open("new_student.json", "w", encoding="utf-8") as f1:  # Відкриття файлу student.json у режимі читання, використовуючи конструкцією with
                        print("[УВАГА] - Файл new_student.json було відкрито у режимі запису!")
                        json.dump(sorted_student(data), f1, ensure_ascii=False, indent=4)  # запис у новий файл
                    print("[УВАГА] - Результат успішно записано у файл new_student.json!")
                    break
                else: print("[УВАГА] - Обрано неіснуючий варіант\nВведіть, будь ласка, ще раз!")
    except FileNotFoundError:
        print("[ПОМИЛКА] - Файл 'student.json' не знайдено!")
main()
