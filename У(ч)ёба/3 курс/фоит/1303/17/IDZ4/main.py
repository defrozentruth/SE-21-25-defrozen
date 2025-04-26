import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
from scipy.io.wavfile import write

coef = 7

t = 4.25
file_path = 'signaldigit17.txt'
R = 50
L1 = 12.4E-3 * coef
L2 = 14.4E-3 * coef
L3 = 12E-3 * coef
L4 = 8.3E-3 * coef
L5 = 3.7E-3 * coef
C1 = 5.9E-6 * coef
C2 = 5.4E-6 * coef
C3 = 4.1E-6 * coef
C4 = 2.4E-6 * coef
C5 = 497.9E-9 * coef
sample_rate = 41400


def zl(l, omega):
    return 1j * omega * l


def zc(c, omega):
    return 1 / (1j * omega * c)


def butterworth_filter(omega):
    z5 = 1 / (1 / R + 1 / zc(C5, omega))
    z4 = 1 / (1 / zc(C4, omega) + 1 / (z5 + zl(L5, omega)))
    z3 = 1 / (1 / zc(C3, omega) + 1 / (z4 + zl(L4, omega)))
    z2 = 1 / (1 / zc(C2, omega) + 1 / (z3 + zl(L3, omega)))
    z1 = 1 / (1 / zc(C1, omega) + 1 / (z2 + zl(L2, omega)))
    zl1 = zl(L1, omega)
    z = zl1 + z1
    i_in = 1 / z
    u1 = i_in * z1
    i1 = u1 / (z2 + zl(L2, omega))
    u2 = i1 * z2
    i2 = u2 / (z3 + zl(L3, omega))
    u3 = i2 * z3
    i3 = u3 / (z4 + zl(L4, omega))
    u4 = i3 * z4
    i4 = u4 / (z5 + zl(L5, omega))
    u5 = i4 * z5
    return u5


def save_audio(signal, filename):
    write(filename, 44100, np.array(signal).astype(np.float32))


with open(file_path, 'r') as file:
    discrete_signal = [line.strip().split('\t') for line in file]

analog_signal = [int(''.join(b), 2) for b in discrete_signal]
dt = t / len(discrete_signal)

# Input signal
time_axis = np.linspace(0, t, len(analog_signal))
plt.plot(time_axis, analog_signal)
plt.title('Analog Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

# Spectre calculation
fsig = fft(analog_signal)
out_n = len(fsig)
freq_axis = np.abs(np.fft.fftfreq(out_n, dt)[1:])
plt.plot(freq_axis, np.abs(fsig[1:]))
plt.title('Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Filter's frequency response
freq_range = freq_axis
filter_response = np.abs(butterworth_filter(freq_range))

plt.plot(freq_range, filter_response)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Filter's application
H_list = filter_response
F_new = fsig[1:] * H_list
plt.plot(freq_axis, np.abs(F_new))
plt.title('Filtered Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Inverse Fourier transform
filtered_signal = np.real(ifft(np.concatenate(([0], F_new))))
filtered_time_axis = np.linspace(0, t, len(filtered_signal))

# Filtered signal plot
plt.plot(filtered_time_axis, filtered_signal)
plt.title('Filtered Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

# Play audio file
save_audio(filtered_signal, 'filtered_signal.wav')
