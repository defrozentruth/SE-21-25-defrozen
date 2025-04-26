import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


L1 = 12.7576133279707
L2 = 0.841565920759344
C1 = 1.16260817766959E-05
C2 = 1.16344719576061E-05
R1 = 103.964713724715
R2 = 38.8929043059504
R3 = 1010.17891797018
R4 = 532.970900039001
N = 8192
dt = 0.0196349540849362


def ZL(w, L):
    return 1j * w * L


def ZC(w, C):
    if 1j * w * C == 0:
        return np.inf
    return 1 / (1j * w * C)


def R_in(w):
    if ZC(w, C1) == np.inf or ZC(w, C2) == np.inf:
        return np.inf
    return R1 + ZL(w, L1) + (1 / (1 / (ZC(w, C1) + R2 + ZL(w, L2) + R3) + 1 / (R4 + ZC(w, C2))))


def I_in(w, U_in):
    return U_in / R_in(w)


def U_parallel(w, U_in):
    if ZC(w, C1) == np.inf or ZC(w, C2) == np.inf:
        return np.inf
    i_in = I_in(w, U_in)
    return i_in * (1 / (1 / (ZC(w, C1) + R2 + ZL(w, L2) + R3) + 1 / (R4 + ZC(w, C2))))


def I_parallel_1(w, U_in):
    u_parallel = U_parallel(w, U_in)
    return u_parallel / (R4 + ZC(w, C2))


def U_out(w, U_in):
    i_parallel_1 = I_parallel_1(w, U_in)
    return i_parallel_1 * R4


def H(w, U_in):
    u_out = U_out(w, U_in)
    return u_out / U_in


if __name__ == '__main__':
    T = dt * N
    U = 5  # Вольт

    # АЧХ
    w_array = np.linspace(0, 100, 1000)
    H_array = [np.abs(H(w, U)) for w in w_array]
    plt.plot(w_array, H_array)
    plt.vlines(35, 0, 0.6, color='red')
    plt.xlabel('Hz')
    plt.ylabel('H')
    plt.show()

    # Сигнал
    signal = np.loadtxt("22.txt")
    time_array = np.arange(0, T, dt)
    plt.plot(time_array, signal)
    plt.xlabel('t')
    plt.ylabel('U')
    plt.show()

    # Спектр
    F = sp.fft.fft(signal)
    A_array = [np.abs(i) for i in F]
    w_array = [i * 2 * np.pi / T for i in range(N)]
    plt.plot(w_array[:int(len(w_array) / 2)], A_array[:int(len(A_array) / 2)])
    plt.xlabel('w')
    plt.ylabel('A(w)')
    plt.show()

    # Ответ
    w_4_harmonica = 35
    answer = np.abs(H(w_4_harmonica, U))
    print(answer)
