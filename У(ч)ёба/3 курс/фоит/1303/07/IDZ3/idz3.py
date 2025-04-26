import numpy as np
import matplotlib.pyplot as plt


L1 = 12.3564703021424
L2 = 0.886796702338419
C1 = 0.0000114592238047738
C2 = 0.0000122868559236183
R1 = 113.207017454714
R2 = 39.6366528226263
R3 = 1087.44220519815
R4 = 506.008438524223
dt = 0.0196349540849362
N1 = 8192
t = dt * N1


def imp_1(w):
    return R4 + 1 / (1j * w * C2)


def imp_2(w):
    return 1 / (1j * w * C1) + R2 + 1j * w * L2 + R3


def imp_parall(w):
    return 1 / (1 / imp_1(w) + 1 / imp_2(w))


def I_1(w, Uin):
    return Uin / (R1 + 1j * w * L1 + imp_parall(w))


def U_parall(w, Uin):
    return I_1(w, Uin) * imp_parall(w)


def I_2(w, Uin):
    return U_parall(w, Uin) / imp_1(w)


def U_out(w, Uin):
    return I_2(w, Uin) * R4


def Func(w, Uin):
    return U_out(w, Uin) / Uin

w_values = np.linspace(0, 100, 1000)
plt.plot(w_values, np.abs(Func(w_values, 1)), label='АЧХ')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.legend()
plt.show()


signal = np.loadtxt("C:\\Users\\dns\\Desktop\\Учеба\\3 курс\\5 семестр\\ФОИТ\\7.txt")
time_values = np.arange(0, N1 * dt, dt)
plt.plot(time_values, signal, label='Сигнал')
plt.xlabel('Время')
plt.ylabel('Значение сигнала')
plt.legend()
plt.show()


Fsig = np.fft.fft(signal)
frequency_values = np.fft.fftfreq(N1, dt)
FourAbs = np.abs(Fsig)
plt.plot(2 * np.pi * frequency_values, FourAbs, label='Спектр')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.legend()
plt.show()


freq_3 = 30
print(np.abs(Func(freq_3, 1)))