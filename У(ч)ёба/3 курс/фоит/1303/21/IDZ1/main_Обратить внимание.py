import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.special import *
from scipy.constants import c

def f1(y):
    res = 1.5 + 0.3 * (np.cos(0.8 * y)) ** 2
    return res

def Zf(y):
    return 42+3*np.sin(17.951958020513104*y)


alpha = math.radians(32)  # градусы!! перевести в радианы
y0 = 0.1
R = 1.2
n2 = 1
w = 3.6 * 10**14
c = 0.00001

arr_z = []
arr_y = []

def n1(y):
    return f1(y) * (1 - (0.35 * 10 ** 14 / w) ** 2)

def incoming_angle(alpha0):
    n_start = n1(y0) #показатель преломления в точке входа
    sin_alpha = np.sin(alpha0)/n_start #угол под которым луч зашел, ось горизонтальна
    gamma = np.pi/2 - np.arcsin(sin_alpha)  # перевернули угол, теперь ось вертикальна
    return np.sin(gamma)  # вернули синус вертикального угла


def iteration(start_angle):
    S = 0
    H = y0
    L = 0
    sin_gamma = start_angle
    n_gamma = n1(y0)
    incline = 1
    while(S <= Zf(H)):
        H += c * np.sqrt(1-sin_gamma**2) * incline #текущая высота
        if(H >= R): n_beta = n2
        else: n_beta = n1(H)
        sin_beta = (n_gamma * sin_gamma) / n_beta #находим угол преломленного луча
        if(sin_beta > 1):
            sin_beta = sin_gamma #луч отразился
            incline *= -1
        L += c #траектория
        S += sin_beta * c #расстояние
        sin_gamma = sin_beta #меняем входные условия для новой итерации
        n_gamma = n_beta
        arr_y.append(H)
        arr_z.append(S)
    print("алгоритм остановился, тк луч достиг выхода на высоте ", H, " и расстоянии ", Zf(H))
    return L

t1 = np.arange(-R, R, 0.1)

res = iteration(incoming_angle(alpha))
print("результат", res)

plt.plot(arr_z, arr_y, Zf(t1), t1, [0,40], [R, R], 'g', [0,40], [-R, -R], 'g')
plt.show()
