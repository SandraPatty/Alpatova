import RPi.GPIO as GPIO
from time import sleep


dac = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)

def dec2bin(value):
 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

try:
    T = float(input())
    c = T / 512
    while True:
        for i in range(0, 256):
            a = i
            GPIO.output(dac, dec2bin(a))
            sleep(c)
        for i in range(255, -1, -1):
            a = i
            GPIO.output(dac, dec2bin(a))
            sleep(c)
        
            
except KeyboardInterrupt:
    print("Программа остановлена")
    
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()