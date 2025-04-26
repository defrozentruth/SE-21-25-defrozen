import matplotlib.pyplot as plt
import random
import numpy as np
from itertools import chain

class Point:
    def __init__(self, x, y, f):
        self.x = x
        self.y = y
        self.f = f

def isIn(x,y):
    res = x ** 2 + y ** 2 <= 25
    res1 = 0.3 * abs(-1.8 + x) ** 3 + 0.8 * abs(-1.8 + y) ** 3 >= 0.6
    res2 = 0.3 * abs(1.8+x) ** 3.5 + 0.8 * abs(1.8 + y) ** 3.5 >= 0.5
    return res and res1 and res2

F1 = -6
F2 = -5
f = -1
step = 0.1
start = -6
finish = 6
size = 10
epsilon = 0.00001
t1 = np.arange(start, finish, step)

xArr = []
yArr = []
arr_point = []

def init():
    for x in t1:
        arr_point.append([])
        for y in t1:
            if isIn(x, y):
                if(abs(x ** 2 + y ** 2 - 25) <= 1):
                    f = 0
                elif(abs(0.3 * abs(-1.8 + x) ** 3 + 0.8 * abs(-1.8 + y) ** 3 - 0.6) <= 0.3):
                    f = F1
                elif(abs(0.3 * abs(1.8 + x) ** 3.5 + 0.8 * abs(1.8 + y) ** 3.5 - 0.5) <= 0.2):
                    f = F2
                else:
                    f = random.random()* (abs(F1) + abs(F2)) + min(F1, F2)
            else:
                f = None
            point = Point(x, y, f)
            arr_point[-1].append(point)

def iteration():
    max_delta = 0
    for y in range(1, len(arr_point)-2):
        for x in range(1, len(arr_point[y])-2):
            neighboors = [arr_point[y][x-1].f,
                          arr_point[y][x+1].f,
                          arr_point[y-1][x].f,
                          arr_point[y+1][x].f]
            if(any(potent is None for potent in neighboors)):
                continue
            delta = max(neighboors) - min(neighboors)
            if (delta > max_delta):
                max_delta = delta
            arr_point[y][x].f = sum(neighboors)/4
    return max_delta

def repeat(epsilon):
    previous_delta = abs(F1) + abs(F2) + 10
    n = 0
    while(True):
        n += 1
        new_delta = iteration()
        if(abs(previous_delta - new_delta) < epsilon ):
            break
        previous_delta = new_delta

def add(point1, point2):
    xArr.append(point1.x)
    xArr.append(point2.x)
    yArr.append(point1.y)
    yArr.append(point2.y)

def findPoint(tmp, neighboor, flag):
    diapason = abs(tmp.f - neighboor.f)
    if (diapason == 0):
        add(tmp, neighboor)
        return True
    s = abs(f - tmp.f)
    if(flag=='x'):
        xArr.append(tmp.x + (s / diapason) * step)
        yArr.append(tmp.y)
    else:
        xArr.append(tmp.x)
        yArr.append(tmp.y +(s/diapason)*step)
    return False

def find(f):
    for i in range(1, len(arr_point)-2):
        for j in range(1, len(arr_point[i])-2):
            tmp = arr_point[i][j]
            right = arr_point[i+1][j]
            down = arr_point[i][j+1]
            if(tmp.f is None or right.f is None or down.f is None):
                continue
            if(tmp.f <= f <= right.f or tmp.f >= f >= right.f):
                findPoint(tmp, right, 'x')

            if(tmp.f <= f <= down.f or tmp.f >= f >= down.f):
                findPoint(tmp, down, 'y')

def sort():
    points = list(zip(xArr, yArr))
    leftmost_point, *_, rightmost_point = sorted(points, key=lambda lst: lst[0])
    x1, y1 = leftmost_point
    x2, y2 = rightmost_point

    border_slope = (y2 - y1) / (x2 - x1)

    points_below = [(x1, y1)]
    points_above = [(x2, y2)]

    for x, y in points:
        border = border_slope * (x - x1) + y1
        if y < border:
            points_below.append((x, y))
        elif y > border:
            points_above.append((x, y))

    points_below.sort()
    points_above.sort(reverse=True)

    points_above.append((x1, y1))

    merged_points = points_below + points_above

    x_lst = [x for x, _ in merged_points]
    y_lst = [y for _, y in merged_points]
    plt.plot(x_lst, y_lst, c='black')

    return merged_points

def findLength(merged_points):
    x0 = merged_points[-1][0]
    y0 = merged_points[-1][1]
    l = 0
    for x1, y1 in merged_points:
        l += np.sqrt((x1 - x0)**2 + (y1 - y0)**2)
        x0, y0 = x1, y1
    return l

plt.rcParams.update({'figure.figsize': (6,6)})
cmap = plt.get_cmap('hsv')

init()

l = [elem for elem in list(chain(*arr_point)) if elem.f is not None]

repeat(epsilon) 

plt.scatter([elem.x for elem in l], [elem.y for elem in l], s=size, cmap=cmap, c=[elem.f for elem in l])

find(f)
l = findLength(sort()) 
print("Длина эквипотенциали = ", l)
print("Количество точек", len(xArr))

plt.show()
