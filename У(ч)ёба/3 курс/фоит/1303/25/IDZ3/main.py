import numpy as np
import matplotlib.pyplot as plt


# Consts
def L1():
    return 12.9613676535114


def L2():
    return 0.496169770763215


def C1():
    return 1.15709335234433E-05


def C2():
    return 1.16514071253152E-05


def R1():
    return 100.244891037914


def R2():
    return 37.7326519768152	


def R3():
    return 1067.73817189554


def R4():
    return 536.657874938589


def N():
    return 8192


def dt():
    return 0.0196349540849362


# Functions
def capacitor(omega, C):
    cap = (1j * omega * C)
    if cap == 0:
        return np.inf
    return 1 / cap


def inductor(omega, L):
    return 1j * omega * L


def leftBranch(omega):
    return capacitor(omega, C1()) + R2() + inductor(omega, L2()) + R3()


def rightBranch(omega):
    return R4() + capacitor(omega, C2())


def parallel(omega):
    divisor = 1/leftBranch(omega) + 1/rightBranch(omega)
    if divisor == 0:
        return np.inf
    return 1 / divisor


def findCircuitI(omega, Uin):
    return Uin / (R1() + inductor(omega, L1()) + parallel(omega))
  

def findUparallel(omega, Uin):
    return findCircuitI(omega, Uin) * parallel(omega)


def findInRightBranchI(omega, Uin):
    return findUparallel(omega, Uin) / rightBranch(omega)


def Uout(omega, Uin):
    return findInRightBranchI(omega, Uin) * R4()


def result(omega, Uin):
    return Uout(omega, Uin) / Uin

def main():
    t = N() * dt()
    omega = np.linspace(0, 100, 1000)
    h = [np.abs(result(omg, 1)) for omg in omega]
    plt.plot(omega, h)
    plt.suptitle('АЧХ')
    plt.show()

    signal = np.loadtxt('25.txt')
    plt.plot(np.arange(0, t, dt()), signal)
    plt.suptitle('Сигнал')
    plt.show()


    singalFourier = np.fft.fft(signal)
    df = 1/t

    plt.plot(2 * np.pi * df * np.arange(N()//2), np.abs(singalFourier[:singalFourier.size//2]) * 2 / singalFourier.size)
    plt.suptitle('Спектр')
    plt.show()

    print(np.abs(result(40, 1)))
    return


if __name__ == '__main__':
    main()