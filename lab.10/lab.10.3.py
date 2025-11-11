"""
Побудуйте кругову діаграму на основі даних з предметної області лабораторної роботи №12.
Використайте бібліотеку Matplotlib.
На круговій діаграмі мають відображатися значення показників у відсотках, наприклад, відсоток дівчат та хлопців,
які навчаються у певному класі,
сектори діаграми повинні бути розфарбовані в різний колір, на діаграмі мають бути підписи.
"""

from matplotlib import pyplot as plt # Підключення модуля pyplot з бібліотеки matplotlib, необхідного для роботи з діаграмами
import numpy as np # Підключення модуля numpy для роботи з масивами та обчислення значень функції для кожного х

fig, ax = plt.subplots(figsize = (6, 3), subplot_kw = dict(aspect = "equal")) # Створення полотна для діаграми
# Записані дані з предметної області лабораторної роботи №9
students = [
        "Гриценко 150 см Ж",
        "Павленко 178 см Ч",
        "Лунцевич 163 см Ч",
        "Бабакович 152 см Ж",
        "Бринькевич 180 см Ч",
        "Мельник 154 см Ж",
        "Гринькевич 147 см Ч",
        "Ждан 190 см Ж",
        "Фамільянович 181 см Ч",
        "Отрукиотбиванич 134 см Ч"
    ]

def sum_height(students):
    sum_male = 0
    sum_female = 0
    for student in students:
        if student.split()[-1] == 'Ч':
            sum_male += float(student.split()[1])
        elif student.split()[-1] == 'Ж':
            sum_female += float(student.split()[1])
    return [sum_male, sum_female]
"""
Функція sum_height(students), необхідна для обчислення суми зросту всіх дівчаток та всіх хлопчиків.
Повертає результат у вигляді списку з двох значень.
"""

# Функція для підписів у відсотках
def func(pct, allvals):
    absolute = int(np.round(pct / 100. * np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute} см)"
"""
Функція func(pct, allvals), необхідна для створення відсоткової співвідношення.
Повертає форматований рядок з відсотковим значенням
"""

names=['Хлопчики','Дівчатка']

# Побудова кругової діаграми
wedges, texts, autotexts = ax.pie(sum_height(students), autopct = lambda pct: func(pct, sum_height(students)), textprops = dict(color='w'))

# Додавання легенди
ax.legend(wedges, names, title = 'Учні:', loc = 'center left', bbox_to_anchor = (1, 0, 0.5, 1))

# Налаштування тексту
plt.setp(autotexts, size = 8, weight = 'bold')

# Назва графіка
ax.set_title('Зріст учнів (кругова діаграма)')

plt.savefig('figure3.png') # Збереження даної діаграми у форматі .png
plt.show() # Виведення створеної діаграми на екран