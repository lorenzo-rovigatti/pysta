#!/usr/bin/python3

import time

try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    from mock_RPi_GPIO import GPIO

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


class Ultrasonic_sensor():
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
    def __init__(self, left_motor, right_motor, servo, us_sensor):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.servo = servo
        self.us_sensor = us_sensor

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
        
    def distance(self):
        return self.us_sensor.distance()
