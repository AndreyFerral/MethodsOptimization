import sympy as sp
import re 

def get_conditions():
    conditions = [
        'x1+2*x2<=8',
        '2*x1-x2<=12'
        ]   
    return conditions

def check_function():
    if is_max: return is_max, function
    else: return True, -function

def get_count_x(function):
    cur_count, max_count = 0, 10
    max_symb = []
    # Составляем список символов на поиск
    for i in range(1, max_count+1):
        max_symb.append(f'x{i}')
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
        condition = symbols[i] != 'y' and symbols[i] != 'w'
        cur_count = count_x+1 if condition else count_y+1
        # Составляем список переменных
        for j in range(1, cur_count):
            headers.append(f'{symbols[i]}{j}')
    return headers

def get_lagranje():
    lagranje = str(function)
    pattern = '\d+$'
    # Составляем функцию Лагранжа
    for i in range(len(conditions)):
        if conditions[i].find('<=') != -1:
            # Удаляем знак <= и число после него
            match = re.findall(pattern, conditions[i])
            value = re.sub('<=', '', conditions[i])
            value = re.sub(match[0], '', value)
            value = str(sp.simplify(value)*-1)
            # Добавляем в функцию Лагранжа
            equality = match[0] + value
            lagranje += f'+y{i+1}*({equality})'
        else:
            print('Ошибка! Знак у условий должен быть <=')
            exit()
    return lagranje

def get_derivatives():
    # Составляем список переменных для производных
    x_symbs = get_symbols('x')
    y_symbs = get_symbols('y')
    xy_symbs = x_symbs + y_symbs
    # Составляем список с производными
    derivatives = []
    for i in range(len(xy_symbs)):
        derivatives.append(sp.diff(lagranje, xy_symbs[i]))
    return derivatives

def get_symbols(letter):
    # Устанавливаем количество в зависимости от символа
    condition = letter != 'y' and letter != 'w'
    cur_count = count_x+1 if condition else count_y+1
    # Формируем список символов
    letter_symbs = []
    for i in range(1, cur_count):
        letter_symbs.append(letter+str(i))
    return letter_symbs

def get_characters(expression):
    return re.findall(r'(\b\w*[\.]?\w+\b|\*{2}|[<>=]{1,2}|[\(\)\+\*\-\/])', expression)

def parser_coeff(parser_string, symbol):
    coeff = '0'
    for i in range(len(parser_string)):
        if parser_string[i] == symbol:
            coeff = '1'
            if i == 0: break
            elif parser_string[i-1] == '-':
                coeff = parser_string[i-1] + coeff
            elif parser_string[i-1] == '*':
                coeff = parser_string[i-2]
                if i-2 == 0: break
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

    equation = []
    for i in range(len(list_eq)):
        if i < count_x: 
            equation.append(list_eq[i].replace('>', f'-{v_symbs[i]}+{z_symbs[i]}'))
        else: 
            equation.append(list_eq[i].replace('<', f'+{w_symbs[i-count_x]}'))
    return equation

def build_list_eq():
    list_eq = []
    for i in range(len(equation)):
        temp = []
        for j in range(len(headers)):
            characters = get_characters(equation[i])
            temp.append(parser_coeff(characters, headers[j]))
        list_eq.append(temp)
    return list_eq

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
# Вывод полученных значений
print('Функция', function)
print('Условия', conditions)
print('Лагранж', lagranje)
print('Производные', derivatives)
print('Уравнение', equation)
print('Заголовки', headers)
print('Список коэффициентов', list_eq)

# todo Преобразовать equation в список для искуственного базиса