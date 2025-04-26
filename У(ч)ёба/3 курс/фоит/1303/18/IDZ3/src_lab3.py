import numpy as np
import scipy
import sympy
import matplotlib.pyplot as plt

L1 = 13.5918808040161
L2 = 0.792438656142625
C1 = 1.17102061840227E-05
C2 = 1.27285942843008E-05
R1 = 104.236702705245
R2 = 33.3716048275039
R3 = 1014.67452335933
R4 = 500.799783087408
N = 8192
deltat = 0.0196349540849362
k = 3

file = open('18.txt', 'r')
signal = []
for num in file:
    signal.append(float(num))

omega = sympy.Symbol("omega")
Uin = sympy.Symbol("Uin")


def ZL(L):
    return 1j * omega * L


def ZC(C):
    return 1 / (1j * omega * C)


Z4_8_right = R4 + ZC(C2)
Z4_8_left = ZC(C1) + R2 + ZL(L2) + R3
Z1_4 = R1 + ZL(L1)
Zpar = (Z4_8_left * Z4_8_right) / (Z4_8_left + Z4_8_right)
Iall = Uin / (Z1_4 + Zpar)
Upar = Iall * Zpar
Ileft = Upar / Z4_8_left
Uout = R3 * Ileft

H = Uout / Uin

F = scipy.fft.fft(np.array(signal))

y = [abs(ele) for ele in F]
x = [i * 2 * np.pi / (N * deltat) for i in range(N)]

newY = []
newX = []

for i in range(N):
    if (abs(y[i]) > 1e-10):
        newY.append(2 * y[i] / F.size)
        newX.append(x[i])

newX = newX[:int(len(newX) / 2)]
newY = newY[:int(len(newY) / 2)]

print(abs(H.subs(omega, newX[3])))

plt.scatter(newX, newY)
plt.show()

steps = [deltat * i for i in range(N)]
plt.plot(steps, signal)
plt.show()

sympy.plotting.plot(abs(H), (omega, 0, 100))