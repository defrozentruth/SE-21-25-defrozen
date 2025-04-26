import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import random

outer_phi = 0
first_phi = 6
second_phi = -6

target_phi = 1


def outer_electrode_contour(x, y):
    lhs = np.power(x, 2) + np.power(y, 2)
    return lhs - 25


def first_electrode_contour(x, y):
    lhs = 0.3 * np.power(np.abs(1.8 + x), 3) + 0.8 * np.power(np.abs(1.8 + y), 3)
    return lhs - 0.8


def second_electrode_contour(x, y):
    lhs = 0.3 * np.power(np.abs(-1.8 + x), 2) + np.power(np.abs(-1.8 + y), 2)
    return lhs - 0.8


class PointPhi:
    def __init__(self, x, y, phi):
        self.x = x
        self.y = y
        self.phi = phi
        self.is_active = True

    def set_phi(self, phi):
        self.phi = phi
        self.is_active = False


points_per_side = 200
plot_width = 6


def plot_for(func: callable):
    for x in range(points_per_side):
        for y in range(points_per_side):
            func(x, y)


def create_point(x, y):
    return PointPhi(-plot_width + 2 * plot_width * x / points_per_side,
                    -plot_width + 2 * plot_width * y / points_per_side,
                    first_phi + random.random() * (second_phi - first_phi))


# Make random potential distribution on the grid
points = [
    [create_point(x, y) for y in range(points_per_side)]
    for x in range(points_per_side)
]
x_grid_points = np.linspace(-plot_width, plot_width, points_per_side)
y_grid_points = np.linspace(-plot_width, plot_width, points_per_side)

contours_x = []
contours_y = []

outer_ellipsis_width = 0.5
inner_ellipsis_width = 0.1


# draw electrode contours and set potentials
def draw_contours(x, y):
    result = outer_electrode_contour(points[x][y].x, points[x][y].y)
    if np.abs(result) < outer_ellipsis_width:
        contours_x.append(points[x][y].x)
        contours_y.append(points[x][y].y)

    if result >= 0:
        points[x][y].set_phi(outer_phi)
        return

    result = first_electrode_contour(points[x][y].x, points[x][y].y)
    if np.abs(result) < inner_ellipsis_width:
        contours_x.append(points[x][y].x)
        contours_y.append(points[x][y].y)

    if result <= 0:
        points[x][y].set_phi(first_phi)
        return

    result = second_electrode_contour(points[x][y].x, points[x][y].y)
    if np.abs(result) < inner_ellipsis_width:
        contours_x.append(points[x][y].x)
        contours_y.append(points[x][y].y)

    if result <= 0:
        points[x][y].set_phi(second_phi)
        return


# draw_contours()
plot_for(draw_contours)
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.scatter(contours_x, contours_y, c='blue', s=2)

calculation_error = 0.01


# Average potential on the grid until it is precise enough
def recalculate_phi():
    global points

    new_phi = [[0 for _ in range(points_per_side)] for _ in range(points_per_side)]
    is_precise = True

    def average_phi(x, y):
        global points
        nonlocal new_phi
        if points[x][y].is_active:
            new_phi[x][y] = ((points[x + 1][y].phi + points[x][y + 1].phi +
                              points[x - 1][y].phi + points[x][y - 1].phi) / 4)

    def check_precision(x, y):
        global points
        nonlocal is_precise
        if points[x][y].is_active:
            if np.abs(points[x][y].phi - new_phi[x][y]) > calculation_error:
                is_precise = False
            points[x][y].phi = new_phi[x][y]

    plot_for(average_phi)
    plot_for(check_precision)

    return not is_precise


while recalculate_phi():
    ...

x_points = []
y_points = []
colors = []


def color_points(x, y):
    global points, x_points, y_points, colors

    def get_color(phi):
        k = (phi - first_phi) / (second_phi - first_phi)
        return [k, k, k]

    if points[x][y].is_active:
        x_points.append(points[x][y].x)
        y_points.append(points[x][y].y)
        colors.append(get_color(points[x][y].phi))


plot_for(color_points)

plt.scatter(x_points, y_points, c=colors, s=1)


def get_equation_system(a: PointPhi, b: PointPhi, c: PointPhi):
    return [
        f'a + k1 * {a.x} + k2 * {a.y} - {a.phi}',
        f'a + k1 * {b.x} + k2 * {b.y} - {b.phi}',
        f'a + k1 * {c.x} + k2 * {c.y} - {c.phi}'
    ]


def get_length_on_square(lt_point, rt_point, lb_point, rb_point):
    equation_system = []

    def eval_system(variables):
        (a, k1, k2) = variables
        res = []
        for equation in equation_system:
            res.append(eval(equation))
        return res

    line_points = []

    equation_system = get_equation_system(lb_point, lt_point, rt_point)
    (a, k1, k2) = fsolve(eval_system, [1, 1, 1])

    x_t = (target_phi - a - k2 * lt_point.y) / k1
    if lt_point.x < x_t < rt_point.x:
        plt.scatter(x_t, lt_point.y, c='red', s=1)
        line_points.append((x_t, lt_point.y))

    y_l = (target_phi - a - k1 * lt_point.x) / k2
    if lb_point.y < y_l < lt_point.y:
        plt.scatter(lt_point.x, y_l, c='red', s=1)
        line_points.append((lt_point.x, y_l))

    equation_system = get_equation_system(rb_point, lb_point, rt_point)
    (a, k1, k2) = fsolve(eval_system, [1, 1, 1])

    x_b = (target_phi - a - k2 * rb_point.y) / k1
    if lb_point.x < x_b < rb_point.x:
        plt.scatter(x_b, rb_point.y, c='red', s=1)
        line_points.append((x_b, rb_point.y))

    y_r = (target_phi - a - k1 * rb_point.x) / k2
    if rb_point.y < y_r < rt_point.y:
        plt.scatter(rb_point.x, y_r, c='red', s=1)
        line_points.append((rb_point.x, y_r))

    if len(line_points) == 2:
        return np.hypot(
            line_points[0][0] - line_points[1][0],
            line_points[0][1] - line_points[1][1]
        )

    return 0


total_length = 0

phi_error = 0.2


def calculate_length(x, y):
    global total_length, points
    if points[x][y].is_active:
        if np.abs(points[x][y].phi - target_phi) < phi_error:
            p1 = points[x][y]
            p2 = points[x + 1][y]
            p3 = points[x][y - 1]
            p4 = points[x + 1][y - 1]
            total_length += get_length_on_square(p1, p2, p3, p4)


plot_for(calculate_length)

print(total_length)

plt.show()
