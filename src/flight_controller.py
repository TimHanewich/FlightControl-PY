from turtle import left
import settings
import motor_driver
import math

MEAN_POWER = 0.0 # the mean power that the motors should center around.

def set_mean_power(value:float):
    global MEAN_POWER
    MEAN_POWER = value

# hold X + Z position (all motor power the same)
def hold():
    global MEAN_POWER
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
    motor_driver.set_motor_power(motor_driver.Motor.RearLeft, MEAN_POWER + adj)
    motor_driver.set_motor_power(motor_driver.Motor.RearRight, MEAN_POWER + adj)

    # set fronts
    motor_driver.set_motor_power(motor_driver.Motor.FrontLeft, MEAN_POWER - adj)
    motor_driver.set_motor_power(motor_driver.Motor.FrontRight, MEAN_POWER - adj)

# input can range from -100.0 to 100.0 (-100 would be full throttle backward. 100 would be full throttle forward)
def set_direction(backward_forward:float, left_right:float):

    # check the input
    if backward_forward > 100.0 or backward_forward < -100.0:
        raise ValueError("backward_forward input was greater than 100.0 or less than 100.0")
    if left_right > 100.0 or left_right < -100.0:
        raise ValueError("left_right input was greater than 100.0 or less than 100.0")

    # set globals
    global MEAN_POWER

    # calculate standard adjustments
    backward_forward_adj = settings.slip_diff * ((backward_forward/100)/2)
    left_right_adj = settings.slip_diff * ((left_right/100)/2)

    #calculate motor speed
    power_FL = MEAN_POWER - backward_forward_adj + left_right_adj
    power_FR = MEAN_POWER - backward_forward_adj - left_right_adj
    power_RL = MEAN_POWER + backward_forward_adj + left_right_adj
    power_RR = MEAN_POWER + backward_forward_adj - left_right_adj

    # ensure none are below 0.0
    power_FL = max(power_FL, 0.0)
    power_FR = max(power_FR, 0.0)
    power_RL = max(power_RL, 0.0)
    power_RR = max(power_RR, 0.0)

    #ensure none are above 100.0
    power_FL = min(power_FL, 100.0)
    power_FR = min(power_FR, 100.0)
    power_RL = min(power_RL, 100.0)
    power_RR = min(power_RR, 100.0)

    #set the power
    motor_driver.set_motor_power(motor_driver.Motor.FrontLeft, power_FL)
    motor_driver.set_motor_power(motor_driver.Motor.FrontRight, power_FR)
    motor_driver.set_motor_power(motor_driver.Motor.RearLeft, power_RL)
    motor_driver.set_motor_power(motor_driver.Motor.RearRight, power_RR)


