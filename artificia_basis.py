# Метод искуственного базиса

z = lambda M, x1, x2, x3, x4, x5, x6, x7: -x1 - 2*x2 + 3*x3 - 10*x4 - M*x5 - M*x6 - M*x7 # max ("-" перед M)

def head():
    print(f"I | Базис | Cб | A0 | {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | ")
    print(f"  |       |    |    | {a[0]} | {a[1]} | {a[2]} | {a[3]} | {a[4]} | {a[5]} | {a[6]} | ")

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

    if j <= len(r)-4: z -= r[j]
    return z, c

M = '-M'
a = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7']
r  = [1, -2, 3, -10, M, M, M]
f  = [1, 1, 2, -6, 1, 0, 0, 1]
s = [1, 1, 4, -8, 0, 1, 0, 1]
t  = [4, 2, 1, -4, 0, 0, 1, 3]

c = [r[4], r[5], r[6]]
m1, m2 = [], []

def m1m2():
    m1.clear 
    m2.clear

    for i in range(len(f)):
        if i >= len(f)-4 and i <= len(f)-2:
            m1.append(0)
            m2.append(0)
        else:
            first, second = dot(c, [f[i], s[i], t[i]], i)
            m1.append(first)
            m2.append(second)

    print(f"4 |       |    | {m1[7]} | {m1[0]} | {m1[1]} | {m1[2]} | {m1[3]} | {m1[4]} | {m1[5]} | {m1[6]} | ")
    print(f"5 |       |    | {m2[7]} | {m2[0]} | {m2[1]} | {m2[2]} | {m2[3]} | {m2[4]} | {m2[5]} | {m2[6]} | ")

head()

print(f"1 |   {a[4]}  | {r[4]} | {f[7]} | {f[0]} | {f[1]} | {f[2]} | {f[3]} | {f[4]} | {f[5]} | {f[6]} | ")
print(f"2 |   {a[5]}  | {r[5]} | {s[7]} | {s[0]} | {s[1]} | {s[2]} | {s[3]} | {s[4]} | {s[5]} | {s[6]} | ")
print(f"3 |   {a[6]}  | {r[6]} | {t[7]} | {t[0]} | {t[1]} | {t[2]} | {t[3]} | {t[4]} | {t[5]} | {t[6]} | ")
m1m2()


