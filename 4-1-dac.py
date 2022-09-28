import RPi.GPIO as GPIO
from time import sleep


dac = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)

GPIO.setup(dac, GPIO.OUT)

def decimal2binary(value):
 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

try:

    a = input("Введите число от 0 до 255: ")
    if a == "q":
        raise KeyboardInterrupt
    if int(a) < 0 or int(a) > 255:
        raise ValueError

    a = int(a)
    GPIO.output(dac, decimal2binary(a))
    U = a * 3.3 / 256
    print (f'Предполагаемое напряжение на ЦАП {"{:.2f}".format(U)} Вольт')
    sleep(5)
    

except ValueError or ArithmeticError:
    print("Неправильный ввод")
except KeyboardInterrupt:
    print("Программа остановлена")
    
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()