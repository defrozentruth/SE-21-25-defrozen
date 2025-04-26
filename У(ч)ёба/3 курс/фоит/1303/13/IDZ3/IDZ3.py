import numpy as np
import matplotlib.pyplot as plt

L1 = 13.5934758394208
L2 = 0.736428750945079
C1 = 0.0000114807684098339
C2 = 0.0000119450718128781
R1 = 104.70009686908
R2 = 32.9926577881827
R3 = 1095.36423315565
R4 = 508.587107056158
dt = 0.0196349540849362
N1 = 8192


time_values = np.arange(0, N1 * dt, dt)


signal = np.loadtxt("13.txt")


plt.figure()
plt.plot(time_values, signal, label='Сигнал')
plt.xlabel('Время')
plt.ylabel('Значение сигнала')
plt.legend()
plt.show()


Fsig = np.fft.fft(signal)
frequency_values = np.fft.fftfreq(N1, dt)

plt.figure()
FourAbs = np.abs(Fsig)
plt.plot(2 * np.pi * frequency_values, FourAbs, label='Спектр')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.legend()
plt.show()


w_values = np.linspace(0, 100, 1000)

with np.errstate(divide='ignore', invalid='ignore'):
    imp_1 = R4 + 1 / (1j * w_values * C2)
    imp_2 = 1 / (1j * w_values * C1) + R2 + 1j * w_values * L2 + R3
    imp_parall = 1 / (1 / imp_1 + 1 / imp_2)
    I_1 = 1 / (R1 + 1j * w_values * L1 + imp_parall)
    U_parall = I_1 * imp_parall
    I_2 = U_parall / imp_1
    U_out = I_2 * R4
    ACH = np.abs(U_out)

plt.figure()
plt.plot(w_values, ACH, label='АЧХ')
plt.xlabel('Частота')
plt.ylabel('Амплитуда')
plt.legend()
plt.show()

w = 30;
imp_1 = R4 + 1 / (1j * w * C2)
imp_2 = 1 / (1j * w * C1) + R2 + 1j * w * L2 + R3
imp_parall = 1 / (1 / imp_1 + 1 / imp_2)
I_1 = 1 / (R1 + 1j * w * L1 + imp_parall)
U_parall = I_1 * imp_parall
I_2 = U_parall / imp_1
U_out = I_2 * R4

res = np.abs(U_out/1);

print(res)

