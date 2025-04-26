import numpy as np
import matplotlib.pyplot as plt


# Constants
def alpha():
    return np.deg2rad(22)


def y0():
    return 0.3


def omega():
    return 3.3 * 10 ** 14


def n2():
    return 1


def R():
    return 0.6


def dR():
    return 0.0001


# Functions
def f1(y):
    return 1.2 + 0.3 * np.cos(0.8 * y) ** 3


def Zf(y):
    return 42 + 3 * np.sin(17.951958020513104 * y)


def n1(y, om=omega()):
    return f1(y) * (1 - ((0.35 * 10 ** 14) / om) ** 2)


def findYZ(y, z, sinAngle, direction):
    y += dR() * np.sqrt(1 - sinAngle ** 2) * direction
    z += dR() * sinAngle
    return y, z


def main():
    arrayZ = [0]
    arrayY = [y0()]
    trajectoryLen = 0

    currentN = n2()
    nextN = n1(y0())
    currentY = y0()
    currentZ = 0

    currentAlpha = alpha()
    sinAlpha = np.sin(np.pi / 2 - np.arcsin((np.sin(currentAlpha) * currentN) / nextN))
    verticalDirection = 1
    currentN = nextN
    while currentZ <= Zf(currentY):
        currentY, currentZ = findYZ(currentY, currentZ, sinAlpha, verticalDirection)

        nextN = n1(currentY)
        if abs(currentY) >= R():
            nextN = n2()

        sinBeta = (currentN * sinAlpha) / nextN

        if sinBeta >= 1:
            verticalDirection *= -1
            sinBeta = sinAlpha

        currentN, sinAlpha = nextN, sinBeta
        trajectoryLen += dR()
        arrayZ.append(currentZ)
        arrayY.append(currentY)
    print(trajectoryLen)

    plt.plot([0, 45], [R(), R()], "lime")
    plt.plot([0, 45], [-R(), -R()], "lime")
    plt.plot([0, 0], [-R(), R()], "lime")
    exitArrayY = np.arange(-R(), R(), 0.0001)
    plt.plot(Zf(exitArrayY), exitArrayY, "lime")
    plt.plot(arrayZ, arrayY, 'red')
    plt.show()


if __name__ == '__main__':
    main()
