import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
import sounddevice as sd


def read_analog_signal(filename):
    with open(filename, 'r') as file:
        discret_signal = [line.strip().split('\t') for line in file]
    return [int(''.join(b), 2) for b in discret_signal]


def plot_time_domain(signal, t):
    time_axis = np.linspace(0, t, len(signal))
    plt.plot(time_axis, signal)
    plt.title('Input Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()


def plot_frequency_spectrum(signal):
    fsig = fft(signal)
    out_n = len(fsig)
    dt = 1 / len(signal)
    freq_axis = np.fft.fftfreq(out_n, dt)[1:]
    plt.plot(freq_axis, np.abs(fsig[1:]))
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.show()


def butterworth_filter(w, Uin):
    coefficient = 2
    L1 = 12.4 * pow(10, -3) * coefficient
    L2 = 14.4 * pow(10, -3) * coefficient
    L3 = 12 * pow(10, -3) * coefficient
    L4 = 8.3 * pow(10, -3) * coefficient
    L5 = 3.7 * pow(10, -3) * coefficient
    C1 = 5.9 * pow(10, -6) * coefficient
    C2 = 5.4 * pow(10, -6) * coefficient
    C3 = 4.1 * pow(10, -6) * coefficient
    C4 = 2.4 * pow(10, -6) * coefficient
    C5 = 497.9 * pow(10, -9) * coefficient
    R1 = 50
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


def apply_butterworth_filter(signal):
    fsig = fft(signal)
    out_n = len(fsig)
    dt = 1 / len(signal)
    freq_axis = np.fft.fftfreq(out_n, dt)[1:]
    freq_range = np.linspace(1, out_n, out_n - 1)
    filter_response = np.abs(butterworth_filter(freq_range, 1))

    plt.plot(freq_range, filter_response)
    plt.title('Normalized Filter Frequency Response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(0, 10000)
    plt.show()

    H_list = filter_response
    F_new = fsig[1:] * H_list

    plt.plot(freq_axis, np.abs(F_new))
    plt.title('Filtered Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.show()

    changed_signal = ifft(np.concatenate(([0], F_new)))
    return np.real(changed_signal)


def plot_filtered_signal(filtered_signal, t):
    filtered_time_axis = np.linspace(0, t, len(filtered_signal))
    plt.plot(filtered_time_axis, filtered_signal)
    plt.title('Filtered Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()


def play_audio(signal, sample_rate):
    sd.play(signal, sample_rate)
    sd.wait()


if __name__ == "__main__":
    file_path = "signaldigit1.txt"
    analog_signal = read_analog_signal(file_path)

    t = 3.75

    plot_time_domain(analog_signal, t)
    plot_frequency_spectrum(analog_signal)

    filtered_signal = apply_butterworth_filter(analog_signal)

    plot_filtered_signal(filtered_signal, t)
    play_audio(filtered_signal, 44100)
