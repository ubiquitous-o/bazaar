import pigpio
import time
import sys

class ServoMotor:
    def __init__(self, pin=23, min_angle=0, max_angle=270, ini_angle=270/2):
        self.pin = pin
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.angle = 0
        self.ini_angle = ini_angle
        self.pi = None

    def init(self):
        print("init servo")
        self.pi = pigpio.pi()
        self.pi.set_mode(self.pin, pigpio.OUTPUT)
        self.set_initial_angle()

    def stop(self):
        print("stop servo")
        self.pi.set_mode(self.pin, pigpio.INPUT)
        self.pi.stop()

    def set_angle(self, target_angle):
        target_angle = float(target_angle)
        print(target_angle)
        if target_angle < self.min_angle or target_angle > self.max_angle:
            print("unusable angle")
            return

        pulse_width = (target_angle / 270) * (2500 - 500) + 500
        print("pulse_width" + str(pulse_width))
        self.angle = target_angle
        self.pi.set_servo_pulsewidth(self.pin, pulse_width)
        # time.sleep(1)

    def set_initial_angle(self):
        self.set_angle(self.ini_angle)
