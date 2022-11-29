from sympy import * 
import copy
import re 

# todo сделать автоматизированное создание
xy_symbols = ['x1', 'x2', 'y1', 'y2']
#x1, x2, y1, y2 = symbols(xy_symbols)

def get_conditions():
    conditions = [
        'x1+2*x2<=8',
        '2*x1-x2<=12']   
    return conditions

def check_function():
    if is_max: return is_max, function
    else: return true, -function

def get_lagranje():
    lagranje = function
    pattern = '\d+$'
    # Составляем функцию Лагранжа
    for i in range(len(conditions)):
        if conditions[i].find('<=') != -1:
            # Удаляем знак <= и число после него
            match = re.findall(pattern, conditions[i])
            value = re.sub('<=', '', conditions[i])
            value = re.sub(match[0], '', value)
            # Добавляем в функцию Лагранжа
            equality = match[0] + '-' + value
            lagranje += f'+y{i+1}*({equality})'
        else:
            print('Ошибка! Знак у условий должен быть <=')
            exit()
    return lagranje

def get_derivatives():
    derivatives = []
    for i in range(len(xy_symbols)):
        # Составляем список производных по списку символов
        derivatives.append(diff(lagranje, xy_symbols[i]))
    return derivatives

def get_symbols(letter):
    count = len(xy_symbols)/2
    symbols = []
    for i in range(int(count)):
        symbols.append(letter+str(i+1))
    return symbols

def calc_eq():
    pattern = '[-+] \d+$'
    list_matchs = []
    list_values = []
    for i in range(len(derivatives)):
        string = str(derivatives[i])
        match = re.findall(pattern, string)
        value = re.sub(pattern, '', string)
        list_matchs.append(match)
        list_values.append(value)

    print('Выделение левой и правой части из выражения:')
    print('Левая', list_values)
    print('Правая', list_matchs)

    list_eq = []
    for i in range(len(derivatives)):
        left = simplify(list_values[i])
        right = (-simplify(list_matchs[i][0])) 
        # По умолчанию у первой половины знак >=, второй <=
        # Если правая сторона отрицательная, то умножнаем на -1
        if len(derivatives)/2 > i:
            if right < 0: list_eq.append(str(-left) + '>=' + str(-right))
            else: list_eq.append(str(left) + '<=' + str(right))
        else:
            if right < 0: list_eq.append(str(-left) + '<=' + str(-right))
            else: list_eq.append(str(left) + '>=' + str(right))
        
    print('Соединенный', list_eq)

    v_symbs = get_symbols('v')
    w_symbs = get_symbols('w')
    z_symbs = get_symbols('z')

    equation = []
    v, w = 0, 0
    # todo Переделать. Первая половина всегда будет >=
    for i in range(len(list_eq)):
        if list_eq[i].find('>') != -1:
            equation.append(list_eq[i].replace('>', f'-{v_symbs[v]}+{z_symbs[v]}'))
            v += 1
        else:
            equation.append(list_eq[i].replace('<', f'+{w_symbs[w]}'))
            w += 1
    return equation

is_max = True
function = '2*x1+4*x2-x1**2-2*x2**2'
is_max, function = check_function()
conditions = get_conditions()
lagranje = get_lagranje()
derivatives = get_derivatives()
equation = calc_eq()

print('Функция', function)
print('Условия', conditions)
print('Лагранж', lagranje)
print('Производные', derivatives)
print('Уравнение', equation)

# todo Преобразовать equation в список для искуственного базиса
print('Проверка', diff('2*x1 + y1 + 2*y2', 'x1'))