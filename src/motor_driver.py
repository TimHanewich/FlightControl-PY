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
    GPIO.setup(settings.pin_mFL, GPIO.OUT)
    GPIO.setup(settings.pin_mFR, GPIO.OUT)
    GPIO.setup(settings.pin_mRL, GPIO.OUT)
    GPIO.setup(settings.pin_mRR, GPIO.OUT)

    #set up the pwm driver classes
    dFL = GPIO.PWM(settings.pin_mFL, 1000)
    dFR = GPIO.PWM(settings.pin_mFR, 1000)
    dRL = GPIO.PWM(settings.pin_mRL, 1000)
    dRR = GPIO.PWM(settings.pin_mRR, 1000)

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
    GPIO.cleanup(settings.pin_mFL)
    GPIO.cleanup(settings.pin_mFR)
    GPIO.cleanup(settings.pin_mRL)
    GPIO.cleanup(settings.pin_mRR)
    