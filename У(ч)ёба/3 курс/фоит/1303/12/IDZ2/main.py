import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
p_find = 4
p1 = -6
p2 = 5
eps = 0.1


def electrode_ext(x, y):
    return x**2 + y**2 - 25


def electrode1(x, y):
    return abs(1.8 + x)**3 + 0.8 * abs(y)**3 - 0.5


def electrode2(x, y):
    return 0.5 * abs(-1.8 + x)**2 + abs(y)**2 - 0.5


def makeElectrode():
    x = np.linspace(-5, 5, 400)
    y = np.linspace(-5, 5, 400)
    X, Y = np.meshgrid(x, y)

    coords1 = electrode1(X, Y)
    coords2 = electrode2(X, Y)
    coords_ext = electrode_ext(X, Y)
    plt.contour(X, Y, coords1, levels=[0], colors='red')
    plt.contour(X, Y, coords2, levels=[0], colors='red')
    plt.contour(X, Y, coords_ext, levels=[0], colors='blue')


def findPos(x, y):
    if -5 * accuracy <= electrode_ext(x, y) <= 0:
        return 0  # на внешнем электроде
    if electrode_ext(x, y) > 0:
        return -2  # вне области
    if electrode1(x, y) <= 0:
        return 1  # 1 электрод
    if electrode2(x, y) <= 0:
        return 2  # 2 электрод
    else:
        return -1  # внешний электрода


def makeStartValues():
    for height in range(0, countLines):
        grid[height] = []
        for width in range(0, countLines):
            grid[height].append(None)
            x = -5 + width * accuracy
            y = -5 + height * accuracy
            position = findPos(x, y)
            if position != -1:
                if position == 0:
                    grid[height][width] = 0
                elif position == 1:
                    grid[height][width] = p1
                elif position == 2:
                    grid[height][width] = p2
            elif position == -1:
                influence = randint(1, 10) / 10
                grid[height][width] = (
                    (0 + influence * p1 + (1 - influence) * p2)) / 3


def getColor(value):
    if value >= 0:
        green = int(value * 255 / 5)
        color_hex = "#{:02x}{:02x}{:02x}".format(0, green, 0)
    else:
        red = int(abs(value) * 255 / 6)
        color_hex = "#{:02x}{:02x}{:02x}".format(red, 0, 0)
    return color_hex


def makeGrid():
    for height in range(0, countLines):
        for width in range(0, countLines):
            x = -5 + width * accuracy
            y = -5 + height * accuracy
            if grid[height][width] is not None:
                plt.scatter(x, y, color=getColor(grid[height][width]), s=3)
            else:
                plt.scatter(x, y, color="white", s=3)


def setPotentialValues(quantity=1000):
    for i in range(quantity):
        for height in range(1, countLines - 1):
            for width in range(1, countLines - 1):
                x = -5 + width * accuracy
                y = -5 + height * accuracy
                if findPos(x, y) == -1:
                    neighbours = [
                        grid[height-1][width],
                        grid[height+1][width],
                        grid[height][width-1],
                        grid[height][width+1]
                    ]
                    neighbours = [_ for _ in neighbours if _ is not None]

                    grid[height][width] = sum(neighbours) / len(neighbours)


def coordPythagoras(x1, x2, y1, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5


def calculateLen(traceX, traceY):
    res = 0
    for i in range(len(traceX) - 1):
        res += coordPythagoras(traceX[i], traceX[i+1],
                               traceY[i], traceY[i+1])
    return res


def drawPotentialLine():
    traceX = []
    traceY = []
    for width in range(0, countLines):
        for height in range(0, countLines):
            x = -5 + width * accuracy
            y = -5 + height * accuracy
            if (grid[height][width] is not None) and abs(grid[height][width] - p_find) <= eps:
                traceX.append(x)
                traceY.append(y)
                plt.scatter(x, y, color='blue', s=3)

    traceY_pos = []
    traceX_pos = []
    traceY_neg = []
    traceX_neg = []
    for i in range(len(traceX)):
        if traceY[i] < 0:
            traceX_neg.append(traceX[i])
            traceY_neg.append(traceY[i])
        else:
            traceX_pos.append(traceX[i])
            traceY_pos.append(traceY[i])
    temp = list(zip(traceX_neg, traceY_neg))
    temp.sort()
    traceX_neg, traceY_neg = zip(*temp)
    temp = list(zip(traceX_pos, traceY_pos))
    temp.sort()
    traceX_pos, traceY_pos = zip(*temp)
    length = calculateLen(traceX_pos, traceY_pos) + \
        calculateLen(traceX_neg, traceY_neg) + coordPythagoras(
        traceX_neg[0], traceX_pos[0], traceY_neg[0], traceY_pos[0]) + coordPythagoras(traceX_neg[-1], traceX_pos[-1], traceY_neg[-1], traceY_pos[-1])
    print(length)
    plt.plot(traceX_pos, traceY_pos, color='yellow')
    plt.plot(traceX_neg, traceY_neg, color='yellow')
    plt.plot([traceX_neg[0], traceX_pos[0]], [
             traceY_neg[0], traceY_pos[0]], color='yellow')
    plt.plot([traceX_neg[-1], traceX_pos[-1]],
             [traceY_neg[-1], traceY_pos[-1]], color='yellow')


makeElectrode()
accuracy = 0.1
graph_size = 10
countLines = int(graph_size / accuracy)
grid = [0] * countLines
makeStartValues()
setPotentialValues()
makeGrid()
drawPotentialLine()
plt.axis('equal')
plt.grid(False)
plt.show()
