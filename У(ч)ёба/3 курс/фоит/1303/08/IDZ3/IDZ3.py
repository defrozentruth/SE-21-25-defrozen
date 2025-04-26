import numpy as np
import matplotlib.pyplot as pyplot


# Функция расчета коэффициента передачи цепи
def search_res(frequency, voltage_in):
    # Вычисляем отношение выходного напряжения к входному
    return voltage_out(frequency, voltage_in) / voltage_in


# Функция для расчета выходного напряжения
def voltage_out(frequency, voltage_in):
    # Выходное напряжение равно произведению тока на сопротивление R2
    return amperage(frequency, voltage_in) * R2


# Функция для расчета тока в цепи
def amperage(frequency, voltage_in):
    # Ток равен напряжению на импедансе Z2
    return voltage(frequency, voltage_in) / second_imp(frequency)


# Функция для расчета напряжения на цепи
def voltage(frequency, voltage_in):
    # Напряжение равно произведению входного тока на полный импеданс
    return general_amperage(frequency, voltage_in) * general_imp(frequency)


# Функция для расчета входного тока
def general_amperage(frequency, voltage_in):
    # Входной ток равен входному напряжению деленному на сумму сопротивлений и импедансов
    return voltage_in / (R1 + 1j * frequency * L1 + general_imp(frequency))


# Функция для расчета полного импеданса цепи
def general_imp(frequency):
    # Полный импеданс равен сумме импедансов Z1 и Z2
    return 1 / (1 / first_imp(frequency) + 1 / second_imp(frequency))


# Функция для расчета импеданса Z1
def first_imp(frequency):
    return R4 + 1 / (1j * frequency * C2)


# Функция для расчета импеданса Z2
def second_imp(frequency):
    return 1 / (1j * frequency * C1) + R2 + 1j * frequency * L2 + R3


# Катушки индуктивности, Гн
L1 = 12.7537816086948
L2 = 0.550365044426687

# Конденсаторы, Ф
C1 = 0.0000116269809712528
C2 = 0.0000149842214124653

# Резисторы, Ом
R1 = 110.283405269895
R2 = 31.2175753863943
R3 = 1040.17866945978
R4 = 535.999521945388

N1 = 8192  # Кол-во отсчетов N (элементов массива)

# Время между соседними отсчетами (δt), с
dt = 0.0196349540849362

t = dt * N1


def set_labels_and_show(x_label, y_label):
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)
    pyplot.legend()
    pyplot.show()


# Построение графика АЧХ
w_values = np.linspace(0, 100, 1000)
pyplot.plot(w_values, np.abs(search_res(w_values, 10)), label='АЧХ')
set_labels_and_show('Частота', 'Амплитуда')

# Загрузка и отображение входного сигнала
signal = np.loadtxt("./8.txt")
time_values = np.arange(0, N1 * dt, dt)
pyplot.plot(time_values, signal, label='Сигнал')
set_labels_and_show('Время', 'Значение сигнала')

# Преобразование Фурье и отображение спектра
transformed_signal = np.fft.fft(signal)
frequency_values = np.fft.fftfreq(N1, dt)
amplitudes = np.abs(transformed_signal)
pyplot.plot(2 * np.pi * frequency_values, amplitudes, label='Спектр')
set_labels_and_show('Частота', 'Амплитуда')

# Анализ гармоники на частоте 10 Гц
freq_harmonic_3 = 20
print(np.abs(search_res(freq_harmonic_3, 10)))
