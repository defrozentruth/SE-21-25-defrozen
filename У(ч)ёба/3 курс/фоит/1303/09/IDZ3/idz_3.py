import numpy as np
import scipy
import sympy
import matplotlib.pyplot as plt

L1 = 13.2223794108314
L2 = 0.812031426330705
C1 = 1.06055586901015E-05
C2 = 1.27316440410797E-05
R1 = 119.968082966626
R2 = 38.9142489347643
R3 = 1043.6179421621
R4 = 507.618413286267
N = 8192
dt = 0.0196349540849362
k = 4

file = open('9.txt', 'r')
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

y = [abs(elem) for elem in F]
x = [i * 2 * np.pi / (N * dt) for i in range(N)]

newY = []
newX = []

for i in range(N):
    if abs(y[i]) > 1e-10:
        newY.append(2 * y[i] / F.size)
        newX.append(x[i])

newX = newX[:int(len(newX) / 2)]
newY = newY[:int(len(newY) / 2)]

print(abs(H.subs(omega, newX[3])))
plt.scatter(newX, newY)
plt.show()

steps = [dt * i for i in range(N)]
plt.plot(steps, signal)
plt.show()

sympy.plotting.plot(abs(H), (omega, 0, 100))
