# Метод дифференциальных рент
import copy
from prettytable import PrettyTable

# Исходные данные задачи

eq = [
    [7, 12, 4, 8, 5, 180],
    [1, 8, 6, 5, 3, 350],
    [6, 13, 8, 7, 4, 20],
    [110, 90, 120, 80, 150, 550]
]
'''
eq = [
    [7, 12, 4, 8, 5, 180],
    [3, 10, 8, 7, 5, 350],
    [7, 14, 9, 8, 5, 20],
    [110, 90, 120, 80, 150, 550]
]
'''
# Количество строк и столбцов
row = len(eq)
col = len(eq[0])

def build_headers():
    # Список[0] с первым пустым элементом
    headers = [[],[]]
    headers[0].append('')

    # Формируем содержание заголовков
    for number in range(1, col):
        headers[0].append(f'B{number}')
        if number < row: 
            headers[1].append(f'A{number}')
    
    # Добавляем столбцы 
    headers[0].append('Запасы')
    headers[0].append('Плюс/Минус')
    headers[1].append('Потребности')
    headers[1].append('Разность')
    return headers

def build_table():
    # Добавляем верхний заголовок для отображения
    headers = build_headers()
    table = PrettyTable(headers[0])
    # Определяем нижниюю и правую линию
    line_down, line_right = add_lines(headers)

    # Добавляем строки в таблицу для отображения
    for i in range(row):
        # Добавляем к строке значений заголовок
        current_row = []
        current_row.append(headers[1][i])
        # Добавляем к строке значения уравнения
        for j in range(col):
            current_row.append(eq[i][j])
        # Добавляем для вывода значение правой линии
        current_row.append(line_right[i])
        table.add_row(current_row)

    # Добавляем для вывода нижнюю линию
    table.add_row(line_down)
    return table

def calculate_lines():
    # Подготавливаем матрицу для плана
    plan = [[0]*(col-1) for i in range(row-1)]

    # Заполняем план мин элементами
    for j in range(col-1):
        # Составляем список для поиска мин элемента
        list_less = []
        for i in range(row-1): 
            list_less.append(eq[i][j])
        # Добавляем мин элемент в опорный план
        number_min = min(list_less)
        for i in range(row-1): 
            if eq[i][j] == number_min: 
                plan[i][j] = number_min

    # Формируем строки потребностей и запасов
    needs, reserves = [], []
    for i in range(col-1):
        needs.append(eq[-1][i])
        if i < row-1: reserves.append(eq[i][-1])
    print(needs, reserves)

    # Получаем очередность перемещения товара
    order = get_order(plan)

    # todo Распределить грузы по точкам 

    print(get_order(plan))

    return plan

def get_order(plan):
    order_support = copy.deepcopy(plan)
    order = []
    # 0 - пустые элементы
    # -1 - замена чисел с одним заполнением

    # Добавляем в очередь элементы с одним заполнением
    for i in range(row-1):
        for j in range(col-1):
            if order_support[i][j] != 0:
                if is_suitable(order_support, i, j):
                    order.append([i, j])
                    order_support[i][j] = -1

    # Добавляем в очередь остальные элементы
    for i in range(row-1):
        for j in range(col-1):
            if order_support[i][j] != 0 and order_support[i][j] != -1:
                order.append([i, j])
    
    return order

def is_suitable(order_support, i, j):
    # True - единственное заполнение
    check_row = True # в строке
    check_col = True # в столбце

    for n in range(col-1):
        # Проверяем по строке
        if order_support[i][n] != 0 and n != j:
            check_row = False
        # Проверяем по столбцу
        if n < row-1:
            if order_support[n][j] != 0 and n != i:
                check_col = False

    # Возвращаем true, если есть одно заполнения
    return check_row or check_col

def add_lines(headers):
    # Составляем пустые списки
    line_down = [''] * (col + 1)
    line_right = [''] * row

    # Наполняем списки значениями
    for i in range(col - 1):
        line_down[i] = 0
        if i < row - 1: line_right[i] = 0

    # Добавляем заголовок в нижний список
    line_down.insert(0, headers[1][-1])
    return line_down, line_right

print(build_table())
print(row, col)
print(build_headers())
print(add_lines(build_headers()))
print(calculate_lines())