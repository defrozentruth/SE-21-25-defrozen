import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

def writeToFile(filename, signal):
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
    # Consts
    t = 3.5
    digitalSignal = np.loadtxt("signaldigit25.txt", dtype=int)

    signal = []
    for row in digitalSignal:
        signal.append(int(''.join(map(str,row)),2))

    dt = 3.5 / len(signal)

    timeLine = np.arange(0, t, dt)
    plt.plot(timeLine, signal)
    plt.suptitle("Сигнал")
    plt.show()

    singalFourier = np.fft.fft(signal)
    frequences = [(i + 1) * 2 * np.pi/t for i in range(singalFourier.size)]
    plt.plot(frequences[1:len(frequences)//2], np.abs(singalFourier[1:singalFourier.size//2]))
    plt.suptitle('Спектр до фильтра')
    plt.show()

    hAbs = [abs(filter(frequences[i],1)) for i in range(singalFourier.size)]
    plt.plot(frequences[:500], hAbs[:500])
    plt.suptitle('АЧХ')
    plt.show()

    singalFourierAfterFilter = []
    for i in range(singalFourier.size-1):
        singalFourierAfterFilter.append(singalFourier[i + 1] * hAbs[i+1])

    plt.plot(
        frequences[:len(singalFourierAfterFilter)//2],
        list(map(abs,singalFourierAfterFilter))[:len(singalFourierAfterFilter)//2]
    )
    plt.suptitle("Спектр после фильтра")
    plt.show()

    signalAfterFilter = np.fft.ifft(singalFourierAfterFilter)
    signalAfterFilter = [signalAfterFilter[i].real for i in range(signalAfterFilter.size)]
    plt.plot(timeLine[1:], signalAfterFilter)
    plt.suptitle('Сигнал после фильтра')
    plt.show()


    writeToFile("out.wav", signalAfterFilter)


if __name__ == '__main__':
    main()