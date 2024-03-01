import pigpio
import time
import sys

class ServoMotor:
    def __init__(self, pin=18, min_angle=0, max_angle=270, ini_angle=90):
        self.pin = pin
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.angle = 0
        self.ini_angle = ini_angle
        self.pi = None

    def start(self):
        self.pi = pigpio.pi()
        self.pi.set_mode(self.pin, pigpio.OUTPUT)

    def stop(self):
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
        time.sleep(1)

    def set_ini_angle(self):
        self.set_angle(self.ini_angle)

if __name__ == "__main__":
    args = sys.argv

    servo_motor_vertical = ServoMotor(pin=18, max_angle=270, min_angle=0, ini_angle=90)

    servo_motor_vertical.start()

    servo_motor_vertical.set_angle(int(args[1]))

#    servo_motor_vertical.set_angle(40)
#    for angle in range(180, -1, -10):
#        servo_motor_horizontal.set_angle(angle)


    servo_motor_vertical.set_ini_angle()

    print("now"+str(servo_motor_vertical.angle))

    servo_motor_vertical.stop()
