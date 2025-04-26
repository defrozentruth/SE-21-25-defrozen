import matplotlib.pyplot as plt
import numpy as np

L1 = 13.2094490761272
L2 = .834706894606612
C1 = 1.16365869528265E-05
C2 =  1.300478410357E-05
R1 = 114.535253054028
R2 = 32.1696621442138
R3 = 1052.22025365489
R4 = 529.813173240116
N = 8192
dt = 0.0196349540849362


def read_file():
    with open('12.txt', 'r') as f:
        data = [float(line) for line in f.readlines()[:N]]
    return data

def draw_signal():
    plt.title('s_вход(t)')
    plt.xlabel('t, c')
    plt.ylabel('s_вход')
    plt.plot(time, signal, color='red')
    plt.show()

def draw_amplitude():
    plt.title('A_вход(ω)')
    plt.xlabel('ω, рад/c')
    plt.ylabel('A_вход')
    plt.plot(frequency[:stop_i], spectre_module[:stop_i], color='red')
    plt.show()

def calculate_h(omega):
    Z_C1 = 1 / (1j * omega * C1)
    Z_C2 = 1 / (1j * omega * C2)
    Z_L1 = 1j * omega * L1
    Z_L2 = 1j * omega * L2
    r_output = R3 * (R4 + Z_C2) / (R4 + Z_C2 + Z_C1 + R2 + Z_L2 + R3)
    r_parallel = ((R4 + Z_C2) * (Z_C1 + R2 + Z_L2 + R3)) / (R4 + Z_C2 + Z_C1 + R2 + Z_L2 + R3)
    r_input = R1 + Z_L1 + r_parallel
    return r_output / r_input

def calculate_stop_i():
    stop_i = next((i + 1 for i, val in enumerate(frequency) if 2 * np.pi * df * i > 100), 0)
    return stop_i

def draw_afr():
    plt.title('|H(iω)|')
    plt.xlabel('ω, рад/c')
    plt.ylabel('|H|')
    plt.plot(frequency[1:stop_i], H[:stop_i-1], color='red')
    plt.show()

if __name__ == '__main__':
    j = 1j
    df = 1 / (dt * N)
    signal = read_file()
    time = np.arange(0, dt * N, dt)
    spectre = np.fft.fft(signal)
    spectre_module = np.abs(spectre)  
    frequency = 2 * np.pi * np.arange(N) * df 
    stop_i = calculate_stop_i()
    H = np.abs([calculate_h(omega) for omega in frequency[1:]])
    H_ans = calculate_h(40) 
    draw_signal()
    draw_amplitude()
    draw_afr()
    print(abs(H_ans))
