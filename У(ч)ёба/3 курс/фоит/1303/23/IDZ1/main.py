import numpy as np
import matplotlib.pyplot as plt

y0=0.3
R=1.2
accurance=R/1000
n2=1
w=3.1 * 10 ** 14
a=22* np.pi / 180
coords=[]
def f1(y):
    return 1.5 + 0.3*np.cos(0.8*y)**3
def Zf(y):
    return 42 + 3*np.sin(17.951958020513104*y)
def n(y, w):
    return f1(y) * (1 - ((0.35 * 10 ** 14) / w) ** 2)
def graphic(result):
    plt.plot([0, 45], [R, R], "lime")
    plt.plot([0, 45], [-R, -R], "lime")
    plt.plot([0, 0], [-R, R], "lime")
    exit = np.arange(-R, R, accurance)
    plt.plot(Zf(exit), exit, "lime")
    plt.plot(*zip(*result[0]), color='red')
    plt.show()
def waveLength():
    distance = 0

    nB = n(y0,w)
    nA = nB

    y = y0
    z = 0
    coords.append((z, y))

    angle = np.sin(np.pi/2 - np.arcsin((np.sin(a)*n2)/n(y0, w)))
    direction = 1

    while z <= Zf(y):
        y += accurance * np.sqrt(1 - angle ** 2) * direction
        z += accurance * angle
        nB = n(y, w)

        if abs(y) >= R:
            nB = n2

        if (nA * angle) / nB > 1:
            direction *= -1
        else:
            angle=(nA * angle) / nB

        nA = nB
        distance += accurance
        coords.append((z, y))

    return coords, distance


result=waveLength()
print(result[1])
graphic(result)




