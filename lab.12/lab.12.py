"""
Аналіз відтінків текстових повідомлень (sentiment analysis) з Twitter або іншого джерела.
Визначення емоційного забарвлення повідомлень за допомогою NLTK, TextBlob або VADER.
"""

import pandas as pd # Імпортування бібліотеки pandas, необхідної для роботи з датафреймом
import matplotlib.pyplot as plt # Імпортування модуля pyplot бібліотеки matplotlib, необхідного для побудови гістограми
from textblob import TextBlob # Імпортування класу textblob бібліотеки TextBlob для роботи з аналізом емоційного забарвлення повідомлення
import nltk # Імпортування бібліотеки nltk для роботи з текстом
from nltk.sentiment.vader import SentimentIntensityAnalyzer # Імпортування класу модуля Vader бібліотеки nltk для роботи з аналізом емоційного забарвлення повідомлення
import re # Імпортування модуля re, необхідного для роботи з регулярними виразами
import os # Імпортування бібліотеки os, необхідної для взаємодії з операційною системою
from datetime import datetime # Імпортування класу datetime модуля datetime для створення об'єкту, що містить дані поточного часу

def clean_text(text):
    text = str(text) # Перетворення рядка на тип str
    # Очищення тексту від зайвих символів
    text = re.sub(r'http\S+|www\.\S+', '', text) # Видалення посилань
    text = re.sub(r'@\w+', '', text) # Видалення згадувань (@user)
    text = re.sub(r'#', '', text)  # Видалення хештегів (залишаємо слово)
    text = re.sub(r'\b\d+\b', '', text) # Видалення ізольованих цифр у кінці
    text = re.sub(r'\s+', ' ', text).strip() # Прибирання зайвих пробілів
    return text # Повернення очищеного тексту
"""
Функція clean_text(text) необхідна для очищення рядків повідомлень від зайвого тексту, такого як: посилання, теги людей, хештеги, цифри...
У аргументах функція приймає елемент датафрейму - символьний рядок.
Як результат функція повертає оновлений, очищений рядок.
"""

def analyze_vader(texts):
    sid = SentimentIntensityAnalyzer() # Створення об'єкту класу Vader
    results = [] # Створення порожнього списку для збереження результатів аналізу відтінків текстових повідомлень
    # Перебір списку по повідомленнях
    for t in texts:
        score = sid.polarity_scores(t) # Створення словника score з результатами аналізу повідомлення
        compound = score['compound'] # Визначення значення compound зі словника score
        label = 'neutral' # Задання дефолтного значення для загального настрою повідомлення
        if compound >= 0.05: # Умовний оператор if, якщо compound >= 0.05, то повідомлення вважається позитивним
            label = 'positive'
        elif compound <= -0.05: # Умовний оператор if, якщо compound <= 0.05, то повідомлення вважається негативним
            label = 'negative'

        score['label'] = label # Додання нового рядка у словник score з оцінкою настрою повідомлення
        results.append(score) # Додання результату у список results
    return results # Повернення списку
"""
Функція analyze_vader(texts) необхідна для аналізу емоційного забарвлення повідомлення за допомогою використання бібліотеки Vader.
У аргументах функція приймає список рядків.
Функція повертає результати аналізу повідомлення у вигляді списку.
"""

def analyze_textblob(texts):
    results = [] # Створення порожнього списку для збереження результатів аналізу відтінків текстових повідомлень
    # Перебір списку по повідомленнях
    for t in texts:
        tb = TextBlob(t) # Аналіз повідомлення
        polarity = tb.polarity # Занесення значення polarity до відповідної змінної
        label = 'neutral' # Задання дефолтного значення для загального настрою повідомлення
        if polarity > 0.05: # Умовний оператор if, якщо compound > 0.05, то повідомлення вважається позитивним
            label = 'positive'
        elif polarity < -0.05:
            label = 'negative' # Умовний оператор if, якщо compound < 0.05, то повідомлення вважається негативним
        # Додання результатів у список results, елементами якого є словник
        results.append({
            'polarity': polarity,
            'subjectivity': tb.subjectivity,
            'label': label
        })
    return results # Повернення списку
"""
Функція analyze_textblob(texts) необхідна для аналізу емоційного забарвлення повідомлення за допомогою використання бібліотеки TextBlob.
У аргументах функція приймає список рядків.
Функція повертає результати аналізу повідомлення у вигляді списку.
"""

def main():
    now = datetime.now() # Визначення поточних дати та часу

    try:
        nltk.download('vader_lexicon', quiet=True) # Завантаження лексикону для Vader
    except OSError:
        print("\n>-[ПОМИЛКА] - Невдала спроба завантажити необхідні для роботи ресурси!")
        exit() # Аварійне завершення програми

    print("\n>-[УВАГА] - Усі необхідні ресурси для роботи завантажено!")

    default_path = 'obama.csv' # Визначення стандартного CSV-файлу програми
    path_input = input(f"Введіть шлях до CSV-файлу (за замовчуванням '{default_path}'): ").strip() # Введення користувачем назви бажаного CSV-файлу для аналізу
    path = path_input if path_input else default_path # Якщо нічого не введено, то використовується стандартний CSV-файл

    # Перевірка чи існує csv-файл
    if not os.path.isfile(path):
        print(f"\n>-[ПОМИЛКА] - Файл '{path}' не знайдено!\n(Аварійне завершення програми...)")
        exit() # Аварійне завершення програми

    # Читання CSV-файлу
    try:
        df = pd.read_csv(path, lineterminator='\n')
    except FileNotFoundError:
        df = pd.read_csv(path)

    # Визначення колонки з текстом
    target_column = None
    priority_columns = ['Embedded_text', 'Text', 'tweet', 'Tweet', 'text'] # Пріоритетні точні назви (на випадок, якщо використовуються різні файли)
    # Пошук колонки з відповідною назвою
    for col in priority_columns:
        if col in df.columns:
            target_column = col
            break
    # Якщо точних назв немає, пошук схожих
    if target_column is None:
        possible_cols = [c for c in df.columns if 'text' in c.lower() or 'tweet' in c.lower()]
        if possible_cols:
            target_column = possible_cols[0] # Якщо знайдеться кілька колонок, що мають у назві слово text чи tweet, то програма бере першу, яка зустрінеться
    # Якщо нічого не знайдено
    if target_column is None:
        print("\n>-[УВАГА] - Не знайдено колонку з текстом повідомлень!")
        print("\nДоступні колонки:", list(df.columns))
        exit() # Аварійне завершення програми

    print(f"\n>-[УВАГА] - Використовується колонка: '{target_column}'")

    # Очищення тексту від зайвих символів
    print("\n>-[УВАГА] - Очищення тексту від зайвих символів...")

    df['clean_text'] = df[target_column].apply(clean_text) # Очищення рядків від зайвого вмісту
    df = df[df['clean_text'].str.strip().astype(bool)].reset_index(drop=True) # Видалення пустих рядків та переіндексація існуючих

    # Аналіз повідомлень на тональність
    print(f"\nОберіть метод аналізу повідомлень з файлу {path}:\n1) VADER\n2) TextBlob\n")

    while True:
        method = input("Введіть 1 або 2: ").strip()
        if method in ['1', '2']:  # Умовний оператор if, перевірка, чи ввід є у списку дозволених варіантів
            break  # Вихід з циклу

        print("\n>-[УВАГА] - Неправильний вибір!\n(Будь ласка, введіть тільки 1 або 2)")

    if method == '1':
        print("\n>-[УВАГА] - Аналіз VADER...")

        results = analyze_vader(df['clean_text'].tolist()) # Перетворення датафрейму на список та аналіз текстового повідомлення за допомогою бібліотеки Vader
        rtext = "VADER"
    else:
        print("\n>-[УВАГА] - Аналіз TextBlob...")

        results = analyze_textblob(df['clean_text'].tolist()) # Перетворення датафрейму на список та аналіз текстового повідомлення за допомогою бібліотеки textblob
        rtext = "TextBlob"

    results_df = pd.DataFrame(results) # Перетворення результату на датафрейм
    final_df = pd.concat([df, results_df], axis=1) # об’єднує два датафрейми поруч один з одним (по колонках).

    # Виведення статистики
    print("\nРозподіл тональності...")

    counts = final_df['label'].value_counts()
    print(counts)

    print("\nПобудова гістограми...")

    # Побудова графіку
    plt.figure(figsize=(8, 6)) # Визначення розміру полотна
    # Створення словника для збереження значень кольору для кожного емоційного забарвлення повідомлення
    color_map = {
        'negative': 'red',
        'positive': 'green',
        'neutral': 'gray'
    }
    counts.plot(kind='bar', color=[color_map[i] for i in counts.index]) # Побудова гістограми
    # Введення позначень на гістограмі
    plt.title(f'Розподіл тональності (Файл {path})', fontweight = 'bold', fontsize = 16)
    plt.xlabel('Тональність', fontsize = 16)
    plt.ylabel('Кількість повідомлень', fontsize = 16)
    plt.tight_layout()
    plt.savefig('sentiment_distribution.png')
    plt.show()

    print("\n>-[УВАГА] - Графік збережено як 'sentiment_distribution.png'!")

    # Вибір формату збереження аналізу
    print("\nОберіть формат збереження результату:\n1) CSV\n2) JSON")

    while True:
        fmt = input("\nВведіть 1 або 2: ").strip()
        if fmt in ['1', '2']:  # Перевірка, чи ввід є у списку дозволених варіантів
            break  # Вихід з циклу
        print("\n>-[УВАГА] - Неправильний вибір!\n(Будь ласка, введіть тільки 1 або 2)")

    # Запис результату у CSV-файл
    if fmt == '1':
        try:
            final_df.to_csv('sentiment_results.csv', index=False)
        except FileNotFoundError:
            print("\n>-[ПОМИЛКА] - Невдала спроба зберегти результат в окремий CSV-файл!")
            exit() # Аварійне завершення програми

        print("\n>-[УВАГА] - Результати збережено у 'sentiment_results.csv'!")

    # Запис результату у JSON-файл
    else:
        try:
            final_df.to_json(
                'sentiment_results.json',
                orient='records',
                force_ascii=False,
                indent=4
            )
        except FileNotFoundError:
            print(">-[ПОМИЛКА] - Невдала спроба зберегти результат в окремий JSON-файл!")
            exit() # Аварійне завершення програми

        print("\n>-[УВАГА] - Результати збережено у 'sentiment_results.json'!")

    # Запис результату у текстовий файл
    print("\n>-[УВАГА] - Результат записується у файл 'result.txt'...")

    try:
        with open("result.txt", 'a+', encoding = "utf-8") as f:
            f.write(f"{"-" * 30}\nРЕЗУЛЬТАТ:\nЧас: {now}\nВикористаний файл: {path}\nАналіз відтінків текстових повідомлень за {rtext}:\n{counts}\n{"-" * 30}\n")
    except FileNotFoundError:
        print("\n>-[ПОМИЛКА] - Не вдалося відкрити файл 'result.txt' для запису!")
        exit() # Аварійне завершення програми

    print("\n>-[УВАГА] - Результат записано у файл 'result.txt'!")
"""
Функція main() - головна функція програми, саме в ній відображений весь алгоритм виконання програми.
"""

# Виклик функції main()
main()
