import matplotlib.pyplot as plt
import random
import numpy as np


class Point:
    def __init__(self, x, y, f):
        self.x = x
        self.y = y
        self.f = f


F1 = -5
F2 = 5
f = -4
step = 0.1
arrStart = np.arange(F1, F2 + 1, step)
arr_x = []
arr_y = []
arr_point = []


def isIn(x, y):
    res1 = x ** 2 + y ** 2 <= 25
    res2 = 0.8 * abs(-1.5 + x) ** 2.5 + 0.8 * abs(y) ** 2.5 >= 0.7
    res3 = abs(1.5 + x) ** 1.5 + abs(y) ** 1.5 >= 0.8
    return res1 and res2 and res3


def init():
    for x in arrStart:
        arr_point.append([])
        for y in arrStart:
            if isIn(x, y):
                if (abs(x ** 2 + y ** 2 - 25) <= 1):
                    f = 0
                elif (abs(0.8 * abs(-1.5 + x) ** 2.5 + 0.8 * abs(y) ** 2.5 - 0.7) <= 0.4):
                    f = F1
                elif (abs(abs(1.5 + x) ** 1.5 + abs(y) ** 1.5 - 0.8) <= 0.4):
                    f = F2
                else:
                    f = random.uniform(min(F1, F2), max(F1, F2))
            else:
                f = None
            point = Point(x, y, f)
            arr_point[-1].append(point)


def iteration():
    n = 0
    while (n <= 500):
        for y in range(1, len(arr_point) - 1):
            for x in range(1, len(arr_point[y]) - 1):
                neighboors = [arr_point[y][x - 1].f,
                              arr_point[y][x + 1].f,
                              arr_point[y - 1][x].f,
                              arr_point[y + 1][x].f]
                if (any(potent is None for potent in neighboors)):
                    continue
                arr_point[y][x].f = sum(neighboors) / 4
        n += 1


def findPoint(tmp, neighboor, flag):
    diapason = abs(tmp.f - neighboor.f)
    s = abs(f - tmp.f)
    if (flag == 'horisontal'):
        arr_x.append(tmp.x + (s / diapason) * step)
        arr_y.append(tmp.y)
    else:
        arr_x.append(tmp.x)
        arr_y.append(tmp.y + (s / diapason) * step)


def find(f):
    for i in range(1, len(arr_point) - 2):
        for j in range(1, len(arr_point[i]) - 2):
            tmp = arr_point[i][j]
            right = arr_point[i + 1][j]
            down = arr_point[i][j + 1]
            if (tmp.f is None or right.f is None or down.f is None):
                continue
            if (tmp.f <= f <= right.f or tmp.f >= f >= right.f):
                findPoint(tmp, right, 'horisontal')
            if (tmp.f <= f <= down.f or tmp.f >= f >= down.f):
                findPoint(tmp, down, 'vertical')


def sort():
    points = list(zip(arr_x, arr_y))
    leftmost_point, *_, rightmost_point = sorted(points, key=lambda lst: lst[0])
    x1, y1 = leftmost_point
    x2, y2 = rightmost_point
    tan = (y2 - y1) / (x2 - x1)

    points_below = [(x1, y1)]
    points_above = [(x2, y2)]

    for x, y in points:
        border = tan * (x - x1) + y1
        if y < border:
            points_below.append((x, y))
        elif y > border:
            points_above.append((x, y))

    points_below.sort()
    points_above.sort(reverse=True)

    points_above.append((x1, y1))

    correct_points = points_below + points_above

    x_lst = [x for x, _ in correct_points]
    y_lst = [y for _, y in correct_points]
    plt.plot(x_lst, y_lst, c='black')

    return correct_points


def findLength(merged_points):
    x0 = merged_points[-1][0]
    y0 = merged_points[-1][1]
    l = 0
    for x1, y1 in merged_points:
        l += np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        x0, y0 = x1, y1
    return l


init()
iteration()
arr = []
for sublist in arr_point:
    for elem in sublist:
        if elem.f is not None:
            arr.append(elem)
plt.rcParams.update({'figure.figsize': (6, 6)})
plt.scatter([elem.x for elem in arr], [elem.y for elem in arr])

find(f)
pointsArr = sort()
lenLine = findLength(pointsArr)
print("Длина = ", lenLine)

plt.show()
