import numpy as np
import matplotlib.pyplot as p

alpha = -32  # угол в градусах
direct = -1  # направление
y0 = -0.1  # начальная координата по y
z0 = 0  # начальная координата по z
w = 3 * 10 ** 14  # омега
n2 = 1  # коэффициент преломления
R = 1.2  # радиус
epsilon = 0.00001  # шаг
S = 0  # длина траектории
arr_y = [y0]  # ось y
arr_z = [z0]  # ось z


def f1(y):
    return 1.5 + 0.3 * np.cos(0.8 * y) ** 3


def Zf(y):
    return 42 + 3 * np.sin(17.951958020513104 * y)


def n1(y, w):
    return f1(y) * (1 - ((0.35 * 10 ** 14) / w) ** 2)


def algorithm():
    global alpha
    global direct
    global S

    # расчёт углов альфа и бета
    alpha = np.deg2rad(alpha)
    beta = np.arcsin((np.sin(alpha) * n2) / n1(y0, w))

    # новые значения y и z
    arr_y.append(y0 + np.sin(beta) * epsilon)
    arr_z.append(0 + np.cos(beta) * epsilon)

    # новое значения n1 и n2
    new_n1 = n1(arr_y[len(arr_y) - 1], w)
    new_n2 = n1(y0, w)

    # новый угол
    new_alpha = np.pi / 2 - beta
    new_beta = np.arcsin((np.sin(new_alpha) * new_n2) / new_n1)

    # прибавляем в длину
    S += epsilon

    # while arr_z[len(arr_z) - 1] <= Zf(arr_y[len(arr_y) - 1]):
    while abs(Zf(arr_y[len(arr_y) - 1]) - arr_z[len(arr_z) - 1]) >= 0.001:
        if abs(1 - np.sin(new_beta)) <= 0.000000001:
            new_beta = new_alpha
            direct *= -1

        arr_y.append(arr_y[len(arr_y) - 1] + np.cos(new_beta) * epsilon * direct)
        arr_z.append(arr_z[len(arr_z) - 1] + np.sin(new_beta) * epsilon)

        new_n1 = n1(arr_y[len(arr_y) - 1], w) if R >= abs(arr_y[len(arr_y) - 1]) else n2
        new_n2 = n1(arr_y[len(arr_y) - 2], w)

        new_alpha = new_beta
        new_beta = np.arcsin((np.sin(new_alpha) * new_n2) / new_n1)

        S += epsilon


def main():
    algorithm()
    print(f"Длина траектории светового луча S = {S}")
    y = np.arange(-R, R, 0.001)
    p.plot(arr_z, arr_y, "r", Zf(y), y, "b", [0, 45], [R, R], "b", [0, 45], [-R, -R], "b")
    p.show()


if __name__ == '__main__':
    main()
