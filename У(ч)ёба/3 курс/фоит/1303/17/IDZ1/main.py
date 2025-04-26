import matplotlib.pyplot as plt
import numpy as np


radius: float = 1.2
n2: int = 1
omega: float = 3.2
y0: float = 0.4
alpha: float = np.deg2rad(42)


def f1(y: float) -> float:
    return 1.4 - 0.18 * y ** 4


def zf(y):
    return 12 + 2 * np.sin(17.951958020513104 * y)


def calculate_n1(y: float) -> float:
    return f1(y) * (1 - (0.35 / omega) ** 2)


def calculate_sin0() -> (float, int):
    n1_0 = calculate_n1(y0)
    sin_beta = np.sin(np.pi / 2 - np.arcsin(np.sin(np.abs(alpha)) * n2 / n1_0))
    return sin_beta, np.sign(alpha)


steps_cnt: int = 10000
delta: float = 2 * radius / steps_cnt

y: float = y0
z: float = 0
n: float = calculate_n1(y)
sin, sign = calculate_sin0()
length: float = 0


def next_step() -> None:
    global y, z, n, sin, sign, length

    length += delta
    y += sign * np.sqrt(1 - sin ** 2) * delta
    z += np.abs(sin) * delta

    new_n: float = calculate_n1(y) if radius >= np.abs(y) else n2
    new_sin: float = sin * n / new_n

    if np.abs(new_sin) >= 1:
        sign *= -1
    else:
        n = new_n
        sin = new_sin


y_points: list[float] = []
z_points: list[float] = []
end_y_points: list[float] = []
end_z_points: list[float] = []


def process() -> None:
    global y_points, z_points, end_y_points, end_z_points

    while z < zf(y):
        y_points.append(y)
        z_points.append(z)
        next_step()

    end_y_points = np.arange(-radius, radius, delta)
    end_z_points = zf(end_y_points)


if __name__ == '__main__':
    process()

    print(length)

    bottom_line_end = end_z_points[0]
    top_line_end = end_z_points[-1]

    wave_color = 'blue'
    lines_color = 'green'
    end_color = 'orange'

    plt.plot(z_points, y_points, wave_color,
             end_z_points, end_y_points, end_color,
             [0, bottom_line_end], [-radius, -radius], lines_color,
             [0, top_line_end], [radius, radius], lines_color)
    plt.show()
