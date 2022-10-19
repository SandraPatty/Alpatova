import RPi.GPIO as GPIO
import time
from math import ceil
from matplotlib import pyplot

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

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

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

try:
    t1 = time.time()
    uRC = 0
    U = 3.3
    UD = int(U / (3.3 / 256))
    GPIO.output(troyka, 1)
    while uRC < (0.80 * U):
        value = adc()
        leds_value = 2 ** ceil(value / 32) - 1
        GPIO.output(leds, dec2bin(leds_value))
        uRC = 3.3 / 256 * value
        array.append(uRC)
        print(value, '{:.2f}'.format(uRC), 'V', leds_value)
    U = 0
    UD = int(U / (3.3 / 256))
    GPIO.output(troyka, 0)
    while uRC > (0.2 * 3.3):
        value = adc()
        leds_value = 2 ** ceil(value / 32) - 1
        GPIO.output(leds, dec2bin(leds_value))
        uRC = 3.3 / 256 * value
        array.append(uRC)
        print(value, '{:.2f}'.format(uRC), 'V', leds_value)
    t2 = time.time()
    duration = t2 - t1
    xs = [i for i in range(len(array))]
    ys = [array[i] for i in range(len(array))]
    pyplot.scatter(xs, ys)
    pyplot.title("Relationship between N and U")
    pyplot.grid()
    pyplot.show()
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
