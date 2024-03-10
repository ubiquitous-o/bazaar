import time 
import pigpio

pi = pigpio.pi()
pi.set_mode(2,pigpio.OUTPUT)

while True:
    print("hogehoge")
    pi.write(2, 1)
    time.sleep(1)
    pi.write(2, 0)
    time.sleep(1)