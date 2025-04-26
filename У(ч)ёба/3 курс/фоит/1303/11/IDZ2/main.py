import random
import numpy as np
import copy
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y, f):
        self.x = x
        self.y = y
        self.f = f


def is_in_constraints(a, b):
    constraint_circle = a ** 2 + b ** 2 <= 25
    constraint_1 = abs(1.5 + a) ** 3.5 + 0.3 * abs(b) ** 3.5 >= 0.8
    constraint_2 = abs(-1.5 + a) ** 1.5 + 0.3 * abs(b) ** 1.5 >= 0.8
    return constraint_circle and constraint_1 and constraint_2


def initialize_points():
    for x in partition:
        inner_list = []
        for y in partition:
            f = None
            if is_in_constraints(x, y):
                circle_constraint = abs(x ** 2 + y ** 2 - 25)
                constraint_1 = abs(abs(1.5 + x) ** 3.5 + 0.3 * abs(y) ** 3.5 - 0.8)
                constraint_2 = abs(abs(-1.5 + x) ** 1.5 + 0.3 * abs(y) ** 1.5 - 0.8)

                if circle_constraint <= 1:
                    f = 0
                elif constraint_1 <= 0.5:
                    f = f1
                elif constraint_2 <= 0.5:
                    f = f2
                else:
                    f = random.uniform(min(f1, f2), max(f1, f2))

            point = Point(x, y, f)
            inner_list.append(point)
        arr_point.append(inner_list)


def perform_iteration():
    n = 0
    while (n <= 500):
        for y in range(1, len(arr_point) - 1):
            for x in range(1, len(arr_point[y]) - 1):
                neighbors = [
                    arr_point[y][x - 1].f,
                    arr_point[y][x + 1].f,
                    arr_point[y - 1][x].f,
                    arr_point[y + 1][x].f
                ]
                no_none_found = True
                for neighbor in neighbors:
                    if neighbor is None:
                        no_none_found = False
                        break
                if not no_none_found:
                    continue
                arr_point[y][x].f = sum(neighbors) / 4
        n += 1


def calculate_point(tmp, neighbor, flag):
    if flag == 'x':
        new_x = tmp.x + (abs(f - tmp.f) / abs(tmp.f - neighbor.f)) * step
        new_y = tmp.y
    else:
        new_x = tmp.x
        new_y = tmp.y + (abs(f - tmp.f) / abs(tmp.f - neighbor.f)) * step
    arr_x.append(new_x)
    arr_y.append(new_y)


def process_equi_potential(f_value):
    for i in range(1, len(arr_point) - 1):
        for j in range(1, len(arr_point[i]) - 1):
            current = arr_point[i][j]
            right_neighbor = arr_point[i + 1][j]
            down_neighbor = arr_point[i][j + 1]
            if (current.f is None or right_neighbor.f is None or down_neighbor.f is None):
                continue
            if (current.f <= f_value <= right_neighbor.f or current.f >= f_value >= right_neighbor.f):
                calculate_point(current, right_neighbor, 'x')

            if (current.f <= f_value <= down_neighbor.f or current.f >= f_value >= down_neighbor.f):
                calculate_point(current, down_neighbor, 'y')


def result_points():
    points = [(x, y) for x, y in zip(arr_x, arr_y)]
    sorted_points = sorted(points, key=lambda lst: lst[0])
    left_point = sorted_points[0]
    right_point = sorted_points[-1]
    x1, y1 = left_point
    x2, y2 = right_point

    slope = (y2 - y1) / (x2 - x1)

    below_border = [(x1, y1)]
    above_border = [(x2, y2)]

    for x, y in points:
        border = slope * (x - x1) + y1
        if y < border:
            below_border.append((x, y))
        elif y > border:
            above_border.append((x, y))

    below_border.sort()
    above_border.sort(reverse=True)

    above_border.append((x1, y1))

    result_points = below_border + above_border

    x_values, y_values = zip(*result_points)

    plt.plot(x_values, y_values, c='green')

    return result_points


def find_length(result_points):
    length = 0
    for i in range(1, len(result_points)):
        x0, y0 = result_points[i - 1]
        x1, y1 = result_points[i]
        length += np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    return length


f1 = -6
f2 = 6
f = 3
step = 0.1
arr_x = []
arr_y = []
arr_point = []
partition = np.arange(f1, f2 + step, step)

plt.gca().set_aspect('equal')

initialize_points()

perform_iteration()

list = []
for row in arr_point:
    for el in row:
        if el.f is not None:
            list.append(el)

plt.scatter([el.x for el in list], [el.y for el in list], c='yellow')

process_equi_potential(f)

length = find_length(result_points())

print(f"Искомая длина: {length}")

plt.show()
