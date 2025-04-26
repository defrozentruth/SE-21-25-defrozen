import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
import sounddevice as sd

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

with open("C:\\Users\\Полина\\PycharmProjects\\foit4\\signaldigit23.txt", 'r') as file:
    discretCode = [line.strip().split('\t') for line in file]

decimalCode = [int(''.join(b), 2) for b in discretCode]
dt = 3 / len(discretCode)

sampleRate = 45000


def input():
    timeAxis = np.linspace(0, 3, len(decimalCode))
    plt.plot(timeAxis, decimalCode)
    plt.title('Сигнал во временной области')
    plt.xlabel('Время')
    plt.ylabel('Амплитуда')
    plt.show()

def filter(w, Uin):
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

def spectr():
    fsig = fft(decimalCode)
    out_n = len(fsig)
    df= 1/3
    freq_axis = np.fft.fftfreq(out_n, dt)[1:]
    plt.plot(freq_axis, np.abs(fsig[1:]))
    plt.title('Спектр сигнала во временной области')
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.show()

    Uin_value = 1
    freq_range = np.linspace(1, out_n / 10, out_n - 1)
    filter_response = np.abs(filter(freq_range, Uin_value))

    plt.plot(freq_range, filter_response)
    plt.title('АЧХ')
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.show()

    H_list = filter_response
    F_new = fsig[1:] * H_list
    plt.plot(freq_axis, np.abs(F_new))
    plt.title('Спектр фильтрованного сигнала')
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.show()

    changed_signal = ifft(np.concatenate(([0], F_new)))
    filteredTimeAxis = np.linspace(0, 3, len(changed_signal))

    plt.plot(filteredTimeAxis, np.real(changed_signal))
    plt.title('Выходной сигнал временной области')
    plt.xlabel('Время')
    plt.ylabel('Амплитуда')
    plt.show()

    sd.play(np.real(changed_signal), sampleRate)
    sd.wait()

input()
spectr()
