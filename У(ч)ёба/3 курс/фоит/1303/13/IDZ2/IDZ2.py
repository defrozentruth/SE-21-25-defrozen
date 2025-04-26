import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import random

e0 = 0
e1 = -5
e2 = 6
e_find = 1
eps = 0.001
X = []
Y = []
num_points = 200
R = 6

def electrod0(x, y):
    return pow(x, 2) + pow(y, 2) - 25


def electrod1(x, y):
    return 0.5*np.abs(-1.8 + x)**1.5 + np.abs(y)**1.5 - 0.6



def electrod2(x, y):
    return 0.3*np.abs(1.8 + x)**3.5 + 0.3*np.abs(y)**3.5 - 0.7


class Point:
    def __init__(self, x, y, V):
        self.x = x
        self.y = y
        self.V = V
        self.take = True


points = [[Point(-R + 2 * R * x / num_points,
                  -R + 2 * R * y / num_points,
                  e1 + random.random() * (e2 - e1)) for y in range(num_points)] for x in
          range(num_points)]

# marking edges
for x in range(num_points):
    for y in range(num_points):

        res = electrod0(points[x][y].x, points[x][y].y)
        if (res > 0 - 0.5 and res < 0 + 0.5):
            X.append(points[x][y].x)
            Y.append(points[x][y].y)

        if res >= 0:
            points[x][y].V = e0
            points[x][y].take = False
            continue

        res = electrod1(points[x][y].x, points[x][y].y)
        if (res > 0 - 0.1 and res < 0 + 0.1):
            X.append(points[x][y].x)
            Y.append(points[x][y].y)

        if res <= 0:
            points[x][y].V = e1
            points[x][y].take = False
            continue

        res = electrod2(points[x][y].x, points[x][y].y)
        if (res > 0 - 0.1 and res < 0 + 0.1):
            X.append(points[x][y].x)
            Y.append(points[x][y].y)

        if res <= 0:
            points[x][y].V = e2
            points[x][y].take = False
            continue

def iter():
    V_new = [[0 for y in range(num_points)] for x in range(num_points)]

    for x in range(num_points):
        for y in range(num_points):
            if (points[x][y].take):
                V_new[x][y] = (points[x + 1][y].V +
                              points[x][y + 1].V +
                              points[x - 1][y].V +
                              points[x][y - 1].V) / 4

    isLastIteration = True
    for x in range(num_points):
        for y in range(num_points):
            if points[x][y].take:
                if np.abs(points[x][y].V - V_new[x][y]) > eps:
                    isLastIteration = False
                points[x][y].V = V_new[x][y]

    if not isLastIteration:
        return True
    else:
        return False


flag = True
while (flag):
    flag = iter()


eq_list = []

def f(variables):
    (a, k1, k2) = variables
    res = []
    for eq in eq_list:
        res.append(eval(eq))
    return res

def create_eq(L):
    return f"a + k1 * {L.x} + k2 * {L.y} - {L.V}"

def findlength(L1, R1, L2, R2):
    global eq_list

    points = []

    eq_list = [create_eq(L1), create_eq(R1), create_eq(L2)]
    (a, k1, k2) = fsolve(f, [1, 1, 1])

    xT = (e_find - a - k2 * L1.y) / k1
    if (xT > L1.x and xT < R1.x):
        plt.scatter(xT, L1.y, c='red', s=1)
        points.append((xT, L1.y))

    yL = (e_find - a - k1 * L1.x) / k2
    if (yL > L2.y and yL < L1.y):
        plt.scatter(L1.x, yL, c='red', s=1)
        points.append((L1.x, yL))

    eq_list = [create_eq(R2), create_eq(R1), create_eq(L2)]

    (a, k1, k2) = fsolve(f, [1, 1, 1])

    xB = (e_find - a - k2 * R2.y) / k1
    if (xB > L2.x and xB < R2.x):
        plt.scatter(xB, R2.y, c='red', s=1)
        points.append((xB, R2.y))

    yR = (e_find - a - k1 * R2.x) / k2
    if (yR > R2.y and yR < R1.y):
        plt.scatter(R2.x, yR, c='red', s=1)
        points.append((R2.x, yR))
    if (len(points) == 2):
        return np.sqrt(pow(np.abs(points[0][0] - points[1][0]), 2) + pow(np.abs(points[0][1] - points[1][1]), 2))

    return 0


totalLength = 0

for x in range(num_points):
    for y in range(num_points):
        if (points[x][y].take):
            if (points[x][y].V < e_find + 0.5 and
                    points[x][y].V > e_find - 0.5):
                totalLength += findlength(points[x][y],
                                                 points[x + 1][y],
                                                 points[x][y - 1],
                                                 points[x + 1][y - 1])

print(totalLength)

x_range = np.linspace(-5, 5, 400)
y_range = np.linspace(-5, 5, 400)
X, Y = np.meshgrid(x_range, y_range)

external_electrode_values = electrod0(X, Y)
electrode1_values = electrod1(X, Y)
electrode2_values = electrod2(X, Y)

plt.contour(X, Y, external_electrode_values, levels=[0], colors='b')
plt.contour(X, Y, electrode1_values, levels=[0], colors='g')
plt.contour(X, Y, electrode2_values, levels=[0], colors='g')

plt.title('Contour Plots of Electrodes')
plt.axis('equal')
plt.grid(True)
plt.show()