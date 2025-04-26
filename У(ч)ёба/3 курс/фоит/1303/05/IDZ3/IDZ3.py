import matplotlib.pyplot as plt
import numpy as np

class CircuitAnalyzer:
    def __init__(self):
        self.L1 = 13.8628000224179
        self.L2 = 0.712836258342916
        self.C1 = 1.16422284290391E-05
        self.C2 = 1.47313522140348E-05
        self.R1 = 107.70872811802
        self.R2 = 30.4723663733368
        self.R3 = 1014.70686271098
        self.R4 = 501.625092437796
        self.N = 8192
        self.dt = 0.0196349540849362
        self.df = 1 / (self.dt * self.N)
        self.spectreAbs = None
        self.sequence = None
        self.H = None

    def read_signal_from_file(self, filename='5.txt'):
        with open(filename, 'r') as file:
            signal = [float(line) for line in file]
        return signal

    def draw_signal(self, signal):
        time = [self.dt * i for i in range(self.N)]
        plt.title('Сигнал')
        plt.xlabel('t')
        plt.ylabel('s')
        plt.plot(time, signal)
        plt.show()

    def draw_amplitude(self, is_stop):
        plt.title('Амплитуда входа')
        plt.xlabel('ω')
        plt.ylabel('A')
        plt.plot(self.sequence[:is_stop], self.spectreAbs[:is_stop])
        plt.show()

    def calculate_H(self, w):
        j = complex(0, 1)
        Z_C1 = 1 / (j * w * self.C1)
        Z_C2 = 1 / (j * w * self.C2)
        Z_L1 = j * w * self.L1
        Z_L2 = j * w * self.L2
        R_input = self.R1 + Z_L1 + (self.R4 + Z_C2) * (self.R2 + self.R3 + Z_C1 + Z_L2) / \
                  (self.R2 + self.R3 + self.R4 + Z_C1 + Z_C2 + Z_L2)
        R_output = (self.R4 + Z_C2) * self.R2 / (self.R2 + self.R3 + self.R4 + Z_C1 + Z_C2 + Z_L2)
        return R_output / R_input

    def draw_amplitude_frequency_response(self, is_stop):
        plt.title('H')
        plt.xlabel('ω, рад/c')
        plt.ylabel('H')
        plt.plot(self.sequence[1:is_stop], self.H[:is_stop - 1])
        plt.show()

    def analyze_circuit(self):
        signal = self.read_signal_from_file()
        self.draw_signal(signal)

        self.spectre = np.fft.fft(signal)
        self.spectreAbs = [abs(each) for each in self.spectre]
        self.sequence = [2 * np.pi * self.df * i for i in range(self.N)]
        is_stop = round(50 / (np.pi * self.df)) + 1
        self.H = [abs(self.calculate_H(w)) for w in self.sequence[1:]]
        result = self.calculate_H(35)

        self.draw_amplitude(is_stop)
        self.draw_amplitude_frequency_response(is_stop)

        print(abs(result))

circuit_analyzer = CircuitAnalyzer()
circuit_analyzer.analyze_circuit()
