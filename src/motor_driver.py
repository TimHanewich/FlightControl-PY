from enum import IntEnum
import settings
import settings
import RPi.GPIO as GPIO

class Motor(IntEnum):
    FrontLeft = 0
    FrontRight = 1
    RearLeft = 2
    RearRight = 3

# PWM drivers
dFL = None
dFR = None
dRL = None
dRR = None

def start_motors():

    #set up the pins for output
    GPIO.setup(settings.gpio_mFL, GPIO.OUT)
    GPIO.setup(settings.gpio_mFR, GPIO.OUT)
    GPIO.setup(settings.gpio_mRL, GPIO.OUT)
    GPIO.setup(settings.gpio_mRR, GPIO.OUT)

    #establish that these are GLOBAL - meaning that INSIDE this function, we are actually refering to the global variables outside of it
    global dFL
    global dFR
    global dRL
    global dRR

    #set up the pwm driver classes
    dFL = GPIO.PWM(settings.gpio_mFL, 1000)
    dFR = GPIO.PWM(settings.gpio_mFR, 1000)
    dRL = GPIO.PWM(settings.gpio_mRL, 1000)
    dRR = GPIO.PWM(settings.gpio_mRR, 1000)

    #start the pwm
    dFL.start(0)
    dFR.start(0)
    dRL.start(0)
    dRR.start(0)


def set_motor_power(m:Motor, power:float):
    if m == Motor.FrontLeft:
        dFL.ChangeDutyCycle(power)
    elif m == Motor.FrontRight:
        dFR.ChangeDutyCycle(power)
    elif m == Motor.RearLeft:
        dRL.ChangeDutyCycle(power)
    elif m == Motor.RearRight:
        dRR.ChangeDutyCycle(power)

def stop_motors():

    #power down all
    set_motor_power(Motor.FrontLeft, 0)
    set_motor_power(Motor.FrontRight, 0)
    set_motor_power(Motor.RearLeft, 0)
    set_motor_power(Motor.RearRight, 0)

    #stop them
    dFR.stop()
    dFR.stop()
    dRL.stop()
    dRR.stop()

    #clean pins
    GPIO.cleanup(settings.gpio_mFL)
    GPIO.cleanup(settings.gpio_mFR)
    GPIO.cleanup(settings.gpio_mRL)
    GPIO.cleanup(settings.gpio_mRR)
    