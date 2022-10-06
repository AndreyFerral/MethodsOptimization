# Метод искуственного базиса
from cmath import inf

z = lambda M, x1, x2, x3, x4, x5, x6, x7: -x1 - 2*x2 + 3*x3 - 10*x4 - M*x5 - M*x6 - M*x7 # max ("-" перед M)

def head():
    print(f"I | Базис | Cб | A0 | {eq[1][1]} | {eq[1][2]} | {eq[1][3]} | {eq[1][4]} | {eq[1][5]} | {eq[1][6]} | {eq[1][7]} | ")
    print(f"  |       |    |    | {eq[0][1]} | {eq[0][2]} | {eq[0][3]} | {eq[0][4]} | {eq[0][5]} | {eq[0][6]} | {eq[0][7]} | ")

def sign(var):
    if var.find('-') != -1: return -1
    else: return 1

def dot(list1 = [], list2 = [], j = int):
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

M = '-M'
eq = [
[None, 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7'],
[None, 2, -3, 6, 1, 0, 0, M], 
[24, 2, 1, -2, 1, 0, 0, 0], 
[22, 1, 2, 4, 0, 1, 0, 0], 
[10, 1, -1, 2, 0, 0, -1, 1]]

# длина массива с учетом 0 индекса
row = len(eq) - 3
col = len(eq[0]) - 1

def is_one(list = []):
    is_one = False
    for i in range(len(list)):
        if list[i] == 1:
            if is_one == False: is_one = True
            else:
                return False
        if list[i] != 0 and list[i] != 1: 
            return False

    if is_one == False: return False
    return True

def create_one():
    mylist = []
    for i in range(col):
        if is_one([eq[2][i+1], eq[3][i+1], eq[4][i+1]]) == True: mylist.append(True)
        else: mylist.append(False)
        #print(eq[2][i+1], eq[3][i+1], eq[4][i+1])
    mylist.insert(0, False)
    return mylist

c = [4,5,7]
one = create_one()
m1, m2 = [], []
#print(one)

def m1m2():
    m1.clear 
    m2.clear

    for i in range(col+1):
        if one[i] == True:
            m1.append(0)
            m2.append(0)
        else:
            list1 = [eq[1][c[0]], eq[1][c[1]], eq[1][c[2]]]
            list2 = [eq[2][i], eq[3][i], eq[4][i]]
            #print(list1, list2)
            first, second = dot(list1, list2, i)
            m1.append(first)
            m2.append(second)

    print(f"4 |       |    | {m1[0]} | {m1[1]} | {m1[2]} | {m1[3]} | {m1[4]} | {m1[5]} | {m1[6]} | {m1[7]} | ")
    print(f"5 |       |    | {m2[0]} | {m2[1]} | {m2[2]} | {m2[3]} | {m2[4]} | {m2[5]} | {m2[6]} | {m2[7]} | ")

    list_less = []
    for i in range(col):
        if m2[i] < 0 and i != 0: list_less.append(m2[i])
    index_j = m2.index(min(list_less))

    choice_list = []
    for i in range(row+1):
        if eq[i+2][index_j] >= 0: 
            choice_list.append(eq[i+2][0]/eq[i+2][index_j])
        else: choice_list.append(inf)
    #print(choice_list)

    index_i = choice_list.index(min(choice_list)) + 2
    main = eq[index_i][index_j]
    #print(f'eq[{index_i}][{index_j}] = {main}')

    for j in range(col):
        #print(eq[index_i][j], '/', main, '=', eq[index_i][j]/main)
        eq[index_i][j] = eq[index_i][j]/main



head()
print(f"1 |   {eq[0][c[0]]}  | {eq[1][c[0]]} | {eq[2][0]} | {eq[2][1]} | {eq[2][2]} | {eq[2][3]} | {eq[2][4]} | {eq[2][5]} | {eq[2][6]} | {eq[2][7]} | ")
print(f"2 |   {eq[0][c[1]]}  | {eq[1][c[1]]} | {eq[3][0]} | {eq[3][1]} | {eq[3][2]} | {eq[3][3]} | {eq[3][4]} | {eq[3][5]} | {eq[3][6]} | {eq[3][7]} | ")
print(f"3 |   {eq[0][c[2]]}  | {eq[1][c[2]]} | {eq[4][0]} | {eq[4][1]} | {eq[4][2]} | {eq[4][3]} | {eq[4][4]} | {eq[4][5]} | {eq[4][6]} | {eq[4][7]} | ")
m1m2()


#if is_one([0, 0, 1, 2]): print('Good')
#else: print('Bad')