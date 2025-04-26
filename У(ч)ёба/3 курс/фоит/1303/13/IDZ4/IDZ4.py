import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
import sounddevice as sd

duration = 2.5
resistor_R1 = 50
capacitor_C1 = 0.000005
capacitor_C2 = 0.0000045
capacitor_C3 = 0.0000035
capacitor_C4 = 0.000002
capacitor_C5 = 497.9 * 10**-9
inductor_L1 = 0.01
inductor_L2 = 0.012
inductor_L3 = 0.01
inductor_L4 = 0.007
inductor_L5 = 0.003

with open("signaldigit13.txt", 'r') as file:
    digital_signal = [line.strip().split('\t') for line in file]

analog_signal = [int(''.join(bits), 2) for bits in digital_signal]

time_step = duration / len(digital_signal)

sample_rate = 44100
time_axis = np.linspace(0, duration, len(analog_signal))

def filter(w, U_in):
    Z_parallel_5 = 1 / (1j * w * capacitor_C5 + 1 / resistor_R1)
    Z_parallel_4 = 1 / (1j * w * capacitor_C4 + 1 / (1j * w * inductor_L5 + Z_parallel_5))
    Z_parallel_3 = 1 / (1j * w * capacitor_C3 + 1 / (1j * w * inductor_L4 + Z_parallel_4))
    Z_parallel_2 = 1 / (1j * w * capacitor_C2 + 1 / (1j * w * inductor_L3 + Z_parallel_3))
    Z_parallel = 1 / (1j * w * capacitor_C1 + 1 / (1j * w * inductor_L2 + Z_parallel_2))
    I1 = U_in / (1j * w * inductor_L1 + Z_parallel)
    U_parallel = I1 * Z_parallel
    I2 = U_parallel / (1j * w * inductor_L2 + Z_parallel_2)
    U_parallel_2 = I2 * Z_parallel_2
    I3 = U_parallel_2 / (1j * w * inductor_L3 + Z_parallel_3)
    U_parallel_3 = I3 * Z_parallel_3
    I4 = U_parallel_3 / (1j * w * inductor_L4 + Z_parallel_4)
    U_parallel_4 = I4 * Z_parallel_4
    I5 = U_parallel_4 / (1j * w * inductor_L5 + Z_parallel_5)
    U_parallel_5 = I5 * Z_parallel_5
    U_out = U_parallel_5
    result = U_out / U_in
    return result

plt.plot(time_axis, analog_signal)
plt.title('Analog Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

frequency_spectrum = fft(analog_signal)
num_samples = len(frequency_spectrum)
dt = 1 / len(analog_signal)
frequency_axis = np.fft.fftfreq(num_samples, dt)[1:]
plt.plot(frequency_axis, np.abs(frequency_spectrum[1:]))
plt.title('Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

U_in_value = 1
frequency_range = np.linspace(1, num_samples, num_samples - 1)
filter_response = np.abs(filter(frequency_range, U_in_value))

plt.plot(frequency_range, filter_response)

plt.title('Normalized Filter Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.xlim(0, 10000)
plt.show()

H_list = filter_response
F_new = frequency_spectrum[1:] * H_list

plt.plot(frequency_axis, np.abs(F_new))
plt.title('Filtered Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()



filtered_signal = ifft(np.concatenate(([0], F_new)))
filtered_time_axis = np.linspace(0, duration, len(filtered_signal))

plt.plot(filtered_time_axis, np.real(filtered_signal))
plt.title('Filtered Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

wavfile.write('filtered_signal.wav', sample_rate, np.real(filtered_signal).astype(np.int16))
sd.play(np.real(filtered_signal), sample_rate)
sd.wait()
