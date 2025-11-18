"""
Імпортувати бібліотеку NLTK та тексти з електронного архіву текстів Project Gutenberg, для виконання завдань взяти текст, заданий варіантом.
Визначити кількість слів у тексті.
Визначити 10 найбільш вживаних слів у тексті, побудувати на основі цих даних стовпчасту діаграму.
Виконати видалення з тексту стоп-слів та пунктуації, після чого знову знайти 10 найбільш вживаних слів у тексті та побудувати на їх основі стовпчасту діаграму.
"""

import nltk # Імпортування бібліотеки nltk для роботи з текстами
# Імпортування модулів бібліотеки nltk
from nltk.corpus import gutenberg, stopwords
from nltk.probability import FreqDist

import string # Імпортування бібліотеки для обробки символів і рядків
import matplotlib.pyplot as plt # Імпортування модуля pyplot бібліотеки matplotlib для роботи з гістограмами

def words_in_text(words_arg):
    word_count = len(words_arg)
    print(f"\nКількість слів у тексті: {word_count}")
"""
Функція words_in_text(words_arg) виводить на екран кількість слів тексту.
Аргументом функція приймає список всього тексту. 
"""

def common_words(words_arg):
    fdist = FreqDist(words_arg)
    top10 = fdist.most_common(10)
    print("\nТоп-10 найчастіше вживаних слів:")
    print(top10)
    return top10
"""
Функція common_words(words_arg) визначає та повертає списком топ-10 найчастіше вживаних слів.
Аргументом функції є список всього тексту.
Функція повертає список найбільш вживаних слів у тексті.
"""

def create_diagram(top_10_arg):
    plt.figure(figsize=(10, 6))
    plt.bar([w[0] for w in top_10_arg], [w[1] for w in top_10_arg])
    plt.title("Топ-10 слів")
    plt.xlabel("Слово")
    plt.ylabel("Частота")
    plt.show()
"""
Функція create_diagram(top_10_arg) необхідна для побудови гістограми.
Функція приймає як аргумент список з 10-ти найбльш вживаних слів.
"""

def delete_stop_words(words_arg):
    stop_words = set(stopwords.words("english"))
    words_no_stop = [w for w in words_arg if w.lower() not in stop_words]
    print(">-[УВАГА] - Стоп-слова видалено!")
    return words_no_stop
"""
Функція delete_stop_words(words_arg) призначена для видалення стоп-слів.
Аргументом виступає список усіх слів тексту.
Функція повертає список слів тексту, але вже з відсутніми стоп-словами.
"""

def delete_punctuation(words_arg):
    table = str.maketrans('', '', string.punctuation)
    words_no_punct = [w.translate(table) for w in words_arg]
    words_no_punct = [w for w in words_no_punct if w.isalpha()]
    print(">-[УВАГА] - Знаки пунктуації видалено!")
    return words_no_punct
"""
Функція delete_punctuation(words_arg) призначена для видалення знаків пунктуації.
Аргументом виступає список усіх слів тексту.
Функція повертає список слів тексту, але вже з відсутніми знаками пунктуації.
"""

def main():
    top_10 = None
    try:
        nltk.download('gutenberg')
        nltk.download('stopwords')
    except ImportError:
        print(">-[ПОМИЛКА] - Ресурси для роботи не вдалося завантажити!")
        exit()

    print(">-[УВАГА] - Необхідні ресурси завантажено!")

    # Завантаження тексту за варіантом
    words = gutenberg.words('chesterton-ball.txt')
    print(">-[УВАГА] - Текст chesterton-ball.txt зчитано!")
    while True:
        print("\n~~ГОЛОВНЕ МЕНЮ:~~\n>1< - Кількість слів у тексті\n>2< - Вивести топ-10 найчастіших слів\n>3< - Видалення стоп-слів\n>4< - Видалення пунктуації\n>5< - Побудова гістограми\n>0< - Вихід")

        choice = input("Ваш вибір: ")

        if choice == "1":
            words_in_text(words)
        elif choice == "2":
            top_10 = common_words(words)
            print(top_10)
        elif choice == "3":
            words = delete_stop_words(words)
        elif choice == "4":
            words = delete_punctuation(words)
        elif choice == "5":
            if top_10:
                create_diagram(top_10)
            else:
                print(">-[УВАГА] - Перед виконанням цього пункту виконайте пункт 2!")
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