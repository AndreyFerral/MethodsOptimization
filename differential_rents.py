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
    plan, line_down, line_right = calculate_lines()
    line_down.insert(0, headers[1][-1])

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

    # Переходим к следующей итерации
    isWork = False
    for i in range(row-1):
        if line_right[i] != '+0':
            isWork = True
            next_eq(line_down, line_right)
            break
    # Необходимо ли продолжать программу
    if not isWork: 
        return table, plan
    else:
        return table, None

def calculate_plan(needs, reserves):
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

    # Получаем очередность перемещения товара
    order = get_order(plan)
    # Распределяем груз по точкам
    for i in range(len(order)):
        m = order[i][0]
        n = order[i][1]
        # Если больше нет потребности или запаса
        if reserves[m] == 0 or needs[n] == 0: 
            continue
        # Если запаса больше потребностей
        elif reserves[m] >= needs[n]:
            plan[m][n] = needs[n]
            reserves[m] = reserves[m] - needs[n]
            needs[n] = 0
        # Если потребностей больше запаса
        else:
            plan[m][n] = reserves[m]
            needs[n] = needs[n] - reserves[m]
            reserves[m] = 0
 
    return plan, needs, reserves

def get_volume(plan):
    result = 0
    for i in range(len(plan)):
        for j in range (len(plan[i])):
            result += plan[i][j]
    return result

def calculate_lines():
    # Формируем строки потребностей и запасов
    needs, reserves = [], []
    for i in range(col-1):
        needs.append(eq[-1][i])
        if i < row-1: 
            reserves.append(eq[i][-1])
    # Запоминаем текущие значения потребностей и запасов
    needs_copy = copy.deepcopy(needs)
    reserves_copy = copy.deepcopy(reserves)
    # Получаем обновленные значения
    plan, needs, reserves = calculate_plan(needs, reserves)

    # Составляем избыточную/недостаточную строку
    line_right = [''] * row
    # Определяем избыточные строки 
    for i in range(len(reserves)):
        if reserves[i] != 0: 
            line_right[i] = f'+{reserves[i]}'
    # Определяем недостаточные строки 
    for i in range(len(needs)):
        if needs[i] != 0: 
            index = line_right.index('')
            line_right[index] = f'-{needs[i]}'
    # Определяем нулевые строки с знаком
    for i in range(len(line_right)-1):
        if line_right[i] == '':
            needs_temp = copy.deepcopy(needs_copy)
            reserves_temp = copy.deepcopy(reserves_copy)
            # Прибавляем к поставкам 1, где стоит 0
            reserves_temp[i] += 1
            # Рассчитываем новый план и сумму планов
            plan_temp = calculate_plan(needs_temp, reserves_temp)[0]
            sum_plan = get_volume(plan)
            sum_plan_temp = get_volume(plan_temp)

            # Если суммарный объем поставок не изменился
            if sum_plan == sum_plan_temp: 
                line_right[i] = '+0'
            # Если суммарный объем поставок изменился
            else:
                line_right[i] = '-0' 

    # Составляем строку разности
    line_down = [''] * (col + 1)
    # Определяем числа в рамках 
    for i in range(row-1):
        for j in range(col-1): 
            if plan[i][j] != 0:
                # Если строка положительная 
                if line_right[i].find('+') != -1:
                    line_down[j] = '-'
                # Иначе надо найти минимальный тариф
                else: 
                    list_less = []
                    # Добавляем в список тарифы в положительных строках
                    for m in range(row-1):
                        if line_right[m].find('+') != -1:
                            list_less.append(eq[m][j])
                    # Вычисляем минимальный тариф
                    number_min = min(list_less)
                    # Рассчитываем разность
                    difference = number_min-eq[i][j]
                    line_down[j] = f'{difference}'

    return plan, line_down, line_right

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

def next_eq(line_down, line_right):
    # Поиск минимальной разности
    list_less = []
    for i in range(len(line_down)):
        if line_down[i].isdigit(): 
            list_less.append(line_down[i])
    difference_min = min(list_less)
    # Изменяем значения в отрицательных строках
    for i in range(row-1):
        for j in range(col-1):
            if line_right[i].find('-') != -1:
                eq[i][j] += int(difference_min)

def start_method():
    # Проверяем задачу на положительные элементы
    try:
        positive_eq_list = [all(x >= 0 for x in part) for part in eq]
        positive_eq = all(x for x in positive_eq_list)
    except:
        print('Задача должна состоять из чисел')
        return
    # Рассчитываем объем запасов и потребностей
    need, reserve = 0, 0
    for i in range(col-1):
        need += eq[-1][i]
        if i < row-1: 
            reserve += eq[i][-1]
    # Проверяем задачу на корректность
    summary = eq[-1][-1]
    if not positive_eq:
        print('Задача должна состоять из положительных элементов')
        return
    elif need != reserve:
        print('Объем запасов не совпадает с объемом потребностей')
        return
    elif need != summary or reserve != summary:
        print('Объем запасов/потребностей не совпадает с общим значением')
        return
    # Если проходит все условия
    eq_copy = copy.deepcopy(eq)
    while True:
        table, plan = build_table()
        if not plan:
            print(table)
        else: 
            total_costs = 0
            for i in range(row-1):
                for j in range(col-1):
                    if plan[i][j] != 0:
                        total_costs += eq_copy[i][j] * plan[i][j]
            print(table)
            print('Оптимальный план:', plan)
            print('Общие затрары:', total_costs)
            break

start_method()