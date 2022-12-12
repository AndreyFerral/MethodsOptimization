from artificia_basis_class import ArtificiaBasis
import sympy as sp
import re

def get_conditions():
    return [
        'x1+2*x2<=8',
        '2*x1-x2<=12'
    ]

def check_function():
    original = is_max, function
    changed = True, str(sp.simplify(function)*-1)
    return original if is_max else changed

def get_count_x(function):
    cur_count, max_count = 0, 10
    # Составляем список символов на поиск
    max_symb = [f'x{i}' for i in range(1, max_count+1)]
    # Получаем количество символов
    for i in range(max_count):
        if function.find(max_symb[i]) != -1:
            cur_count += 1
    return cur_count

def get_count_y(conditions):
    return len(conditions)

def get_headers(symbols, count_x, count_y):
    headers = []
    for i in range(len(symbols)):
        # Устанавливаем количество в зависимости от символа
        condition = symbols[i] not in ['y', 'w']
        cur_count = count_x+1 if condition else count_y+1
        # Составляем список переменных
        headers.extend(f'{symbols[i]}{j}' for j in range(1, cur_count))
    return headers

def get_lagranje():
    lagranje = str(function)
    pattern = '\d+$'
    # Составляем функцию Лагранжа
    for i in range(len(conditions)):
        if conditions[i].find('<=') != -1:
            # Удаляем знак <= и число после него
            index_sign = conditions[i].find('<=')
            value = conditions[i][0:index_sign]
            # Добавляем в функцию Лагранжа
            value = str(sp.simplify(value)*-1)
            match = re.findall(pattern, conditions[i])
            equality = match[0] + value
            lagranje += f'+y{i+1}*({equality})'
        else:
            print('Ошибка! Знак у условий должен быть <=')
            exit()
    return lagranje

def get_derivatives():
    # Составляем список переменных для производных
    xy_symbs = get_symbols('x') + get_symbols('y')
    # Составляем список с производными
    return [sp.diff(lagranje, xy_symbs[i]) for i in range(len(xy_symbs))]

def get_symbols(letter):
    # Устанавливаем количество в зависимости от символа
    condition = letter not in ['y', 'w']
    cur_count = count_x+1 if condition else count_y+1
    # Формируем список символов
    return [letter+str(i) for i in range(1, cur_count)]

def get_characters(expression):
    return re.findall(r'(\b\w*[\.]?\w+\b|\*{2}|[<>=]{1,2}|[\(\)\+\*\-\/])', expression)

def parser_coeff(parser_string, symbol):
    # Функция для получения значения у коэффициента
    coeff = '0'
    for i in range(len(parser_string)):
        if parser_string[i] == symbol:
            coeff = '1'
            if i == 0: break
            elif parser_string[i-1] == '-':
                coeff = parser_string[i-1] + coeff
            elif parser_string[i-1] == '*':
                coeff = parser_string[i-2]
                if i == 2: break
                elif parser_string[i-3] == '-':
                    coeff = parser_string[i-3] + coeff
    return coeff

def calc_equation():
    pattern = '[-+] \d+$'
    list_matchs, list_values = [], []

    # Выделение левой и правой части из производных
    for i in range(len(derivatives)):
        parser_string = str(derivatives[i])
        match = re.findall(pattern, parser_string)
        value = re.sub(pattern, '', parser_string)
        list_matchs.append(match)
        list_values.append(value)

    list_eq = []
    # Соединение левой и правой части в неравенства
    for i in range(len(derivatives)):
        left = sp.simplify(list_values[i])
        right = sp.simplify(list_matchs[i][0])
        # Определяем знаки в зависимости от x или y
        greater_equal, less_equal = '>=', '<='
        if_sign = greater_equal if count_x > i else less_equal
        else_sign = less_equal if count_x > i else greater_equal
        # Если правая сторона отрицательная, то умножнаем на -1
        if right < 0: list_eq.append(str(left) + else_sign + str(-right))
        else: list_eq.append(str(-left) + if_sign + str(right))

    v_symbs = get_symbols('v')
    z_symbs = get_symbols('z')
    w_symbs = get_symbols('w')

    # Заменяем неравенство на равенство
    equation = []
    for i in range(len(list_eq)):
        if list_eq[i].find('>') != -1:
            equation.append(list_eq[i].replace('>', f'-{v_symbs[i]}+{z_symbs[i]}'))
        else:
            equation.append(list_eq[i].replace('<', f'+{w_symbs[i-count_x]}'))
    return equation

def build_list_eq():
    list_eq, temp = [], [None]
    # Формируем первую строку в eq
    for i in range(len(headers)):
        if headers[i].find('z') < 0:
            temp.append(0)
        else: temp.append('-M')
    list_eq.append(temp)
    # Формируем остальные строки в eq
    for i in range(len(equation)):
        temp = []
        characters = get_characters(equation[i])
        # Получаем значение после равенства
        index = [j + 1 for j in range(len(characters)) if characters[j] == '=']
        temp.append(int(characters[index[0]]))
        # Получаем коэффициенты
        for j in range(len(headers)):
            value = int(parser_coeff(characters, headers[j]))
            temp.append(value)
        list_eq.append(temp)

    return list_eq

def build_eq_condition():
    # Составляем условия как в методички
    eq_condition_old = []
    for i in range(1, count_x + 1):
        temp = [f'x{i}', f'v{i}']
        eq_condition_old.append(temp)
    for i in range(1, count_y + 1):
        temp = [f'y{i}', f'w{i}']
        eq_condition_old.append(temp)
    # Составляем условия для искуственного базиса
    eq_condition = []
    for i in range(len(eq_condition_old)):
        temp = []
        for j in range(len(eq_condition_old[i])):
            for m in range(len(headers)):
                if headers[m] == eq_condition_old[i][j]:
                    temp.append(m+1)
        eq_condition.append(temp)
    return eq_condition

# Данные для ввода пользователем
is_max = True
function = '2*x1+4*x2-x1**2-2*x2**2'
conditions = get_conditions()

# Обработка введенных данных
is_max, function = check_function()
symbols = ['x', 'y', 'v', 'w', 'z']
count_x = get_count_x(function)
count_y = get_count_y(conditions)
headers = get_headers(symbols, count_x, count_y)

# Получение различных значений
lagranje = get_lagranje()
derivatives = get_derivatives()
equation = calc_equation()
list_eq = build_list_eq()
eq_condition = build_eq_condition()
# Вывод полученных значений
print('Функция:', function)
print('Условия:', conditions)
print('Лагранж:', lagranje)
print('Производные:', derivatives)
print('Уравнение:', equation)
print('Заголовки:', headers)
print('Входные данные:', list_eq)
print('Условия P:', eq_condition)

# Вызываем метод искуственного базиса
artificia_basis = ArtificiaBasis(list_eq, eq_condition, function)