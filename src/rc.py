# RADIO CONTROLLER - meant to be used as standalone

import radio_comm
import xbox
import time
import math
import fc_codes
import settings


joy = xbox.Joystick()

while not joy.Back():

    try:
        # Start a MEAN_POWER value that will be changed and recycled
        MEAN_POWER = 0

        # get backward forward value
        left_y = joy.leftY()
        bf = round(left_y * 100)
        if bf > 100:
            bf = 100
        elif bf < -100:
            bf = -100

        # get left right value
        left_x = joy.leftX()
        lr = round(left_x * 100)
        if lr > 100:
            lr = 100
        elif lr < -100:
            lr = -100

        # increment mean power?
        if joy.A() == 1:
            MEAN_POWER = MEAN_POWER + 1
        
        # decrement mean power?
        if joy.B() == 1:
            MEAN_POWER = MEAN_POWER - 1

        # calculate the code for this 
        CODE = fc_codes.input_to_code(settings.rc_seed, MEAN_POWER, bf, lr)

        # transmit
        print("Transmitting: MP(" + str(MEAN_POWER) + ") BF(" + str(bf) + ") LR(" + str(lr) + ") = " + str(CODE))
        radio_comm.send_code(CODE, False)

        #wait
        print("Success! Waiting... ")
        time.sleep(0.1)
    except:
        joy.close()
        print("That failed! Joystick closed.")


joy.close()
print("Complete! Joystick closed.")


    
