from math import *
import numpy as np
import matplotlib.pyplot as plt

R = 0.7
n2 = 1
omega = 3
y0 = 0.1
alpha = radians(25)

n1_coeff = (1 - pow((0.35 / omega), 2))
N = 17001
h = 2 * R / N
length = 0


def f1(y):
    return 1.5 - 0.3 * pow(y, 2)


def Zf(y):
    return 20 + 3 * sin(17.951958020513104 * y)


def n1(y):
    return f1(y) * n1_coeff


layers_n = [n1(i * h + h / 2 - R) for i in range(N)]
layers_zf = [Zf(i * h + h / 2 - R) for i in range(N)]
layers_coords = [i * h - R for i in range(N)]

begin_layer_index = 0
for i in range(len(layers_coords) // 2, len(layers_coords)):
    if y0 < layers_coords[i]:
        begin_layer_index = i - 1
        break

beta = asin(sin(alpha) * n2 / layers_n[begin_layer_index])
z = h / tan(beta)
length = h / sin(beta)

n1 = layers_n[begin_layer_index]

n1_index = begin_layer_index
n2_index = n1_index + 1

up = True
down = False
direction = up

plt.ylim(-R, R)
plt.xlim(0, 20)
plt.ylabel('y', loc='top')
plt.xlabel('z', loc='right')

alpha = radians(90) - beta
while z < layers_zf[n1_index]:
    z += tan(alpha) * h
    length += h / cos(alpha)
    if sin(alpha) > layers_n[n2_index] / layers_n[n1_index] and direction == up:
        direction = down
        plt.plot([z - tan(alpha) * h, z], [layers_coords[n2_index], layers_coords[n1_index]], color='black')
        n2_index -= 2

    elif sin(alpha) > layers_n[n2_index] / layers_n[n1_index] and direction == down:
        direction = up
        plt.plot([z - tan(alpha) * h, z], [layers_coords[n1_index], layers_coords[n1_index + 1]], color='black')
        n2_index += 2

    else:
        beta = asin(sin(alpha) * layers_n[n1_index] / layers_n[n2_index])
        if direction == up:
            plt.plot([z - tan(beta) * h, z], [layers_coords[n2_index], layers_coords[n2_index + 1]], color='black')
            n1_index += 1
            n2_index += 1
            alpha = beta
        else:
            plt.plot([z - tan(beta) * h, z], [layers_coords[n1_index], layers_coords[n2_index]], color='black')
            n1_index -= 1
            n2_index -= 1
            alpha = beta

plt.show()
print(f'length = {length}')
