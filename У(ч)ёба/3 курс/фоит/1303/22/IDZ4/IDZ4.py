import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

C = 0.00001  # 10 мкФ
R = 1000  # 1 кОм
U = 5  # 5 В


def ZC(w, C):
    if 1j * w * C == 0:
        return np.inf
    return 1 / (1j * w * C)


def R_in(w):
    if ZC(w, C) == np.inf:
        return np.inf
    return R + ZC(w, C)


def I_in(w, U_in):
    return U_in / R_in(w)


# фильтр низких частот RC
def H(w, U_in):
    U_out = I_in(w, U_in) * ZC(w, C)
    return U_out / U_in


if __name__ == '__main__':
    # Аналоговый сигнал
    analogue_signal = []
    with open('signaldigit22.txt', 'r') as file:
        for line in file:
            bits_string = line.strip().split('\t')
            bits = ''.join(bits_string)
            analogue_signal.append(int(bits, 2))

    scaled = np.float32(np.real(analogue_signal) / np.max(np.abs(np.real(analogue_signal))) * 1.0)
    # Запись звукового сигнала в файл
    write('original22.wav', 44100, scaled)

    N = len(analogue_signal)
    T = 3.75
    dt = T / N

    # Сигнал на входе
    time_array = np.arange(0, T, dt)
    plt.plot(time_array, analogue_signal)
    plt.xlabel('t')
    plt.ylabel('U')
    plt.show()

    # Спектр на входе
    F = np.fft.fft(analogue_signal)
    A = [np.abs(i) * 2 / N for i in F[1:]]
    w = [i * 2 * np.pi / T for i in range(N)]
    plt.plot(w[:int(len(w) / 2)], A[:int(len(A) / 2)])
    plt.xlabel('w')
    plt.ylabel('A')
    plt.show()

    # АЧХ
    U = 5
    H_array = [np.abs(H(w_elem, U)) for w_elem in w]
    plt.plot(w[:450], H_array[:450])
    plt.xlabel('Hz')
    plt.ylabel('H')
    plt.show()

    # Выходной спектр
    F_new = []
    for i in range(len(F)-1):
        F_new.append(F[i+1] * H_array[i+1])
    A = [np.abs(i) * 2 / N for i in F_new]
    plt.plot(w[:int(len(w) / 2)], A[:int(len(A) / 2)])
    plt.xlabel('w')
    plt.ylabel('A')
    plt.show()

    # Выходной сигнал
    analogue_signal_out = np.fft.ifft(F_new)
    print(analogue_signal_out)
    plt.plot(time_array[1:], analogue_signal_out)
    plt.xlabel('t')
    plt.ylabel('U')
    plt.show()

    scaled = np.float32(np.real(analogue_signal_out) / np.max(np.abs(np.real(analogue_signal_out))) * 1.0)
    # Запись выходного звукового сигнала в файл
    write('filtered22.wav', 44100, scaled)
