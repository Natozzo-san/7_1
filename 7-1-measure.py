import RPi.GPIO as gpio
import matplotlib.pyplot as plt
import time
from time import sleep


gpio.setmode(gpio.BCM)
dac=[26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
comp=4
troyka=17
gpio.setup(dac, gpio.OUT, initial=gpio.HIGH)
gpio.setup(leds, gpio.OUT)
gpio.setup(troyka,gpio.OUT, initial=gpio.HIGH)
gpio.setup(comp, gpio.IN)
count = 0

#
def perev(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]
#
def adc():
    k=0
    for i in range(7, -1, -1):
        k+=2**i
        gpio.output(dac, perev(k))
        sleep(0.005)
        if gpio.input(comp)==0:
            k-=2**i
    return k


res_of_u = []
time_begin = time.time()
tim = []
utr = 0

try:
    #зарядка
    while utr < 256*0.90:
        utr = adc()
        res_of_u.append(utr/256*3.3)
        tim.append(time.time()-time_begin)
        gpio.output(leds, perev(utr))
        count +=1
        print(utr,' ')
    gpio.setup(troyka, gpio.OUT, initial = gpio.LOW)
    #разрядка
    while utr > 256*(1-0.9):
        utr = adc()
        res_of_u.append(utr/256*3.3)
        tim.append(time.time()-time_begin)
        gpio.output(leds, perev(utr))
        count +=1
        print(utr,' ')
    gpio.setup(troyka, gpio.OUT, initial=gpio.LOW)

    plt.plot(tim,value)
    plt.xlabel('time')
    plt.ylabel('напряжение')
    plt.show()

    timeF = time.time()
    tiMe = abs(timeF - time_begin)
    print(len(tim)/(time.time()-time_begin))
    print(3.3/256)
    
        
finally:
    with open("data.txt", "w") as outfile:
        for i in res_of_u:
            outfile.write(str(i) + '\n')
    with open("setting.txt", "w") as outfile:
        outfile.write(str(1/10/count) + '\n')
    #gpio.output(dac, 0)
    gpio.setup(dac, gpio.OUT, initial=gpio.LOW)
    gpio.cleanup()

    