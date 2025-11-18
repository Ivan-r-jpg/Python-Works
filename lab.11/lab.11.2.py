"""
Створіть датафрейм з даними використання велодоріжок за 2010 рік.
Визначте загальну кількість велосипедистів за рік на усіх велодоріжках
Визначте загальну кількість велосипедистів за рік на кожній велодоріжці.
Визначте, який місяць найбільш популярний у велосипедистів, на кожній з трьох з обраних велодоріжок.
Побудуйте графік завантаженості однієї з велодоріжок по місяцях.
"""

import pandas as pd # Імпортування бібліотеки pandas для роботи з датафреймом
import matplotlib.pyplot as plt # Імпортування модуля pyplot бібліотеки matplotlib для роботи з графіками

def test(df_arg):
    print("\nТестування датафрайму (Чи коректно зчитався файл):\n")
    print(df_arg.head())
    print(df_arg.info())
    print(df_arg.describe())
"""
Функція test(df_arg) виводить на екран перші рядки датафрейму, інформацію про типи даних та описову статистику. 
Використовується для перевірки структури та коректності завантаження даних.
"""

def create_lanes(df_arg):
    bike_lanes = df_arg.select_dtypes(include='number').columns
    return bike_lanes
"""
Функція create_lanes(df_arg) отримує на вхід датафрейм і за допомогою 
select_dtypes(include='number') вибирає всі стовпці, що містять числові значення. 
Оскільки дані про кількість велосипедистів є числовими, функція повертає 
імена саме тих стовпців, які відповідають велодоріжкам.
"""

def print_bike_lanes(df_arg):
    bike_lanes = create_lanes(df_arg)
    print(f"Визначено велодоріжки: {list(bike_lanes)}")
"""
Функція print_bike_lanes(df_arg) виводе на екран список назв всіх доступних велодоріжок.
У аргументах функції приймається датафрейм.
"""

def total_sum(df_arg):
    bike_lanes = create_lanes(df_arg)
    total = df_arg[bike_lanes].sum().sum()
    print(f"Загальна кількість велосипедистів за рік: {int(total)}")
"""
Функція total_sum(df_arg) розраховує загальну суму кількості велосипедистів на усіх велодоріжках за рік.
Аргументом функції виступає датафрейм.
"""

def lane_sum(df_arg):
    bike_lanes = create_lanes(df_arg)
    lane_totals = df_arg[bike_lanes].sum().sort_values(ascending=False).astype(int)
    print(lane_totals)
"""
Функція lane_sum(df_arg) обчислює та виводить суму велосипедистів для кожної велодоріжки окремо. 
Сортує результати за спаданням.
Аргументом функції є датафрейм.
"""

def popularity(df_arg):
    bike_lanes = create_lanes(df_arg)
    for i, lane in enumerate(bike_lanes, 1):
        print(f"{i}. {lane}")

    chosen_lanes = []
    while len(chosen_lanes) < 3:
        print("-" * 30)
        choice = input(f"Залишилось обрати {3 - len(chosen_lanes)}\n{'-' * 30}\nВведіть назву доріжки: ")
        if choice in bike_lanes and choice not in chosen_lanes:
            chosen_lanes.append(choice)
            print(f"Додано: {choice}")
        else:
            print(">-[УВАГА] - Помилка вибору!\n(Спробуйте ще раз)")
    print("\n--- Ваш вибір ---")
    print(", ".join(chosen_lanes))
    print("-" * 40)
    df_arg['Month'] = df_arg['Date'].dt.month_name(locale='uk_UA')
    monthly_data = df_arg.groupby('Month')[chosen_lanes].sum()
    print("\nМісячна статистика:")
    print(monthly_data)
    print("\nНайпопулярніші місяці:")
    print(monthly_data.idxmax())
"""
Функція popularity(df_arg) пропонує користувачу вибрати три велодоріжки, 
після чого обчислює кількість велосипедистів по місяцях для кожної з них та визначає найпопулярніший місяць для кожної велодоріжки окремо.
Аргументом функції передається датафрейм.
"""

def graph(df_arg):
    bike_lanes = create_lanes(df_arg)
    print("\nПо якій доріжці побудувати графік завантаженості по місяцях?")
    for i, lane in enumerate(bike_lanes, 1):
        print(f"{i}. {lane}")

    while True:
        lane_choice = input("Введіть назву доріжки: ")
        if lane_choice in bike_lanes:
            break
        print(">-[УВАГА] - Некоректно введені дані!\n(Спробуйте ще раз)")

    # Створення колонки з місяцями
    df_arg['Month'] = df_arg['Date'].dt.month_name(locale='uk_UA')

    # Групування по місяцях
    monthly_sum = df_arg.groupby('Month')[lane_choice].sum()
    months_order = [
        'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
        'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'
    ]
    monthly_sum = monthly_sum.reindex(months_order)
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_sum.index, monthly_sum.values, marker='o')
    plt.title(f"Завантаженість велодоріжки по місяцях: {lane_choice}")
    plt.xlabel("Місяць")
    plt.ylabel("Кількість велосипедистів")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
"""
Функція graph(df_arg) потрібна для побудови графіка завантаженості вибраної велодоріжки за рік. 
Аргументом потрібно передавати датафрейм.
"""

def main():
    df = pd.read_csv('comptagevelo2010.csv')
    try:
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        print("Стовпець 'Date' успішно перетворено у datetime!")
    except ValueError:
        print(">-[УВАГА] - Помилка перетворення дати!")
        exit()
    while True:
        print("\n~~ГОЛОВНЕ МЕНЮ:~~\n>1< - Тестування датафрейму\n>2< - Визначити загальну кількість велосипедистів за рік\n>3< - Визначити загальну кількість велосипедистів за кожною велодоріжкою\n>4< - Визначити найпопулярніші місяці на трьох обраних велодоріжках\n>5< - Побудувати графік завантаженості велодоріжки\n>6< - Вивести на екран усі доступні велодоріжки\n>0< - Вихід")

        choice = input("Введіть ваш вибір: ")

        if choice == "1":
            test(df)
        elif choice == "2":
            total_sum(df)
        elif choice == "3":
            lane_sum(df)
        elif choice == "4":
            popularity(df)
        elif choice == "5":
            graph(df)
        elif choice == "6":
            print_bike_lanes(df)
        elif choice == "0":
            print("\n>-Роботу завершено...")
            break
        else:
            print(">-[УВАГА] - Неправильний вибір, спробуйте ще раз!")
"""
Функція main() - головна функція програми, у ній використовуються всі функції та ведеться діалог з користувачем.
"""

# Запуск програми
main()
