import numpy as np
import sympy as sp
import random as ran
import matplotlib.pyplot as plt

step = 0.04
find_phi = 2
phi_1 = 6
phi_2 = -5
size = 260
offset = 0.2
epsilon = 0.01
x = np.arange(-5 - offset, 5 + offset + step, step)
y = np.arange(-5 - offset, 5 + offset + step, step)
array_of_points = []
iterationFrag = 0
iterationLen = 0
x_points = []
y_points = []
color = []


class Point:
    def __init__(self, x, y, phi, inElectrode):
        self.x = x
        self.y = y
        self.phi = phi
        self.inElectrode = inElectrode


def array_init():
    for i in range(0, size):
        array_of_points.append([])
        for j in range(0, size):
            x_cord = -5 - offset + j * step
            y_cord = -5 - offset + i * step
            array_of_points[i].append(Point(x_cord, y_cord, 0, False))


def external_electrode(x, y):
    return x ** 2 + y ** 2 - 25


def electrode_1(x, y):
    return np.abs(x + 1.8) ** 2 + 0.8 * np.abs(y) ** 2 - 0.6


def electrode_2(x, y):
    return 0.5 * np.abs(-1.8 + x) ** 4 + 0.3 * np.abs(y) ** 4 - 0.5


def initElectrode():
    X, Y = np.meshgrid(x, y)

    external_electrode_value = external_electrode(X, Y)
    electrode_1_value = electrode_1(X, Y)
    electrode_2_value = electrode_2(X, Y)

    plt.contour(X, Y, external_electrode_value, [0], colors='blue')
    plt.contour(X, Y, electrode_1_value, [0], colors='red')
    plt.contour(X, Y, electrode_2_value, [0], colors='red')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')


def fragmentation():
    for i in range(0, size):
        for j in range(0, size):
            x_cord = -5 - offset + j * step
            y_cord = -5 - offset + i * step
            if electrode_1(x_cord, y_cord) <= 0:
                array_of_points[i][j] = Point(x_cord, y_cord, phi_1, False)
            elif electrode_2(x_cord, y_cord) <= 0:
                array_of_points[i][j] = Point(x_cord, y_cord, phi_2, False)
            elif ((x_cord ** 2 + y_cord ** 2 < 25) and (np.abs(x_cord + 1.8) ** 2 + 0.8 * np.abs(y_cord) ** 2 > 0.6)
                  and (0.5 * np.abs(-1.8 + x_cord) ** 4 + 0.3 * np.abs(y_cord) ** 4 > 0.5)):
                array_of_points[i][j] = Point(x_cord, y_cord, ran.uniform(phi_2, phi_1), True)
                x_points.append(array_of_points[i][j].x)
                y_points.append(array_of_points[i][j].y)
    plt.scatter([x_points], [y_points], c='gray', s=1)


def algorithm():
    global iterationFrag
    new_phi_array_of_points = [[0] * size for _ in range(size)]
    iteration = True
    while iteration:
        iterationFrag += 1
        iteration = False
        for i in range(0, size):
            for j in range(0, size):
                if array_of_points[i][j].inElectrode:
                    new_phi_array_of_points[i][j] = (array_of_points[i + 1][j].phi
                                                     + array_of_points[i - 1][j].phi
                                                     + array_of_points[i][j + 1].phi
                                                     + array_of_points[i][j - 1].phi) / 4
        for i in range(0, size):
            for j in range(0, size):
                if array_of_points[i][j].inElectrode:
                    if not iteration and (np.abs(array_of_points[i][j].phi - new_phi_array_of_points[i][j]) > epsilon):
                        iteration = True
                    array_of_points[i][j].phi = new_phi_array_of_points[i][j]
    print(f'Количество итераций алгоритма: {iterationFrag}')


def equipotentialPoints(LeftTopPoint, RightTopPoint, LeftBottomPoint, RightBottomPoint):
    global iterationLen
    points = []

    a, k1, k2 = sp.symbols('a k1 k2')
    top_triangle_eq1 = a + k1 * LeftTopPoint.x + k2 * LeftTopPoint.y - LeftTopPoint.phi
    top_triangle_eq2 = a + k1 * RightTopPoint.x + k2 * RightTopPoint.y - RightTopPoint.phi
    top_triangle_eq3 = a + k1 * LeftBottomPoint.x + k2 * LeftBottomPoint.y - LeftBottomPoint.phi
    top_triangle_solve = sp.nsolve((top_triangle_eq1, top_triangle_eq2, top_triangle_eq3), (a, k1, k2), (1, 1, 1))

    xTop = (find_phi - top_triangle_solve[0] - top_triangle_solve[2] * LeftTopPoint.y) / top_triangle_solve[1]
    if LeftTopPoint.x < xTop < RightTopPoint.x:
        plt.scatter(xTop, LeftTopPoint.y, c='black', s=1)
        points.append((xTop, LeftTopPoint.y))

    yLeft = (find_phi - top_triangle_solve[0] - top_triangle_solve[1] * LeftTopPoint.x) / top_triangle_solve[2]
    if LeftBottomPoint.y < yLeft < LeftTopPoint.y:
        plt.scatter(LeftTopPoint.x, yLeft, c='black', s=1)
        points.append((LeftTopPoint.x, yLeft))

    a, k1, k2 = sp.symbols('a k1 k2')
    bottom_triangle_eq1 = a + k1 * RightBottomPoint.x + k2 * RightBottomPoint.y - RightBottomPoint.phi
    bottom_triangle_eq2 = a + k1 * RightTopPoint.x + k2 * RightTopPoint.y - RightTopPoint.phi
    bottom_triangle_eq3 = a + k1 * LeftBottomPoint.x + k2 * LeftBottomPoint.y - LeftBottomPoint.phi
    bottom_triangle_solve = sp.nsolve((bottom_triangle_eq1, bottom_triangle_eq2, bottom_triangle_eq3),
                                      (a, k1, k2), (1, 1, 1))

    xBottom = (find_phi - bottom_triangle_solve[0] -
               bottom_triangle_solve[2] * RightBottomPoint.y) / bottom_triangle_solve[1]
    if LeftBottomPoint.x < xBottom < RightBottomPoint.x:
        plt.scatter(xBottom, RightBottomPoint.y, c='black', s=1)
        points.append((xBottom, RightBottomPoint.y))

    yRight = (find_phi - bottom_triangle_solve[0] -
              bottom_triangle_solve[1] * RightBottomPoint.x) / bottom_triangle_solve[2]
    if RightBottomPoint.y < yRight < RightTopPoint.y:
        plt.scatter(RightBottomPoint.x, yRight, c='black', s=1)
        points.append((RightBottomPoint.x, yRight))
    if len(points) == 2:
        return np.sqrt((np.abs(float(points[0][0] - points[1][0])) ** 2) +
                       (np.abs(float(points[0][1] - points[1][1])) ** 2))
    return 0


def findLength():
    lenEquip = 0
    for i in range(0, size):
        for j in range(0, size):
            if array_of_points[i][j].inElectrode:
                if find_phi - 0.2 < array_of_points[i][j].phi < find_phi + 0.2:
                    lenEquip += equipotentialPoints(array_of_points[i][j],
                                                    array_of_points[i][j + 1],
                                                    array_of_points[i - 1][j],
                                                    array_of_points[i - 1][j + 1])
    print(f'Количество итерация для нахождения длины: {iterationLen}')
    print(f'Длина: {lenEquip}')


if __name__ == '__main__':
    array_init()
    initElectrode()
    fragmentation()
    algorithm()
    findLength()
    plt.show()
