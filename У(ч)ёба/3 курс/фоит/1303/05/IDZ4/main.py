import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
import sounddevice as sd

class SignalProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.discretCode = self.load_signal()

    def load_signal(self):
        with open(self.filename, 'r') as file:
            discretCode = [line.strip().split('\t') for line in file]

        return [int(''.join(b), 2) for b in discretCode]

    def plot_signal(self, time_axis, signal, title, xlabel='Время', ylabel='Амплитуда'):
        plt.plot(time_axis, signal)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def filter_butterworth(self, freq_range, Uin, R1, L1, L2, L3, L4, L5, C1, C2, C3, C4, C5):
        Z5 = 1 / (1j * freq_range * C5 + 1 / R1)
        Z4 = 1 / (1j * freq_range * C4 + 1 / (1j * freq_range * L5 + Z5))
        Z3 = 1 / (1j * freq_range * C3 + 1 / (1j * freq_range * L4 + Z4))
        Z2 = 1 / (1j * freq_range * C2 + 1 / (1j * freq_range * L3 + Z3))
        Z = 1 / (1j * freq_range * C1 + 1 / (1j * freq_range * L2 + Z2))
        I1 = Uin / (1j * freq_range * L1 + Z)
        U = I1 * Z
        I2 = U / (1j * freq_range * L2 + Z2)
        U2 = I2 * Z2
        I3 = U2 / (1j * freq_range * L3 + Z3)
        U3 = I3 * Z3
        I4 = U3 / (1j * freq_range * L4 + Z4)
        U4 = I4 * Z4
        I5 = U4 / (1j * freq_range * L5 + Z5)
        U5 = I5 * Z5
        Uout = U5
        return Uout / Uin

    def process_signal(self, R1, L1, L2, L3, L4, L5, C1, C2, C3, C4, C5, sample_rate=45000):
        dt = 3 / len(self.discretCode)
        time_axis = np.linspace(0, 3, len(self.discretCode))

        self.plot_signal(time_axis, self.discretCode, 'Сигнал во временной области')

        fsig = fft(self.discretCode)
        out_n = len(fsig)
        freq_axis = np.fft.fftfreq(out_n, dt)[1:]

        self.plot_signal(freq_axis, np.abs(fsig[1:]), 'Спектр сигнала во временной области', 'Частота', 'Амплитуда')

        Uin_value = 1
        freq_range = np.linspace(1, out_n / 10, out_n - 1)
        filter_response = np.abs(self.filter_butterworth(freq_range, Uin_value, R1, L1, L2, L3, L4, L5, C1, C2, C3, C4, C5))

        self.plot_signal(freq_range, filter_response, 'АЧХ', 'Частота', 'Амплитуда')

        H_list = filter_response
        F_new = fsig[1:] * H_list

        self.plot_signal(freq_axis, np.abs(F_new), 'Спектр фильтрованного сигнала', 'Частота', 'Амплитуда')

        changed_signal = ifft(np.concatenate(([0], F_new)))
        filtered_time_axis = np.linspace(0, 3, len(changed_signal))

        self.plot_signal(filtered_time_axis, np.real(changed_signal), 'Выходной сигнал временной области')

        sd.play(np.real(changed_signal), sample_rate)
        sd.wait()

# Параметры фильтра и обработки сигнала
R1 = 50
L1 = 0.01
L2 = 0.012
L3 = 0.01
L4 = 0.007
L5 = 0.003
C1 = 0.000005
C2 = 0.0000045
C3 = 0.0000035
C4 = 0.000002
C5 = 497.9 * 10 ** -9

filename = "./signaldigit5.txt"

# Создание экземпляра SignalProcessor и обработка сигнала
signal_processor = SignalProcessor(filename)
signal_processor.process_signal(R1, L1, L2, L3, L4, L5, C1, C2, C3, C4, C5)
