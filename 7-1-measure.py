import RPi.GPIO as GPIO
import time
from math import ceil
from matplotlib import pyplot

#настройка GPIO на Raspberry Pi
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp = 4
troyka = 17
array =[]

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=1)
GPIO.setup(comp, GPIO.IN)

#функция, измеряющая напряжение на выходе тройка-модуля
def adc():
    _value = [0, 0, 0, 0, 0, 0, 0, 0]
    _dec_value = 0
    for i in range(8):
        _value[i] = 1
        GPIO.output(dac, _value)
        time.sleep(0.0007)
        _comp_value = GPIO.input(comp)
        if _comp_value == 0:
            _value[i] = 0
        _dec_value += _value[i] * 2 ** (7 - i)
    return _dec_value

#функция, выводящая двоичное представление числа в область светодиодов
def lights_out(value):
    leds_value = 2 ** ceil(value / 32) - 1
    GPIO.output(leds, [int(bit) for bit in bin(leds_value)[2:].zfill(8)])

#исполняемая часть эксперимента
try:
    #начало эксперимента
    print('Начало зарядки')
    t1 = time.time()

    #измерения во время заряда конденсатора
    uRC = 0
    U = 3.3
    UD = int(U / (3.3 / 256))
    GPIO.output(troyka, 1)
    while uRC < (0.80 * U):
        value = adc()
        lights_out(value)
        uRC = 3.3 / 256 * value
        array.append(uRC)
        print(value, '{:.2f}'.format(uRC), 'V')

    #измерения во время разряда конденсатора
    print('Начало разрядки')
    U = 0
    UD = int(U / (3.3 / 256))
    GPIO.output(troyka, 0)
    while uRC > (0.2 * 3.3):
        value = adc()
        lights_out(value)
        uRC = 3.3 / 256 * value
        array.append(uRC)
        print(value, '{:.2f}'.format(uRC), 'V')

    #конец эксперимента, начало вычислений
    t2 = time.time()
    
    print('Конец эксперимента, начало вычислений')
    duration = t2 - t1
    av_freq = len(array) / duration
    T = duration / len(array)
    quant_step = 256
    settings = []
    settings.append(av_freq)
    settings.append(quant_step)

    #построение графика зависимости показаний АЦП от номера измерения
    xs = [i for i in range(len(array))]
    ys = [array[i] for i in range(len(array))]
    pyplot.scatter(xs, ys)
    pyplot.title("Relationship between N and U")
    pyplot.grid()
    pyplot.show()

    #сохранение данных в файлы
    with open('data.txt', w) as data1:
        data1.write('\n'.join(str(item) for item in array))
    with open('settings.txt', w) as data2:
        data2.write('\n'.join(str(item) for item in settings))

    print(duration, T, av_freq, quant_step)
    
#окончание программы 
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
