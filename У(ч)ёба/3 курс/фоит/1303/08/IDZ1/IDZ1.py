import matplotlib

import numpy as np
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

class OpticalFiber:
    def __init__(self, R, N2, OMEGA, Y0, ALPHA, HOP=0.1):
        self.R = R
        self.N2 = N2
        self.OMEGA = OMEGA
        self.Y0 = Y0
        self.ALPHA = ALPHA
        self.HOP = HOP

        self.currentY = self.Y0
        self.currentZ = 0
        self.currentSin, self.direction = self.getStartSin()
        self.currentN = self.f1(self.currentY)
        self.totalLength = 0

        self.pointsByY = []
        self.pointsByZ = []

    def f1(self, y):
        return 1.3 - 0.12 * np.cos(3 * y)

    def getStartSin(self):
        n1_0 = self.f1(self.Y0)
        sinBeta = np.sin(np.pi / 2 - abs(self.ALPHA) * self.N2 / n1_0)
        return sinBeta, np.sign(self.ALPHA)

    def makeStep(self):
        newY = self.currentY + np.sqrt(1 - self.currentSin ** 2) * self.HOP * self.direction
        newZ = self.currentZ + np.abs(self.currentSin) * self.HOP
        newN = self.f1(newY) if self.R >= abs(newY) else self.N2
        newSin = (self.currentSin * self.currentN) / newN

        self.totalLength += self.HOP
        self.currentY = newY
        self.currentZ = newZ

        if abs(newSin) >= 1:
            self.direction *= -1
            return

        self.currentN = newN
        self.currentSin = newSin

    def start(self):
        while self.currentZ < self.zf(self.currentY):
            self.pointsByY.append(self.currentY)
            self.pointsByZ.append(self.currentZ)
            self.makeStep()

        result_length = self.totalLength
        with open('IDZ1.txt', 'w') as f:
            f.write(f'{result_length}')

        t1 = np.arange(-self.R, self.R, 0.001)
        fig, ax = plt.subplots(figsize=(5, 2.5))
        plt.subplots_adjust(top=0.5)
        ax.plot(self.pointsByZ, self.pointsByY, 'r', self.zf(t1), t1, 'b', [0, 22], [self.R, self.R], 'b', [0, 22],
                [-self.R, -self.R], 'b')
        plt.savefig('IDZ1.png', dpi=100)
        plt.show()

    def zf(self, y):
        return 18 + 3 * np.sin(17.951958020513104 * y)


def main():
    R = 0.8
    N2 = 1
    OMEGA = 3 * 10 ** 14
    Y0 = -0.3
    ALPHA = np.deg2rad(-20)
    HOP = 0.01

    fiber = OpticalFiber(R, N2, OMEGA, Y0, ALPHA, HOP)
    fiber.start()


if __name__ == '__main__':
    main()
