import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
import sounddevice as sd


def butterworth_filter(w, Uin):
    Z5 = 1 / (1j * w * C5 + 1 / R1)
    Z4 = 1 / (1j * w * C4 + 1 / (1j * w * L5 + Z5))
    Z3 = 1 / (1j * w * C3 + 1 / (1j * w * L4 + Z4))
    Z2 = 1 / (1j * w * C2 + 1 / (1j * w * L3 + Z3))
    Z = 1 / (1j * w * C1 + 1 / (1j * w * L2 + Z2))
    I1 = Uin / (1j * w * L1 + Z)
    U = I1 * Z
    I2 = U / (1j * w * L2 + Z2)
    U2 = I2 * Z2
    I3 = U2 / (1j * w * L3 + Z3)
    U3 = I3 * Z3
    I4 = U3 / (1j * w * L4 + Z4)
    U4 = I4 * Z4
    I5 = U4 / (1j * w * L5 + Z5)
    U5 = I5 * Z5
    Uout = U5
    return Uout / Uin


def show(plot1, plot2, title, xlabel):
    plt.plot(plot1, plot2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Amplitude')
    plt.show()


duration = 3

filename = "./signaldigit8.txt"

R1 = 50

C1 = 0.000005
C2 = 0.0000045
C3 = 0.0000035
C4 = 0.000002
C5 = 497.9 * 10 ** -9

L1 = 0.01
L2 = 0.012
L3 = 0.01
L4 = 0.007
L5 = 0.003

with open(filename, 'r') as file:
    discrete_signal = [line.strip().split('\t') for line in file]

analog_signal = [int(''.join(b), 2) for b in discrete_signal]
dt = duration / len(discrete_signal)

# Входной сигнал
sample_rate = 44100
time_axis = np.linspace(0, duration, len(analog_signal))
show(time_axis, analog_signal, 'Analog Signal', 'Time (s)')

# Спектр
fsig = fft(analog_signal)
out_n = len(fsig)
df = 1 / dt
freq_axis = np.fft.fftfreq(out_n, dt)[1:]
show(freq_axis, np.abs(fsig[1:]), 'Spectrum', 'Frequency (Hz)')

# Частотная характеристика фильтра
Uin_value = 1
freq_range = np.linspace(1, out_n / 10, out_n - 1)
filter_response = np.abs(butterworth_filter(freq_range, Uin_value))
show(freq_range, filter_response, 'Frequency response', 'Frequency (Hz)')

# Применение фильтра
H_list = filter_response
F_new = fsig[1:] * H_list
show(freq_axis, np.abs(F_new), 'Filtered Spectrum', 'Frequency (Hz)')

# Обратное преобразование Фурье
changed_signal = ifft(np.concatenate(([0], F_new)))
filtered_time_axis = np.linspace(0, duration, len(changed_signal))
show(filtered_time_axis, np.real(changed_signal), 'Filtered Signal', 'Time (s)')

# Воспроизводим отфильтрованный сигнал
sd.play(np.real(changed_signal), sample_rate)
sd.wait()


