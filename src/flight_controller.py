import settings
import motor_driver

MEAN_POWER = 0.0 # the mean power that the motors should center around.

def set_mean_power(value:float):
    global MEAN_POWER
    MEAN_POWER = float

# hold X + Z position (all motor power the same)
def hold():
    global MEAN_POWER
    print(MEAN_POWER)
    motor_driver.set_motor_power(motor_driver.Motor.FrontLeft, MEAN_POWER)
    motor_driver.set_motor_power(motor_driver.Motor.FrontRight, MEAN_POWER)
    motor_driver.set_motor_power(motor_driver.Motor.RearLeft, MEAN_POWER)
    motor_driver.set_motor_power(motor_driver.Motor.RearRight, MEAN_POWER)

# provide percent as a number. i.e. 0-100. Not 0.0-1.0
def forward(percent:float):
    adj = settings.slip_diff * (percent/100) #the adjustment (slip) to apply to the motors. rear motors will decrease by this amount from the mean. front motors will increase by this amount
    
    # declare var as global first
    global MEAN_POWER
    
    #set Rears
    motor_driver.set_motor_power(motor_driver.Motor.RearLeft, MEAN_POWER - adj)
    motor_driver.set_motor_power(motor_driver.Motor.RearRight, MEAN_POWER - adj)

    # set fronts
    motor_driver.set_motor_power(motor_driver.Motor.FrontLeft, MEAN_POWER + adj)
    motor_driver.set_motor_power(motor_driver.Motor.FrontRight, MEAN_POWER + adj)



