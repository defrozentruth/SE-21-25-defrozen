import numpy as np
import matplotlib.pyplot as plt


def f1(y):
    return 1.4 - 0.12 * np.cos(5 * y)


def z_f(y):
    return 28 + 3 * np.sin(17.951958020513104 * y)


def n1(y):
    return f1(y) * (1 - ((0.35 * 10 ** 14) / (3.3 * (10 ** 14))) ** 2)


def plot_trajectory(y_array, z_array, r):
    y = np.arange(-r, r, 0.001)
    plt.plot(z_array, y_array, 'r', label='График траектории луча')
    plt.plot(z_f(y), y, 'b', label='График выходного торца волновода')
    plt.axhline(r, color='b', linestyle='--')
    plt.axhline(-r, color='b', linestyle='--')
    plt.axvline(0, color='b', linestyle='--')
    plt.xlabel('Z координата')
    plt.ylabel('Y координата')
    plt.legend()
    plt.grid()
    plt.show()


def search(a0, n0, r, part, y0, z0):
    a0 = np.deg2rad(a0)
    result_len = 0
    direction = 1
    y_array = []
    z_array = []
    y_array.append(y0)
    z_array.append(z0)
    b = np.arcsin((np.sin(a0) * n0) / n1(y0))
    y_array.append(y0 + np.sin(b) * part)
    z_array.append(0 + np.cos(b) * part)
    n_2 = n1(y_array[-1])
    n_1 = n1(y0)
    a = np.pi / 2 - b
    b = np.arcsin(np.clip((np.sin(a) * n_1) / n_2, -1, 1))
    result_len += part
    while z_array[-1] <= z_f(y_array[-1]):
        if 1 == abs(np.sin(b)):
            b = a
            direction *= -1
        y_array.append(y_array[-1] + np.cos(b) * part * direction)
        z_array.append(z_array[-1] + np.sin(b) * part)
        if abs(y_array[-1]) <= r:
            n_2 = n1(y_array[-1])
        else:
            n_2 = n0
        n_1 = n1(y_array[-2])
        a = b
        b = np.arcsin(np.clip((np.sin(a) * n_1) / n_2, -1, 1))
        result_len += part
    return result_len, y_array, z_array


def main():
    a0 = 20
    n0 = 1
    r = 0.8
    y0 = 0.2
    z0 = 0
    one_part = 0.0001
    result_len, y_array, z_array = search(a0, n0, r, one_part, y0, z0)
    print(f"Результирующая длина траектории = {result_len}")
    plot_trajectory(y_array, z_array, r)


if __name__ == "__main__":
    main()
