import numpy as np
import matplotlib.pyplot as plt


def first_imp(w):
    return R4 + 1 / (1j * w * C2)


def second_imp(w):
    return 1 / (1j * w * C1) + R2 + 1j * w * L2 + R3


def general_imp(w):
    return 1 / (1 / first_imp(w) + 1 / second_imp(w))


def general_amperage(w, voltage_in):
    return voltage_in / (R1 + 1j * w * L1 + general_imp(w))


def voltage(w, voltage_in):
    return general_amperage(w, voltage_in) * general_imp(w)


def amperage(w, voltage_in):
    return voltage(w, voltage_in) / second_imp(w)


def voltage_out(w, voltage_in):
    return amperage(w, voltage_in) * R2


def search_res(w, voltage_in):
    return voltage_out(w, voltage_in) / voltage_in


L1 = 12.9659516344536
L2 = 0.705540831297699
C1 = 0.0000103584165669401
C2 = 0.0000101916476188708
R1 = 114.872909312688
R2 = 34.6560463356828
R3 = 1077.17303654506
R4 = 510.402278188681
N1 = 8192
dt = 0.0196349540849362
t = dt * N1

w_values = np.linspace(0, 100, 1000)
plt.plot(w_values, np.abs(search_res(w_values, 10)), label='АЧХ')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.legend()
plt.show()

signal = np.loadtxt("C:\\Users\\syrtc\\OneDrive\\Рабочий стол\\!\\3 КУРС\\ФОИТ\\IDZ3\\11.txt")
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

freq_harmonic_1 = 10

print(np.abs(search_res(freq_harmonic_1, 10)))
