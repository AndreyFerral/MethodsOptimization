import sympy as sp
import numpy as np

x1 = sp.Symbol('x1')
x2 = sp.Symbol('x2')
y = (x1-3)**2 + (5-x2)**2

eq1 = sp.lambdify(x1, sp.diff(y, x1))
eq2 = sp.lambdify(x2, sp.diff(y, x2))

a = 0.377
h = 0.377

f_pred = -0.5
s_pred = -1
f = 0.2
s = 0.2

R = 30.88
R = lambda x1, x2: (x1-3)**2 + (5-x2)**2
i = 0

while(round(R(f,s), 3) != 0):
    i += 1
    #print(eq1(f), '\n', eq2(s))

    grad = lambda x1, x2: ((x1 + x2)**2)**a
    #print('grad: ', grad(eq1(f), eq2(s)))

    #print('R: ', R(f, s))

    x_next1 = lambda x, x_prev: x - a*(x-x_prev)-h*(eq1(x))
    x_next2 = lambda x, x_prev: x - a*(x-x_prev)-h*(eq2(x))
    #print(x_next1(f, f_pred))
    #print(x_next2(s, s_pred))

    tempf = f
    temps = s
    f = x_next1(f, f_pred)
    s = x_next2(s, s_pred)
    f_pred = tempf
    s_pred = temps

print(f'x1 {f} x2 {s}')
print(f'R {R(f, s)}')
print(i)