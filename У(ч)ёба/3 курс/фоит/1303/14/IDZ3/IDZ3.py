import numpy as np
import matplotlib.pyplot as plt
np.seterr(divide='ignore', invalid='ignore')


L1 = 12.7437585749938
L2 = 0.768930230614144
C1 = 0.0000111330553238954
C2 = 0.0000109818301332892
R1 = 109.407373881698
R2 = 35.8893596610776
R3 = 1026.58639003326
R4 = 535.393344721292
dt = 0.0196349540849362
N1 = 8192
t = dt * N1

W1 = 5

def imp1(w):
    return R4 + 1 / (1j * w * C2)


def imp2(w):
    return 1 / (1j * w * C1) + R2 + 1j * w * L2 + R3


def imp_gen(w):
    return 1 / (1 / imp1(w) + 1 / imp2(w))


def general_amperage(w, voltage_in):
    return voltage_in / (R1 + 1j * w * L1 + imp_gen(w))


def voltage(w, voltage_in):
    return general_amperage(w, voltage_in) * imp_gen(w)


def amperage(w, voltage_in):
    return voltage(w, voltage_in) / imp2(w)


def voltage_out(w, voltage_in):
    return amperage(w, voltage_in) * R2


def search_res(w, voltage_in):
    return voltage_out(w, voltage_in) / voltage_in


w_values = np.linspace(0, 100, 1000)
plt.plot(w_values, np.abs(search_res(w_values, 10)), label='АЧХ')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.legend()
plt.show()

signal = np.loadtxt("C:\\Users\\lesya\\OneDrive\\Документы\\универ\\фоит\\IDZ3\\14.txt")
time_values = np.arange(0, N1 * dt, dt)
plt.plot(time_values, signal, label='Сигнал')
plt.xlabel('Время')
plt.ylabel('Значение сигнала')
plt.legend()
plt.show()

transformed_signal = np.fft.fft(signal)
frequency_values = np.fft.fftfreq(N1, dt)
amplitudes = np.abs(transformed_signal)
plt.plot(2 * np.pi * frequency_values, amplitudes, label='Спектр')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.legend()
plt.show()


print(np.abs(search_res(W1, 1)))
