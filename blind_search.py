# Метод слепого поиска
import random as rnd

left = 1
right = 100

start_point = 10
left_limit = start_point + -100
right_limit = start_point + 100
equation = lambda x, y: 100*(y - x**2)**2+(1-x)**2
result = float('inf')
list_x, list_y, list_res = [], [], []

for i in range(left, right):
    x = rnd.randint(left_limit, right_limit)
    y = rnd.randint(left_limit, right_limit)
    list_x.append(x)
    list_y.append(y)
    list_res.append(equation(x, y))
    print(f'x = {x} | y = {y} | результат = {equation(x, y)}')

result = min(map(abs, list_res))
id = list_res.index(result)
print('Итог: ')
print(f'x = {list_x[id]} | y = {list_y[id]} | результат = {list_res[id]}')