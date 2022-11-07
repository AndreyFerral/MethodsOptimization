# Метод дифференциальных рент
from prettytable import PrettyTable

# Исходные данные задачи
eq = [
    [7, 12, 4, 8, 5, 180],
    [1, 8, 6, 5, 3, 350],
    [6, 13, 8, 7, 4, 20],
    [110, 90, 120, 80, 150, 550]
]

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
    line_down, line_right = build_lines(headers)
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

def build_lines(headers):
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
print(build_lines(build_headers()))