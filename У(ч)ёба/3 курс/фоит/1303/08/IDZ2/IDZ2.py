import random
from itertools import chain

import matplotlib.pyplot as plt
import numpy as np


class Point:
    def __init__(self, x, y, f):
        self.x = x
        self.y = y
        self.f = f

def isIn(x, y):
    res = x ** 2 + y ** 2 <= 25
    res1 = 0.8 * abs(-1.5 + x) ** 3.5 + 0.3 * abs(1.5 + y) ** 3.5 >= 0.6
    res2 = abs(1.5 + x) ** 4 + abs(-1.5 + y) ** 4 >= 0.8
    return res and res1 and res2


F1 = 5
F2 = 5
f = 3
step = 0.1
start = -5
finish = 6
size = 4
epsilon = 0.00001

t1 = np.arange(start, finish, step)
arr_x = []
arr_y = []
arr_point = []


def inicialisation():
    for x in t1:
        arr_point.append([])
        for y in t1:
            if isIn(x, y):
                if abs(x ** 2 + y ** 2 - 25) <= 1:
                    f = 0
                elif abs(0.8 * abs(-1.5 + x) ** 3.5 + 0.3 * abs(1.5 + y) ** 3.5 - 0.6) <= 0.4:
                    f = F1
                elif abs(abs(1.5 + x) ** 4 + abs(-1.5 + y) ** 4 - 0.8) <= 0.4:
                    f = F2
                else:
                    f = random.random() * (abs(F1) + abs(F2)) + min(F1, F2)
            else:
                f = None
            point = Point(x, y, f)
            arr_point[-1].append(point)


def iteration():
    max_delta = 0
    for y in range(1, len(arr_point) - 2):
        for x in range(1, len(arr_point[y]) - 2):
            neighbours = [arr_point[y][x - 1].f,
                          arr_point[y][x + 1].f,
                          arr_point[y - 1][x].f,
                          arr_point[y + 1][x].f]
            if any(potent is None for potent in neighbours):
                continue
            delta = max(neighbours) - min(neighbours)
            if delta > max_delta:
                max_delta = delta
            arr_point[y][x].f = sum(neighbours) / 4
    return max_delta


def repeat(epsilon):
    previous_delta = abs(F1) + abs(F2) + 10  # верхняя граница разности, с хвостиком чтоб наверняка
    n = 0
    while True:
        n += 1
        new_delta = iteration()
        if (abs(previous_delta - new_delta) < epsilon):
            break
        previous_delta = new_delta


def add(point1, point2):
    arr_x.append(point1.x)
    arr_x.append(point2.x)
    arr_y.append(point1.y)
    arr_y.append(point2.y)


def findpoint(tmp, neighboor, flag):
    diapason = abs(tmp.f - neighboor.f)
    if diapason == 0:  # сработает если ищем 0
        add(tmp, neighboor)
        return True
    s = abs(f - tmp.f)
    if flag == 'x':
        arr_x.append(tmp.x + (s / diapason) * step)
        arr_y.append(tmp.y)
    else:
        arr_x.append(tmp.x)
        arr_y.append(tmp.y + (s / diapason) * step)
    return False


def find(f):
    for i in range(1, len(arr_point) - 2):
        for j in range(1, len(arr_point[i]) - 2):
            tmp = arr_point[i][j]
            right = arr_point[i + 1][j]
            down = arr_point[i][j + 1]
            if tmp.f is None or right.f is None or down.f is None:
                continue
            if tmp.f <= f <= right.f or tmp.f >= f >= right.f:
                findpoint(tmp, right, 'x')

            if tmp.f <= f <= down.f or tmp.f >= f >= down.f:
                findpoint(tmp, down, 'y')


def sort():
    points = list(zip(arr_x, arr_y))
    leftmost_point, *_, rightmost_point = sorted(points, key=lambda lst: lst[0])
    x1, y1 = leftmost_point
    x2, y2 = rightmost_point

    border_slope = (y2 - y1) / (x2 - x1)

    points_below_border = [(x1, y1)]
    points_above_border = [(x2, y2)]

    for x, y in points:
        border = border_slope * (x - x1) + y1
        if y < border:
            points_below_border.append((x, y))
        elif y > border:
            points_above_border.append((x, y))

    points_below_border.sort()
    points_above_border.sort(reverse=True)

    points_above_border.append((x1, y1))

    merged_points = points_below_border + points_above_border

    x_lst = [x for x, _ in merged_points]
    y_lst = [y for _, y in merged_points]
    plt.plot(x_lst, y_lst, c='black')

    return merged_points


def findLength(merged_points):
    x0 = merged_points[-1][0]
    y0 = merged_points[-1][1]
    l = 0
    for x1, y1 in merged_points:
        l += np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        x0, y0 = x1, y1
    return l


plt.rcParams.update({'figure.figsize': (6, 6)})
cmap = plt.get_cmap('hsv')

inicialisation()

l = [elem for elem in list(chain(*arr_point)) if elem.f is not None]

repeat(epsilon)

plt.scatter([elem.x for elem in l], [elem.y for elem in l], s=size, cmap=cmap, c=[elem.f for elem in l])

# точки эквипотенциали
find(f)
# упорядочиваем точки и находим длину
l = findLength(sort())
print("Длина заданной эквипотенциали = ", l)

plt.show()
