#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class Motor:
    def __init__(self, forward_pin, reverse_pin, pwm_pin):
        self.forward_pin = forward_pin
        self.reverse_pin = reverse_pin
        self.pwm_pin = pwm_pin

        for pin in (forward_pin, reverse_pin, pwm_pin):
            GPIO.setup(pin, GPIO.OUT)

    def forward(self):
        GPIO.output(self.forward_pin, GPIO.HIGH)
        GPIO.output(self.reverse_pin, GPIO.LOW)
        GPIO.output(self.pwm_pin, GPIO.HIGH)

    def reverse(self):
        GPIO.output(self.forward_pin, GPIO.LOW)
        GPIO.output(self.reverse_pin, GPIO.HIGH)
        GPIO.output(self.pwm_pin, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.forward_pin, GPIO.LOW)
        GPIO.output(self.reverse_pin, GPIO.LOW)
        GPIO.output(self.pwm_pin, GPIO.LOW)


class Robot():
    def __init__(self, left_motor, right_motor):
        self.left_motor = left_motor
        self.right_motor = right_motor

    def forward(self):
        self.left_motor.forward()
        self.right_motor.forward()

    def reverse(self):
        self.left_motor.reverse()
        self.right_motor.reverse()

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def left(self):
        self.left_motor.reverse()
        self.right_motor.forward()

    def right(self):
        self.left_motor.forward()
        self.right_motor.reverse()


def main():
    try:
        # standby pin
        GPIO.setup(40, GPIO.OUT)
        GPIO.output(40, GPIO.HIGH)

        left_motor = Motor(16, 18, 22)
        right_motor = Motor(8, 10, 12)

        robot = Robot(left_motor, right_motor)

        robot.forward()
        time.sleep(2)
        robot.left()
        time.sleep(2)
        robot.right()
        time.sleep(2)
    except:
        pass
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()

