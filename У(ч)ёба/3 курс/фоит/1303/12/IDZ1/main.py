from math import sqrt, sin, radians, pi, asin, tan
import matplotlib.pyplot as plt

R = 0.6
N_2 = 1
OMEGA = 3.4 * 10**14
Y_0 = -0.2
ALPHA_0 = radians(-20)
COUNT_LAYERS = 1000000


def f1(y):
    return 1.4 + sqrt(0.6 - y**2)


def Zf(y):
    return 28 + 3*sin(17.951958020513104 * y)


def n(y):
    return f1(y) * (1 - ((0.35 * 10 ** 14) / OMEGA) ** 2)


def n1(y):
    return f1(y) * (1-(0.35 * 10**14) ** 2)


def new_angle(n1, n2, sin_1):
    return (n1/n2) * sin_1

# функция для создания графика с помощью mathplotlib
def make_chart(way_x, way_y, wave_x, wave_y):
    plt.xlabel("Z")
    plt.ylabel("Y")
    plt.title("Траектория волны")
    plt.ylim(-R, R)
    plt.plot(way_x, way_y)
    plt.plot(wave_x, wave_y)
    plt.show()
# генерация значений координат волны
def make_wave():
    wave_x = []
    wave_y = []
    x = -R
    while x < R:
        x += 0.001
        wave_x.append(Zf(x))
        wave_y.append(x)
    return wave_x, wave_y

# вычисляем значения way_x, way_y, length
def solve():
    dy = R*2/COUNT_LAYERS
    x = 0
    y = Y_0
    way_x = [x]
    way_y = [y]
    alpha_1 = ALPHA_0
    n1 = 1
    n2 = n(y)
    alpha_2 = pi/2 - asin(new_angle(n1, n2, abs(sin(alpha_1))))
    length = 0
    flag_ref = False
    if ALPHA_0 < 0:
        dy *= -1
    while abs(Zf(y) - x) >= 0.05:
        if flag_ref or abs(abs(y) - R) < 0.0005:
            alpha_2 = alpha_1
            dy *= - 1
        dx = abs(dy) * abs(tan(alpha_2))
        x += dx
        y += dy
        length += sqrt(dx**2+dy**2)
        way_x.append(x)
        way_y.append(y)
        n1 = n2
        alpha_1 = alpha_2
        n2 = n(y)
        if new_angle(n1, n2, sin(alpha_1)) >= 1:
            flag_ref = True
            continue
        alpha_2 = asin(new_angle(n1, n2, sin(alpha_1)))
        flag_ref = False
    return way_x, way_y, length


way_x, way_y, length = solve()
wave_x, wave_y = make_wave()
print(length)
make_chart(way_x, way_y, wave_x, wave_y)
