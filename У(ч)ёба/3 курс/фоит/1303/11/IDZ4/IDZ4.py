import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
import sounddevice as sd

t = 3
file_path = "C:\\Users\\syrtc\\Downloads\\signaldigit11.txt"

with open(file_path, 'r') as file:
    discret_signal = [line.strip().split('\t') for line in file]


def butterworth_filter(w, Uin):
    Zpar5 = 1 / (1j * w * C5 + 1 / R1)
    Zpar4 = 1 / (1j * w * C4 + 1 / (1j * w * L5 + Zpar5))
    Zpar3 = 1 / (1j * w * C3 + 1 / (1j * w * L4 + Zpar4))
    Zpar2 = 1 / (1j * w * C2 + 1 / (1j * w * L3 + Zpar3))
    Zpar = 1 / (1j * w * C1 + 1 / (1j * w * L2 + Zpar2))
    I1 = Uin / (1j * w * L1 + Zpar)
    Upar = I1 * Zpar
    I2 = Upar / (1j * w * L2 + Zpar2)
    Upar2 = I2 * Zpar2
    I3 = Upar2 / (1j * w * L3 + Zpar3)
    Upar3 = I3 * Zpar3
    I4 = Upar3 / (1j * w * L4 + Zpar4)
    Upar4 = I4 * Zpar4
    I5 = Upar4 / (1j * w * L5 + Zpar5)
    Upar5 = I5 * Zpar5
    Uout = Upar5
    return Uout / Uin


analog_signal = [int(''.join(b), 2) for b in discret_signal]
dt = t / len(discret_signal)

# Входной сигнал
sample_rate = 44100
time_axis = np.linspace(0, t, len(analog_signal))
plt.plot(time_axis, analog_signal)
plt.title('Analog Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

# Находим спектр
fsig = fft(analog_signal)
out_n = len(fsig)
df = 1 / t
freq_axis = np.fft.fftfreq(out_n, df)[1:]
plt.plot(freq_axis, np.abs(fsig[1:]))
plt.title('Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Фильтр Баттерворта
coef = 2.0
R1 = 50
C1 = 0.0000059 * coef
C2 = 0.0000054 * coef
C3 = 0.0000041 * coef
C4 = 0.0000024 * coef
C5 = 497.9 * 10 ** -9 * coef
L1 = 0.0124 * coef
L2 = 0.0144 * coef
L3 = 0.012 * coef
L4 = 0.0083 * coef
L5 = 0.0037 * coef

# АЧХ фильтра
Uin_value = 1
freq_response = np.vectorize(lambda w: butterworth_filter(w, Uin_value))
freq_range = np.linspace(1, out_n / 10, out_n - 1)
filter_response = np.abs(freq_response(freq_range))

plt.plot(freq_range, filter_response)
plt.title('Normalized Filter Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Применение фильтра
H_list = filter_response
F_new = fsig[1:] * H_list
plt.plot(freq_axis, np.abs(F_new))
plt.title('Filtered Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Обратное преобразование Фурье
changed_signal = ifft(np.concatenate(([0], F_new)))
filtered_signal = np.column_stack((time_axis, np.real(changed_signal)))

# График сигнала после применения фильтра
plt.plot(filtered_signal[:, 0], filtered_signal[:, 1])
plt.title('Filtered Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

# Воспроизводим отфильтрованный сигнал
sd.play(filtered_signal[:, 1], sample_rate)
sd.wait()
