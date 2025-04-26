import numpy as np
import matplotlib.pyplot as plt


def first_imp(w):
    return R4 + 1 / (1j * w * C2)


def second_imp(w):
    return 1 / (1j * w * C1) + R2 + 1j * w * L2 + R3


def total_imp(w):
    return 1 / (1 / first_imp(w) + 1 / second_imp(w))


def total_current(w, voltage_in):
    return voltage_in / (R1 + 1j * w * L1 + total_imp(w))


def voltage(w, voltage_in):
    return total_current(w, voltage_in) * total_imp(w)


def currency(w, voltage_in):
    return voltage(w, voltage_in) / second_imp(w)


def voltage_out(w, voltage_in):
    return currency(w, voltage_in) * R2


def calculate_result(w, voltage_in):
    return voltage_out(w, voltage_in) / voltage_in


# Constants
L1 = 13.478813706353
L2 = 0.539627224025902
C1 = 1.14099638451438E-05
C2 = 1.05777339618707E-05
R1 = 110.39005121382
R2 = 33.1018858020053
R3 = 1029.4684106921
R4 = 502.42136316014
N1 = 8192
dt = 0.0196349540849362
t = dt * N1

W1 = 5
#


def process():
    w_list = np.linspace(0, 100, 1000)
    plt.plot(w_list, np.abs(calculate_result(w_list, 10)), label='АЧХ')
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.show()

    signal_data = np.loadtxt("17.txt")
    time_list = np.arange(0, N1 * dt, dt)
    plt.plot(time_list, signal_data, label='Сигнал')
    plt.xlabel('Время')
    plt.ylabel('Значение сигнала')
    plt.legend()
    plt.show()

    transformed_signal = np.fft.fft(signal_data)
    frequency_list = np.fft.fftfreq(N1, dt)
    amplitude_list = np.abs(transformed_signal)
    plt.plot(2 * np.pi * frequency_list, amplitude_list, label='Спектр')
    ax = plt.gca()
    ax.set_xlim([-1, 40])
    plt.xlabel('Частота')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.show()

    print(np.abs(calculate_result(W1, 1)))


if __name__ == '__main__':
    process()
