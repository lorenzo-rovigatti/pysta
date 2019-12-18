#!/usr/bin/python3

import sys
import time
import RPi.GPIO as GPIO

PINS = {
    "volt_left" : 37,
    "ground_left" : 38,
    "pwm_left" : 22,
    "volt_right" : 8,
    "ground_right" : 10,
    "pwm_right" : 12,
    "servo" : 18,
    "standby" : 40,
    "trigger" : 36,
    "echo" : 32
}

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


class Servo():
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin

        GPIO.setup(pwm_pin, GPIO.OUT)
        self.servo = GPIO.PWM(pwm_pin, 50)
        self.servo.start(2.5)
        time.sleep(0.5)
        #self.servo.stop()


    def change_duty_cycle(self, new_dc):
        self.servo.start(new_dc)
        time.sleep(0.5)
        #self.servo.stop()
        #self.servo.ChangeDutyCycle(new_dc)


class US():
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        GPIO.setup(trig_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)

    def distance(self):
        GPIO.output(self.trig_pin, False)
        time.sleep(0.01)
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        while GPIO.input(self.echo_pin) == 0:
            pass
        pulse_start = time.time()

        while GPIO.input(self.echo_pin) == 1:
            pass
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        return round(distance, 1)


class Robot():
    def __init__(self, left_motor, right_motor, servo):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.servo = servo

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
        GPIO.setup(PINS["standby"], GPIO.OUT)
        GPIO.output(PINS["standby"], GPIO.HIGH)

        US_servo = Servo(PINS["servo"])

        US_sensor = US(PINS["trigger"], PINS["echo"])
        print(US_sensor.distance())

        left_motor = Motor(PINS["volt_left"], PINS["ground_left"], PINS["pwm_left"])
        right_motor = Motor(PINS["volt_right"], PINS["ground_right"], PINS["pwm_right"])

        robot = Robot(left_motor, right_motor, US_servo)

        '''robot.forward()
        time.sleep(2)
        robot.left()
        time.sleep(2)
        robot.right()
        time.sleep(2)'''
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
