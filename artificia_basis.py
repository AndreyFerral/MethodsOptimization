# Метод искуственного базиса
from cmath import inf
from prettytable import PrettyTable

M = '-M'
eq = [
[None, 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'],
[None, 2, -3, 6, 1, 0, 0, M], 
[24, 2, 1, -2, 1, 0, 0, 0], 
[22, 1, 2, 4, 0, 1, 0, 0], 
[10, 1, -1, 2, 0, 0, -1, 1]]

# Объявляем переменную таблицы
t = PrettyTable()

# Длина массива
row = len(eq) - 2
col = len(eq[0]) - 1
removed = 0

# Метод проверки единичных векторов. Список True - False
def create_one():
    mylist = []
    for j in range(1, col+1):
        if is_one([eq[2][j], eq[3][j], eq[4][j]]): mylist.append(True)
        else: mylist.append(False)
    mylist.insert(0, False)
    return mylist

# Метод на проверку единичного вектора
def is_one(list = []):
    is_one = False
    for i in range(len(list)):
        if list[i] == 1:
            if not is_one: 
                is_one = True
            else:
                return False
        if list[i] != 0 and list[i] != 1: 
            return False

    if not is_one: return False
    return True

# Метод для первоначального построения списка базисов
def build_c():
    list_c = []
    one = create_one()

    for i in range(1, col+1):
        if one[i]: list_c.append(i)
    
    if len(list_c) != row: 
        print(f'В задаче должно быть {row} единичных вектора!')
        exit()

    return list_c

# Строим базис
c = build_c()

# Метод для проверки строки на знак
def sign(var):
    if var.find('-') != -1: return -1
    else: return 1

# Метод для перемножения строки и числа
def dot(list1 = [], list2 = [], j = None):
    z, c = 0, 0
    for i in range(len(list1)):
        if type(list1[i]) == str or type(list2[i]) == str:
            temp1, temp2 = list1[i], list2[i]
            if type(temp1) == str: temp1 = sign(temp1)
            else: temp2 = sign(temp2)
            c += temp1 * temp2
        else: 
            z += list1[i] * list2[i]

    if j > 0 and j <= col: 
        z -= eq[1][j]

    return z, c

# Метод для расчета m1 и m2
def m1m2():
    m1, m2 = [], []
    one = create_one()

    for i in range(col+1):
        if one[i] == True:
            m1.append(0)
            m2.append(0)
        else:
            list1 = [eq[1][c[0]], eq[1][c[1]], eq[1][c[2]]]
            list2 = [eq[2][i], eq[3][i], eq[4][i]]
            first, second = dot(list1, list2, i)
            m1.append(first)
            m2.append(second)

    # Условия для проверки строк m1 и m2 (4 и 5)
    res_m2 = all(x == 0 for x in m2) # все значения == 0
    res_m1 = all(x >= 0 for x in m1) # все значения >= 0

    # В любом случае добавляем строку m1 (4)
    t.add_row(['4', '', '', m1[0], m1[1], m1[2], m1[3], m1[4], m1[5], m1[6], m1[7]])

    # Опорный план задачи найден
    if res_m1 and res_m2:
        print(t, f'\nОпорный план является оптимальным. F = {m1[0]}')
        print(f'X* = {get_result()}')
        return False
    # Перестаем считать по строке m2 (5)    
    elif res_m2 == True:
        print(t, '\nСтрока m2 содержит все нулевые значения')
        calc_table(m1)
        return True
    # Продолжаем считать по строке m2 (5)   
    else: 
        t.add_row(['5', '', '', m2[0], m2[1], m2[2], m2[3], m2[4], m2[5], m2[6], m2[7]])
        print(t)
        calc_table(m2)
        return True

# Метод для обновления значений таблицы по результатам m1 или m2
def calc_table(m = []):
    # Определение решающего значение и его индексов
    list_less = []
    for i in range(col):
        if m[i] < 0 and i != 0: list_less.append(m[i])

    # Если в списке нет отрицательных значений
    if list_less == []:
        if m[0] < 0: print('Исходная задача не имеет решения (A0 < 0)')
        elif m[0] == 0: print('Опорный план задачи вырожден (A0 = 0)')
        exit(0)

    # Находим минимальное значение в m1 или m2
    index_j = m.index(min(list_less))

    choice_list = []
    for i in range(row):
        if eq[i+2][index_j] >= 0: 
            choice_list.append(eq[i+2][0]/eq[i+2][index_j])
        else: choice_list.append(inf)

    index_i = choice_list.index(min(choice_list)) + 2
    main = eq[index_i][index_j]

    # Сохраняем измененную главную линию по x и y
    save_y = []
    save_x = [x / main for x in eq[index_i]]
    for i in range(row): save_y.append(eq[i+2][index_j])

    # Расчёт таблицы
    for i in range(row):
        for j in range(col+1):
            if i+2 == index_i: 
                # Изменяем значения в главной линии
                eq[index_i][j] = save_x[j]
            else:
                # Изменяем значения в остальных линиях
                eq[i+2][j] = eq[i+2][j] - save_x[j] * save_y[i]

    # Убираем искусственный базис
    if eq[1][c[index_i-2]] == M: 
        global removed
        removed += 1
        print(f"Искусственный базис {eq[0][c[index_i-2]]} убран")
        for i in range(1, len(eq)):
            eq[i][c[index_i-2]] = 0

    # Изменение базисного значения
    c[index_i-2] = index_j

# Метод для построения таблицы
def table_build():
    t.clear()
    t.field_names = ['I', 'Базис', 'Сб', 'A0', eq[0][1], eq[0][2], eq[0][3], eq[0][4], eq[0][5], eq[0][6], eq[0][7]]
    t.add_row(['', '', '', '', eq[1][1], eq[1][2], eq[1][3], eq[1][4], eq[1][5], eq[1][6], eq[1][7]])

    for i in range(3):
        t.add_row([i+1, eq[0][c[i]], eq[1][c[i]], eq[i+2][0], eq[i+2][1], eq[i+2][2], eq[i+2][3], eq[i+2][4], eq[i+2][5], eq[i+2][6], eq[i+2][7]])

# Метод для построения опорного плана
def get_result():
    wo_removed = col - removed
    result = [0] * wo_removed
    for i in range(len(c)):
        result[c[i]-1] = eq[i+2][0]
    return result
         
# Запускаем код 
while True:
    table_build()
    if m1m2() == False: break