import numpy as np
import matplotlib.pyplot as plt

alpha = 20  
direction = 1
y_0 = 0.3
z_0 = 0
w = 3.6 * 10 ** 14
n2 = 1
R = 0.8
h = 0.00001
traj_len = 0
arr_y = [y_0]
arr_z = [z_0]


def f1(y):
    return 1.3 - 0.15 * np.cos(4 * y)


def Z_f(y):
    return 12 + 3 * np.sin(17.951958020513104 * y)


def n1(y, w):
    return f1(y) * (1 - ((0.35 * 10 ** 14) / w) ** 2)


def algorithm():
    global alpha
    global direction
    global traj_len

    alpha = np.deg2rad(alpha)
    beta = np.arcsin((np.sin(alpha) * n2) / n1(y_0, w))

    arr_y.append(y_0 + np.sin(beta) * h)
    arr_z.append(0 + np.cos(beta) * h)

    new_n1 = n1(y_0, w)
    new_n2 = n1(arr_y[len(arr_y) - 1], w)

    new_alpha = np.pi / 2 - beta

    angle = (np.sin(new_alpha) * new_n1) / new_n2
    angle = np.clip(angle, -1, 1)
    new_beta = np.arcsin(angle)

    traj_len += h

    while arr_z[-1] <= Z_f(arr_y[-1]):
        if 1 - abs(np.sin(new_beta)) <= 0.000000000001:
            new_beta = new_alpha
            direction *= -1

        arr_y.append(arr_y[-1] + np.cos(new_beta) * h * direction)
        arr_z.append(arr_z[-1] + np.sin(new_beta) * h)

        if abs(arr_y[-1]) >= R:
            new_n2 = n2
        else:
            new_n2 = n1(arr_y[-1], w)

        new_n1 = n1(arr_y[-2], w)

        new_alpha = new_beta

        arg = (np.sin(new_alpha) * new_n1) / new_n2
        arg = np.clip(arg, -1, 1)
        new_beta = np.arcsin(arg)

        traj_len += h


def main():
    algorithm()
    print(f"Длина траектории луча = {traj_len}")
    y = np.arange(0, R, 0.0001)
    plt.plot(arr_z, arr_y, "red")
    plt.plot(Z_f(y), y, "blue")
    plt.show()


if __name__ == '__main__':
    main()
