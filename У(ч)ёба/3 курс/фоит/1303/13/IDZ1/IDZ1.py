import numpy as np
import matplotlib.pyplot as plt

R = 0.8
n2 = 1
w = 3.5 * 10 ** 14
y0 = 0.1
a = np.radians(20)
delta = 1 / 1000


def f1(y):
    return 1.4 - 0.14 * y ** 4


def Zf(y):
    return 28 + 3 * np.sin(17.951958020513104 * y)


def n1(y, w):
    return f1(y) * (1 - ((0.35 * 10 ** 14) / w) ** 2)


Z = []
Y = []
result = 0
y = y0
z = 0
Z.append(z)
Y.append(y)
next = n1(y0, w)
curr = next
angle = np.sin(np.pi / 2 - np.arcsin((np.sin(a) * n2) / n1(y0, w)))
forw = 1
result = 0
while z <= Zf(y):
    y += delta * np.sqrt(1 - angle ** 2) * forw
    z += delta * angle
    Z.append(z)
    Y.append(y)
    next = n1(y, w)
    if abs(y) >= R:
        nB = n2
    if (curr * angle) / next > 1:
        forw *= -1
    else:
        angle = (curr * angle) / next
    curr = next
    result += delta

print(result)

plt.plot([0, 45], [R, R], "blue")
plt.plot([0, 45], [-R, -R], "blue")
plt.plot([0, 0], [-R, R], "blue")
Y_arr = np.arange(-R, R, delta)
plt.plot(Zf(Y_arr), Y_arr, "blue")
plt.plot(Z, Y, color='red')
plt.show()
