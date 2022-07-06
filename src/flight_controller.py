import settings
import motor_driver
import math

# Flight control variables
MEAN_POWER = 0.0 # the mean power that the motors should center around.
BACKWARD_FORWARD = 0.0
LEFT_RIGHT = 0.0

def set_mean_power(value:float):
    global MEAN_POWER
    MEAN_POWER = value


# input can range from -100.0 to 100.0 (-100 would be full throttle backward. 100 would be full throttle forward)
def set_direction(backward_forward:float, left_right:float):

    # check the input
    if backward_forward > 100.0 or backward_forward < -100.0:
        raise ValueError("backward_forward input was greater than 100.0 or less than 100.0")
    if left_right > 100.0 or left_right < -100.0:
        raise ValueError("left_right input was greater than 100.0 or less than 100.0")

    # set globals
    global MEAN_POWER
    global BACKWARD_FORWARD
    global LEFT_RIGHT

    # set the values
    BACKWARD_FORWARD = backward_forward
    LEFT_RIGHT = left_right



# executes the values that were saved
def execute():

    # set globals
    global MEAN_POWER
    global BACKWARD_FORWARD
    global LEFT_RIGHT

    # calculate standard adjustments
    backward_forward_adj = settings.slip_diff * ((BACKWARD_FORWARD/100)/2)
    left_right_adj = settings.slip_diff * ((LEFT_RIGHT/100)/2)

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
