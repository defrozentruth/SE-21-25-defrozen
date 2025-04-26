import matplotlib.pyplot as plt
from math import *

# Поменять
R = 1.4
n0 = 1
omega = 3.5
y0 = -0.8
alpha0 = radians(-20)
# Поменять

N = 1000    # Количество слоев разбиения
h = 2*R/N   # Шаг разбиения
coefficient = 1 - pow((0.35/omega), 2)


def f1(y):
    return 1.3 - 0.15 * cos(4*y)


def Zf(y):
    return 12 + 3 * sin(17.951958020513104 * y)


def n1(y):
    return f1(y)*coefficient


def find_beta(alpha, n_alpha, n_beta):
    return asin(sin(alpha)*n_alpha/n_beta)


def is_reflection(alpha, n_alpha, n_beta, layer_alpha, direction):
    if sin(alpha) > n_beta/n_alpha or (abs(layer_alpha) == floor(N/2) and get_sign(layer_alpha) == direction):
        return True
    return False


def get_sign(x):
    if x != 0:
        return int(x/abs(x))
    return 1


def main():
    plt.ylabel("y")
    plt.xlabel("z")
    plt.ylim(-R, R)
    plt.xlim(-1, 35)

    n_arr = dict()
    z_arr = dict()

    for i in range(N):
        n_arr[i - floor(N/2)] = n1((i - floor(N/2))*h + h/2)
        z_arr[i - floor(N/2)] = Zf((i - floor(N / 2))*h + h/2)
        if h*(i-floor(N/2)) + h/2 < y0 < h*(i-floor(N/2) + 1) + h/2:
            start_index = i-floor(N/2) + 1

        plt.plot([Zf((i - floor(N / 2)) * h + h / 2), Zf((i - floor(N / 2)) * h + h / 2)],
                 [(i - floor(N/2))*h - h/2, (i - floor(N/2))*h + h - h/2])
        plt.plot([0, Zf((i - floor(N / 2)) * h + h / 2)], [(i - floor(N / 2)) * h + h / 2, (i - floor(N / 2)) * h + h / 2])
    n_arr[ceil(N/2)] = 1
    n_arr[-ceil(N/2)] = 1

    alpha_layer = start_index
    alpha = pi/2 - find_beta(alpha0, n0, n_arr[alpha_layer])
    h0 = start_index*h - h/2 - y0
    path_len = h0/cos(alpha)
    z_len = h0*tan(alpha)
    z, y = [0], [y0]
    direction = -1
    n_alpha = n_arr[alpha_layer]
    n_beta = n_arr[alpha_layer+direction]

    while z_len < z_arr[alpha_layer]:
        y.append(alpha_layer * h + direction*h/2)
        z.append(z_len)
        if is_reflection(alpha, n_alpha, n_beta, alpha_layer, direction):
            direction = -direction
        else:
            alpha = find_beta(alpha, n_alpha, n_beta)
            alpha_layer += direction

        n_alpha = n_arr[alpha_layer]
        n_beta = n_arr[alpha_layer + direction]

        path_len += h / cos(alpha)
        z_len += h * tan(alpha)

    plt.plot(z, y, marker='o')
    print(path_len)

    plt.show()


if __name__ == "__main__":
    main()
