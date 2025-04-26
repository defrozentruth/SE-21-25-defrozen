import numpy as np
import matplotlib.pyplot as plt

alpha = np.deg2rad(-30)
vert_direct = -1
y0 = -0.4
z0 = 0
omega = 3.2 * 10 ** 14
n2 = 1
R = 0.8
eps = 0.00001
S = 0
arrY = [y0]
arrZ = [z0]

def f1(y):
    return 1.4 + 0.12 * np.cos(6 * y)


def Zf(y):
    return 28 + 3 * np.sin(17.951958020513104 * y)


def n1(y, w):
    return f1(y) * (1 - ((0.35 * 10 ** 14) / w) ** 2)


beta = np.arcsin((np.sin(alpha) * n2) / n1(y0, omega))
arrY.append(y0 + np.sin(beta) * eps)
arrZ.append(0 + np.cos(beta) * eps)
next_n = n1(arrY[len(arrY) - 1], omega)
cur_n = n1(y0, omega)
alpha = np.pi / 2 - beta
sinB = (np.sin(alpha) * cur_n) / next_n
sinB = np.clip(sinB, -1, 1)  # ограничение аргумента в [-1, 1]
beta = np.arcsin(sinB)
S += eps

while abs(Zf(arrY[len(arrY) - 1]) - arrZ[len(arrZ) - 1]) >= 0.001:
    if abs(1 - np.sin(beta)) <= 0.000000001:
        beta = alpha
        vert_direct *= -1

    arrY.append(arrY[len(arrY) - 1] + np.cos(beta) * eps * vert_direct)
    arrZ.append(arrZ[len(arrZ) - 1] + np.sin(beta) * eps)
    next_n = n1(arrY[len(arrY) - 1], omega) if R >= abs(arrY[len(arrY) - 1]) else n2
    cur_n = n1(arrY[len(arrY) - 2], omega)

    alpha = beta
    sinB = (np.sin(alpha) * cur_n) / next_n
    sinB = np.clip(sinB, -1, 1)
    beta = np.arcsin(sinB)
    S += eps


print(S)
y = np.arange(-R, R, 0.00001)
plt.plot(arrZ, arrY, "r", Zf(y), y, "b", [0, 35], [R, R], "b", [0, 35], [-R, -R], "b")
plt.show()