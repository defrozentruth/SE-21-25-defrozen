import matplotlib.pyplot as plt
import numpy as np
import wave
import struct

def read_file(file_path):
    with open(file_path, 'r') as f:
        data = [int(line.replace("\t", ""), 2) for line in f.readlines()]
    return data


def set_plot_style(title, xlabel, ylabel):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def draw_signal(signal_type, time, signal):
    set_plot_style(f'{signal_type}(t)', 't, c', f'{signal_type}')
    plt.plot(time, signal, color='blue')
    plt.show()

def draw_amplitude(amplitude_type, frequency, amplitude):
    set_plot_style(f'A_{amplitude_type}(f)', 'f, Гц', f'A_{amplitude_type}')
    plt.plot(frequency[1:], amplitude[1:], color='green')
    plt.show()

def calculate_h(omega):
    C = 0.000000001
    R0 = 125
    Z_C = 1 / (1j * omega * C)  # 1j вместо j
    R = [Z_C]
    r_input = 1
    n = 255
    for i in range(1, n):
        R.append((Z_C * (R0 + R[i - 1])) / (Z_C + R0 + R[i - 1]))
    for i in range(n):
        a = 1 + ((R0 + R[i]) / Z_C)
        r_input *= a
    r_input *= (R0 + (Z_C * (R0 + R[-1])) / (Z_C + R0 + R[-1]))
    r_output = Z_C
    return r_output / r_input

def draw_afr(frequency, h_values):
    set_plot_style('|H(if)|', 'f, Гц', '|H|')
    plt.plot(frequency, [abs(h_i) for h_i in h_values], color='red')
    plt.show()

def create_wav(signal, filename):
    sample_width = 2
    sample_rate = 44100
    with wave.open(filename, mode="wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(sample_width)
        audio.setframerate(sample_rate)
        for value in signal:
            packed_value = struct.pack('h', int(value))
            audio.writeframes(packed_value)

def calculate_stop_i(N, df):
    stop_i = 0
    frequency = [2 * np.pi * df * i for i in range(N)]  # Вынесено за пределы цикла
    for i in range(N):
        if frequency[i] > 20000 and stop_i == 0:
            stop_i = i + 1
    return stop_i

if __name__ == '__main__':
    j = complex(0, 1)
    gain = 1000
    file_path = 'signaldigit12.txt'
    signal_input = read_file(file_path)
    create_wav(signal_input, "input.wav")
    N = len(signal_input)
    t = 3.25
    dt = t / N
    df = 1 / t
    time = [dt * i for i in range(N)]
    spectre_input = np.fft.fft(signal_input)
    spectre_input_module = [abs(number) for number in spectre_input]
    frequency = [df * i for i in range(N)]
    H = [calculate_h(_) for _ in frequency[1:]]
    spectre_input_sliced = spectre_input[1:]
    spectre_output = [gain * spectre_input_sliced[i] * H[i] for i in range(N - 1)]
    spectre_output_module = [abs(number) for number in spectre_output]
    signal_output = np.fft.ifft(spectre_output)
    signal_output_real = [number.real for number in signal_output]
    stop_i = calculate_stop_i(N, df)
    draw_signal('input', time, signal_input)
    draw_amplitude('input', frequency[:stop_i], spectre_input_module[:stop_i])
    draw_amplitude('output', frequency[1:stop_i], spectre_output_module[:stop_i - 1])
    draw_signal('output', time[1:], signal_output_real)
    draw_afr(frequency[1:stop_i], H[:stop_i - 1])
    create_wav(signal_output_real, "output.wav")
