import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


def write_file(filename, signal):
    write(filename, 44100, np.array(signal).astype(np.float32))


def filter(omega, Uin):
    R = 5000
    C = 0.000001

    def capacitor(omega, C):
        cap = (1j * omega * C)
        if cap == 0:
            return np.inf
        return 1 / cap

    return (Uin * capacitor(omega, C)) / (R + capacitor(omega, C))


def main():
    t = 3.5
    digitalSignal = np.loadtxt("signaldigit9.txt", dtype=int)
    signal = []

    for row in digitalSignal:
        signal.append(int(''.join(map(str, row)), 2))

    dt = 3.5 / len(signal)

    timeLine = np.arange(0, t, dt)
    plt.plot(timeLine, signal)
    plt.suptitle("Сигнал")
    plt.show()

    signalFourier = np.fft.fft(signal)
    frequencies = [(i + 1) * 2 * np.pi / t for i in range(signalFourier.size)]
    plt.plot(frequencies[1:len(frequencies) // 2], np.abs(signalFourier[1:signalFourier.size // 2]))
    plt.suptitle('Исходный спектр')
    plt.show()

    hAbs = [abs(filter(frequencies[i], 1)) for i in range(signalFourier.size)]
    plt.plot(frequencies[:500], hAbs[:500])
    plt.suptitle('АЧХ')
    plt.show()

    singalFourierFiltered = []
    for i in range(signalFourier.size - 1):
        singalFourierFiltered.append(signalFourier[i + 1] * hAbs[i + 1])

    plt.plot(
        frequencies[:len(singalFourierFiltered) // 2],
        list(map(abs, singalFourierFiltered))[:len(singalFourierFiltered) // 2]
    )
    plt.suptitle("Спектр через фильтр")
    plt.show()

    filteredSignal = np.fft.ifft(singalFourierFiltered)
    filteredSignal = [filteredSignal[i].real for i in range(filteredSignal.size)]
    plt.plot(timeLine[1:], filteredSignal)
    plt.suptitle('Сигнал через фильтр')
    plt.show()

    write_file("filtered_signal.wav", filteredSignal)


if __name__ == '__main__':
    main()
