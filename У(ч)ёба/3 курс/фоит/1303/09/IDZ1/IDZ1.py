import numpy as np
import matplotlib.pyplot as plt


def f1(y):
    return 1.4 + 0.12 * np.cos(3 * y)


def n1(y):
    global omega

    return f1(y) * (1 - ((0.35 * 10 ** 14) / omega) ** 2)


def z_f(y):
    return 18 + 3 * np.sin(17.951958020513104 * y)


def get_new_angle(curr_angle, n1, n2):
    return np.arcsin(np.clip((np.sin(curr_angle) * n1) / n2, -1, 1))


def model(r, n_outer, y0, z0, alpha_0):
    global step

    alpha_0 = np.deg2rad(alpha_0)
    s = 0
    course = 1
    arr_y = [y0]
    arr_z = [z0]

    beta = get_new_angle(alpha_0, n_outer, n1(y0))
    arr_y += [y0 + step * np.sin(beta)]  # first y coord
    arr_z += [z0 + step * np.cos(beta)]  # first z coord

    n_1 = n1(arr_y[-2])  # refractive coeff of first area take from prev coord
    n_2 = n1(arr_y[-1])  # # refractive coeff of second area take from last coord

    alpha = np.pi / 2 - beta  # new first angle
    beta = get_new_angle(alpha, n_1, n_2)
    s += step  # accum length

    while arr_z[-1] < z_f(arr_y[-1]):  # while haven't reached yet
        if abs(np.sin(beta)) >= 1:
            course *= -1
            beta = alpha

        arr_y += [arr_y[-1] + step * np.cos(beta) * course]
        arr_z += [arr_z[-1] + step * np.sin(beta)]

        n_1 = n1(arr_y[-2])
        n_2 = n1(arr_y[-1]) if abs(arr_y[-1]) <= r else n_outer  # possible to exceed radius

        alpha = beta
        beta = get_new_angle(alpha, n_1, n_2)

        s += step  # accum length

    return arr_y, arr_z, s


def plot_model(y_values, z_values, r):
    global step
    y = np.arange(-r, r, step)
    plt.plot(z_values, y_values, 'r')
    plt.plot(z_f(y), y, 'c')

    plt.axhline(r, color='b')
    plt.axhline(-r, color='b')

    plt.xlabel('Ось Z')
    plt.ylabel('Ось Y')
    plt.show()


step = 0.001
radius = 0.8
n_out = 1
omega = 3.1 * 10 ** 14
y_start = 0.4
z_start = 0
alpha_start = 40

y_points, z_points, trajectory_length = model(radius, n_out, y_start, z_start, alpha_start)
print("Длина траектории =", trajectory_length)
plot_model(y_points, z_points, radius)
