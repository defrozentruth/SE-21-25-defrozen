import math
import numpy as np
import matplotlib.pyplot as p

R = 1.2 #radius
n2 = 1 #пок. прел. среды за оптоволокном
f1 = lambda y: 1.4 - 0.18 * y ** 4
Zf = lambda y: 8 + np.sin(17.951958020513104 * y)
w = 3 * 10 ** 14#циклическая частота светового луча
y0 = 0.3 #начальный y
a = 30#начальный угол
n1 = lambda y, w: f1(y) * (1 - ((0.35 * 10 ** 14) / w) ** 2) #пок. прел. среды  оптоволокна
S = 0#длина траектории
eps = 0.0001 #шаг
direction = 1

N1 = n1(y0, w)
ang = np.pi / 2 - math.asin((np.sin(np.radians(a)) * n2) /N1)
Y = [y0]
X = [0]
while X[-1] < Zf(Y[-1]):
    Y.append(Y[-1] + np.cos(ang) * eps * direction)
    X.append(X[-1] + abs(np.sin(ang)) * eps)
    N_new = n1(Y[-1], w) if (R >= abs(Y[-1])) else n2
    if (np.sin(ang) * N1) / N_new > 1:
        direction *= -1
    else:
        ang = math.asin((np.sin(ang) * N1) / N_new)
    N1 = N_new
    S += eps

print("S = " + str(S))
y = np.arange(-1.2, 1.2, 0.0001)
p.plot(X, Y, "y")
p.plot(Zf(y), y, "r")
p.plot([0, 10], [R, R], "r")
p.plot([0, 10], [-R, -R], "r")
p.show()