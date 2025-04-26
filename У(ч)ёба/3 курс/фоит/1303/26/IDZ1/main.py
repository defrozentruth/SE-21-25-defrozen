from math import *
import numpy as np
import matplotlib.pyplot as plt


def f1(y):
    return 1.2 + 0.3 * cos(0.8 * y) ** 3


def zf(y):
    return 20 + 3 * sin(17.951958020513104 * y)


def n1(y, om):
    return f1(y) * om


def angle(alpha, cur_pos, next_pos):
    try:
        return asin(sin(alpha) * cur_pos / next_pos)
    except:
        global dir
        dir *= -1
        return alpha



N = 10000 # точность
om = 3.4e14 # омега
om_help = (1 - ((0.35e14) / om) ** 2)
R = 0.6 # радиус
n2 = 1 # внутрення среда
y0 = -0.3 # старт Y
alpha = radians(22) # начальный угол
length = 0

dir = 1
alpha_cur = pi / 2 - angle(alpha, n2, n1(y0, om_help))
y_value = []
z_value = []
y_cur = y0
z_cur = 0
n_cur = n1(y0, om_help)
while z_cur < zf(y_cur):
    y_value.append(y_cur)
    z_value.append(z_cur)
    y_cur += abs(sin(pi/2 - alpha_cur)) * dir / N
    z_cur += cos(pi/2 - alpha_cur) / N
    n_next = n1(y_cur, om_help)
    alpha_cur = angle(alpha_cur, n_cur, n_next)
    n_cur = n_next
    length += 1 / N

y_array = np.linspace(-R, R, N)
z_array = [zf(y) for y in y_array]

plt.plot(z_value, y_value, color='black')
plt.plot(z_array, y_array, color="blue")
plt.plot([-1, 0], [y0 - tan(alpha), y0], color='green')

plt.plot([0, 25], [-R, -R], color='red')
plt.plot([0, 25], [R, R], color='red')
plt.plot([0, 0], [-R, R], color='red')

print(length)
plt.show()
input()