import RPi.GPIO as GPIO
from time import sleep

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17


GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial=1)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    array = [0]*8
    dec = 0
    for i in range(8):
        array[i] = 1
        GPIO.output(dac, array)
        sleep(0.0007)
        c = GPIO.input(comp)
        if c == 0:
            array[i] = 0
        dec += array[i]*2**(8 - i - 1)
    return dec

try:
    while True:
        value = adc()
        volt = 3.3 / 256 * value
        print('{:.2f}'.format(volt), 'V', value)

    
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()