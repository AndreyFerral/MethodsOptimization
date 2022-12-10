# Метод искуственного базиса
from cmath import inf
from prettytable import PrettyTable

class ArtificiaBasis:
    def __init__(self, eq, eq_condition = []):
        # Задаем значения с помощью параметров
        self.eq = eq 
        self.eq_condition = eq_condition
        # Объявляем переменную таблицы
        self.table = PrettyTable()
        self.removed = 0
        # Количество строк и столбцов
        self.row = len(self.eq) - 1
        self.col = len(self.eq[0]) - 1
        # Строим список базисов
        self.bases = self.build_bases()   
        # Запускаем код 
        while True:
            self.build_table()
            if self.calc_m1m2() == False: break

    # Метод проверки единичных векторов. Список True - False
    def get_unit_vectors(self):
        unit_vectors = []
        for j in range(1, self.col+1):
            # Формируем список на проверку
            list_for_check = []
            for i in range(1, self.row+1):
                list_for_check.append(self.eq[i][j])
            # Проверяем вектор на единичность
            if self.is_unit(list_for_check): 
                unit_vectors.append(True)
            else: 
                unit_vectors.append(False)
        # Возвращаем список единичных векторов
        unit_vectors.insert(0, False)
        return unit_vectors

    # Метод на проверку единичного вектора
    def is_unit(self, list_for_check):
        is_unit = False
        for i in range(len(list_for_check)):
            # Если находится цифра 1 (должна быть одна)
            if list_for_check[i] == 1:
                if not is_unit: is_unit = True
                else: return False
            # Единичный вектор должен состоять из 0 и 1
            if list_for_check[i] != 0 and list_for_check[i] != 1: 
                return False

        # Возвращаем результат в зависимости от is_unit
        if is_unit: return True
        else: return False

    # Метод для первоначального построения списка базисов
    def build_bases(self):
        bases = []
        unit_vectors = self.get_unit_vectors()
        # Добавляем в список номер единичного вектора
        for i in range(1, self.col+1):
            if unit_vectors[i]: 
                bases.append(i)
        if len(bases) != self.row: 
            print(f'В задаче должно быть {self.row} единичных вектора!')
            exit()
        return bases

    # Метод для проверки строки на знак
    def sign(self, str_for_check):
        if str_for_check.find('-') != -1: 
            return -1
        else: 
            return 1

    # Метод для перемножения строки и числа
    def dot(self, list1, list2, j):
        m1_number, m2_number = 0, 0
        for i in range(len(list1)):
            if type(list1[i]) == str or type(list2[i]) == str:
                temp1, temp2 = list1[i], list2[i]
                if type(temp1) == str: temp1 = self.sign(temp1)
                else: temp2 = self.sign(temp2)
                m2_number += temp1 * temp2
            else: 
                m1_number += list1[i] * list2[i]

        if j > 0 and j <= self.col: 
            m1_number -= self.eq[0][j]

        return m1_number, m2_number

    # Метод для расчета m1 и m2
    def calc_m1m2(self):
        m1_list, m2_list = [], []
        unit_vectors = self.get_unit_vectors()

        for i in range(self.col+1):
            if unit_vectors[i] == True:
                m1_list.append(0)
                m2_list.append(0)
            else:
                # Формируем списки для перемножения
                list1, list2 = [], []
                for j in range(1, self.row+1):
                    list1.append(self.eq[0][self.bases[j-1]])
                    list2.append(self.eq[j][i])
                # Добавляем результаты умножения
                m1_number, m2_number = self.dot(list1, list2, i)
                m1_list.append(round(m1_number, 3))
                m2_list.append(round(m2_number, 3))

        # Условия для проверки строк m1 и m2
        res_m1 = all(x >= 0 for x in m1_list) # все значения >= 0
        res_m2 = all(x == 0 for x in m2_list) # все значения == 0

        # В любом случае добавляем строку m1
        self.table.add_row([f'{self.row+1}', '', ''] + m1_list)

        # Опорный план задачи найден
        if res_m1 and res_m2:
            print(self.table, f'\nОпорный план является оптимальным. F = {m1_list[0]}')
            print(f'X* = {self.get_result()}')
            return False
        # Перестаем считать по строке m2  
        elif res_m2 == True:
            print(self.table, '\nСтрока m2 содержит все нулевые значения')
            self.calc_table(m1_list)
            return True
        # Продолжаем считать по строке m2
        else: 
            self.table.add_row([f'{self.row+2}', '', ''] + m2_list)
            print(self.table)
            self.calc_table(m2_list)
            return True

    # Метод для обновления значений таблицы по результатам m1 или m2
    def calc_table(self, m_list):
        list_less = []
        for i in range(self.col):
            if m_list[i] < 0 and i != 0: 
                list_less.append(m_list[i])
        # Если в списке нет отрицательных значений
        if list_less == []:
            if m_list[0] < 0: print('Исходная задача не имеет решения (A0 < 0)')
            elif m_list[0] == 0: print('Опорный план задачи вырожден (A0 = 0)')
            exit(0)

        # Находим минимальное значение в m1 или m2
        index_j = m_list.index(min(list_less))

        choice_list = []
        for i in range(1, self.row+1):
            if self.eq[i][index_j] >= 0: 
                choice_list.append(self.eq[i][0]/self.eq[i][index_j])
            else: 
                choice_list.append(inf)
        # Получаем решающий элемент
        index_i = choice_list.index(min(choice_list)) + 1
        main = self.eq[index_i][index_j]
        # Сохраняем измененную главную линию по x и y
        save_y = []
        save_x = [x / main for x in self.eq[index_i]]
        for i in range(self.row): 
            save_y.append(self.eq[i+1][index_j])

        # Расчёт таблицы
        for i in range(1, self.row+1):
            for j in range(self.col+1):
                if i == index_i: 
                    # Изменяем значения в главной линии
                    self.eq[index_i][j] = save_x[j]
                else:
                    # Изменяем значения в остальных линиях
                    self.eq[i][j] = self.eq[i][j] - save_x[j] * save_y[i-1]

        # Убираем искусственный базис
        if self.eq[0][self.bases[index_i-1]] == '-M': 
            # Обновляем значение убранных базисов
            self.removed += 1
            # Заменяем значения убранного базиса на 0
            name_bases = f'P{self.bases[index_i-1]}'
            print(f"Искусственный базис {name_bases} убран")
            for i in range(0, len(self.eq)):
                self.eq[i][self.bases[index_i-1]] = 0.0

        # Определяем новый базис
        self.bases[index_i-1] = index_j

    def get_vectors_name(self):
        vectors_name = []
        for i in range(1, self.col+1):
            vectors_name.append(f'P{i}')
        return vectors_name

    # Метод для построения таблицы
    def build_table(self):
        self.table.clear()
        # Формируем заголовки для таблицы
        header_first = ['I', 'Базис', 'Сб', 'A0'] + self.get_vectors_name()
        header_second = ['', '', '', '']
        for i in range(1, self.col+1):
            header_second.append(self.eq[0][i])
        # Добавляем заголовки в таблицу
        self.table.field_names = header_first
        self.table.add_row(header_second)
        # Формируем строчки в таблице (до m1)
        for i in range(self.row):
            current_row = [i+1, f'P{self.bases[i]}', self.eq[0][self.bases[i]]]
            for j in range(self.col+1):
                value = round(self.eq[i+1][j], 3)
                current_row.append(value)
            self.table.add_row(current_row)
        
    # Метод для построения опорного плана
    def get_result(self):
        wo_removed = self.col - self.removed
        result = [0] * wo_removed
        for i in range(len(self.bases)):
            result[self.bases[i]-1] = self.eq[i+1][0]
        return result


eq = [
    [None, 2, -3, 6, 1, 0, 0, '-M'], 
    [24, 2, 1, -2, 1, 0, 0, 0], 
    [22, 1, 2, 4, 0, 1, 0, 0], 
    [10, 1, -1, 2, 0, 0, -1, 1]]
artificia_basis = ArtificiaBasis(eq)