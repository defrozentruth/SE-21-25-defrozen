import matplotlib
matplotlib.use('TkAgg')
import random
import numpy as np
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y, f):
        self.x = x
        self.y = y
        self.f = f


class EquiPotentialCalculator:
    def __init__(self, f1, f2, f, step):
        self.f1 = f1
        self.f2 = f2
        self.f = f
        self.step = step
        self.arr_x = []
        self.arr_y = []
        self.arr_point = []
        self.partition = np.arange(-5, 5, step)

    def areInConstraints(self, x, y):
        res = x ** 2 + y ** 2 <= 25
        res1 = abs(1.5 + x) ** 1.5 + abs(-1.5 + y) ** 1.5 >= 0.6
        res2 = abs(-1.5 + x) ** 3 + 0.8 * abs(1.5 + y) ** 3 >= 0.5
        return res and res1 and res2

    def initializePoints(self):
        for x in self.partition:
            innerList = []
            for y in self.partition:
                f = None
                if self.areInConstraints(x, y):
                    circleConstraint = abs(x ** 2 + y ** 2 - 25)
                    constraint1 = abs(abs(1.5 + x) ** 1.5 + abs(-1.5 + y) ** 1.5 - 0.6)
                    constraint2 = abs(abs(1.5 + x) ** 1.5 + abs(-1.5 + y) ** 1.5 - 0.5)

                    if circleConstraint <= 1:
                        f = 0
                    elif constraint1 <= 0.5:
                        f = self.f1
                    elif constraint2 <= 0.5:
                        f = self.f2
                    else:
                        f = random.uniform(min(self.f1, self.f2), max(self.f1, self.f2))

                point = Point(x, y, f)
                innerList.append(point)
            self.arr_point.append(innerList)

    def iteratePoints(self):
        n = 0
        while n <= 500:
            for y in range(1, len(self.arr_point) - 1):
                for x in range(1, len(self.arr_point[y]) - 1):
                    neighbors = [
                        self.arr_point[y][x - 1].f,
                        self.arr_point[y][x + 1].f,
                        self.arr_point[y - 1][x].f,
                        self.arr_point[y + 1][x].f
                    ]
                    noNoneFound = all(neighbor is not None for neighbor in neighbors)
                    if not noNoneFound:
                        continue
                    self.arr_point[y][x].f = sum(neighbors) / 4
            n += 1

    def calculateNewPoint(self, tmp, neighbor, flag):
        if flag == 'x':
            new_x = tmp.x + (abs(self.f - tmp.f) / abs(tmp.f - neighbor.f)) * self.step
            new_y = tmp.y
        else:
            new_x = tmp.x
            new_y = tmp.y + (abs(self.f - tmp.f) / abs(tmp.f - neighbor.f)) * self.step
        self.arr_x.append(new_x)
        self.arr_y.append(new_y)

    def processPotentialEquilibrium(self, fValue):
        for i in range(1, len(self.arr_point) - 1):
            for j in range(1, len(self.arr_point[i]) - 1):
                current = self.arr_point[i][j]
                rightNeighbor = self.arr_point[i + 1][j]
                downNeighbor = self.arr_point[i][j + 1]
                if (current.f is None or rightNeighbor.f is None or downNeighbor.f is None):
                    continue
                if (current.f <= fValue <= rightNeighbor.f or current.f >= fValue >= rightNeighbor.f):
                    self.calculateNewPoint(current, rightNeighbor, 'x')

                if (current.f <= fValue <= downNeighbor.f or current.f >= fValue >= downNeighbor.f):
                    self.calculateNewPoint(current, downNeighbor, 'y')

    def getResultingPoints(self):
        points = [(x, y) for x, y in zip(self.arr_x, self.arr_y)]
        sortedPoints = sorted(points, key=lambda lst: lst[0])
        leftPoint = sortedPoints[0]
        rightPoint = sortedPoints[-1]
        x1, y1 = leftPoint
        x2, y2 = rightPoint

        slope = (y2 - y1) / (x2 - x1)

        belowBorder = [(x1, y1)]
        aboveBorder = [(x2, y2)]

        for x, y in points:
            border = slope * (x - x1) + y1
            if y < border:
                belowBorder.append((x, y))
            elif y > border:
                aboveBorder.append((x, y))

        belowBorder.sort()
        aboveBorder.sort(reverse=True)

        aboveBorder.append((x1, y1))

        resultPoints = belowBorder + aboveBorder

        xValues, yValues = zip(*resultPoints)

        plt.plot(xValues, yValues, c='red')

        return resultPoints

    def calculateLength(self, resultPoints):
        length = 0
        for i in range(1, len(resultPoints)):
            x0, y0 = resultPoints[i - 1]
            x1, y1 = resultPoints[i]
            length += np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        return length

    def performPotentialEquilibrium(self):
        self.initializePoints()
        self.iteratePoints()

        arrList = []
        for row in self.arr_point:
            for el in row:
                if el.f is not None:
                    arrList.append(el)

        plt.scatter([el.x for el in arrList], [el.y for el in arrList], c='blue')

        self.processPotentialEquilibrium(self.f)

        length = self.calculateLength(self.getResultingPoints())

        print(f"Desired length: {length}")
        plt.show()


if __name__ == "__main__":
    calculator = EquiPotentialCalculator(f1=5, f2=5, f=4, step=0.1)
    calculator.performPotentialEquilibrium()
