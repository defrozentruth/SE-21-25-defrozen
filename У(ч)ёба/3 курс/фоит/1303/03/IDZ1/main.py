import matplotlib.pyplot as plt
from math import *


def Zf(y) -> float:
    return 50 + 3 * sin(17.951958020513104 * y)


def f1(y: float) -> float:
    return 1.8 - 0.15 * pow(y, 2)


def coefficient_n1(w: float, ) -> float:
    return 1 - pow(0.35 / w, 2)


def get_start_step(y0: float, steps: dict) -> int or None:
    idx = 0
    while idx < len(steps) / 2:
        if steps[idx][0] < y0 < steps[idx][1]:
            return idx
        idx += 1


def get_n1(y: float) -> float:
    return f1(y) * coefficient


def main() -> None:
    plt.figure(figsize=(15, 5))
    plt.xlabel("Z", loc="right")
    plt.ylabel("Y", loc="top")
    plt.locator_params(axis='x', nbins=20)
    plt.ylim(-radius, radius)
    plt.xlim(0, 55)

    # stats for layers
    cf_on_step = {i - ((N - 1) / 2): get_n1(i * step + step / 2 - radius) for i in range(N)}
    z_exit = {i - ((N - 1) / 2): Zf(i * step + step / 2 - radius) for i in range(N)}
    steps = {i - ((N - 1) / 2): (i * step - radius, (i + 1) * step - radius) for i in range(N)}

    for key, value in z_exit.items():
        plt.plot(value, key * step + step / 2,
                 marker="o", markersize=0.5, markeredgecolor='black', markerfacecolor="black")

    # start values
    n_alpha = n2
    n_beta_ind = get_start_step(start_y, steps)
    alpha = radians(start_alpha)

    flag = 0
    z = 0
    length = 0

    # first step
    beta = asin(sin(alpha) * n_alpha / cf_on_step[n_beta_ind])
    plt.plot([z, z + (steps[n_beta_ind][1] - start_y) / tan(beta)], [start_y, steps[n_beta_ind][1]])

    length += (steps[n_beta_ind][1] - start_y) / sin(beta)
    z += (steps[n_beta_ind][1] - start_y) / tan(beta)
    alpha = pi / 2 - beta

    n_alpha = cf_on_step[n_beta_ind]
    n_alpha_ind = n_beta_ind
    n_beta_ind += 1

    while True:

        if z >= z_exit[n_alpha_ind]:
            # get delta z
            z_to_edge = z_exit[n_alpha_ind] - (z - step * tan(alpha))

            # get previous value of length and add length of trajectory to edge
            length -= step / cos(alpha)
            length += z_to_edge / sin(alpha)

            break

        if sin(alpha) > (cf_on_step[n_beta_ind] / n_alpha):
            # обработка случая отражения

            if not flag:
                plt.plot([z, z + step * tan(alpha)], [steps[n_beta_ind][0], steps[n_beta_ind - 2][1]],
                         color='blue')
                flag += 1
                n_beta_ind -= 2

            else:
                plt.plot([z, z + step * tan(alpha)], [steps[n_beta_ind][1], steps[n_beta_ind + 2][0]],
                         color='red')
                flag -= 1
                n_beta_ind += 2

        else:
            # обработка стандартного исхода
            beta = asin(sin(alpha) * n_alpha / cf_on_step[n_beta_ind])

            if flag:
                plt.plot([z, z + step * tan(beta)], [steps[n_beta_ind][1], steps[n_beta_ind][0]],
                         color='blue')
                n_alpha = cf_on_step[n_beta_ind]
                n_alpha_ind = n_beta_ind
                n_beta_ind -= 1

            if not flag:
                plt.plot([z, z + step * tan(beta)], [steps[n_beta_ind][0], steps[n_beta_ind][1]],
                         color='red')
                n_alpha = cf_on_step[n_beta_ind]
                n_alpha_ind = n_beta_ind
                n_beta_ind += 1

            alpha = beta

        length += step / cos(alpha)
        z += step * tan(alpha)

    print(f"length = {length}")
    plt.show()


if __name__ == "__main__":
    # consts
    radius: float = 0.4
    n2: int = 1
    start_y: float = 0.2
    start_alpha: int = 10

    # get n1 coefficient
    omega: float = 3.2
    coefficient: float = coefficient_n1(omega)

    # get steps
    N: int = 100001
    step: float = 2 * radius / N

    main()
