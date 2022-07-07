from enum import IntEnum
import settings
from rpi_rf import RFDevice
import flight_control
import time
import event_logging
import flight_controller
import fc_codes


# sends a code and then follows it with the terminator
def send_code(code:int):

    # Settings to use:
    setting_repeat = 10 #default is 10
    setting_pulselength = 350 #default is 350
    setting_length = 24 #default is 24
    setting_protocol = 1 #default is 1


    rf = RFDevice(settings.gpio_transmitter)
    rf.enable_tx()
    rf.tx_repeat = setting_repeat

    # send the code
    rf.tx_code(code, setting_protocol, setting_pulselength, setting_length)

    # send the terminator
    rf.tx_code(settings.rc_terminator, setting_protocol, setting_pulselength, setting_length)

    rf.cleanup()













class RadioOperatorFocus(IntEnum):
    BackwardForward = 0,
    LeftRight = 1,
    MeanPower = 2


# start receiving
def start_receiving():

    # setting up variables that will be used for radio receiving
    rec = RFDevice(settings.gpio_receiver)
    rec.enable_rx()
    ts = None

    # buffer to wait for the termination after each
    last_code = None

    #continuous variables
    focus = RadioOperatorFocus.BackwardForward
    val_backwardforward = 0
    val_leftright = 0
    val_meanpower = 0


    while flight_control.KILL == False:
        if rec.rx_code_timestamp != ts:
            ts = rec.rx_code_timestamp

            if rec.rx_code == settings.rc_terminator:
                if last_code != None:

                    

                    # Changing focus
                    if last_code == settings.rc_focus_backwardforward:
                        focus = RadioOperatorFocus.BackwardForward
                    elif last_code == settings.rc_focus_leftright:
                        focus = RadioOperatorFocus.LeftRight
                    elif last_code == settings.rc_focus_meanpower:
                        focus = RadioOperatorFocus.MeanPower

                    
                    # system-level
                    elif last_code == settings.rc_fc_exec:
                        try:
                            flight_controller.set_mean_power(val_meanpower) #set mean power 
                            flight_controller.set_direction(val_backwardforward, val_leftright) # set direction
                            flight_controller.execute() #execute
                            event_logging.log("radio", "executed flight scheme")
                        finally:
                            event_logging.log("radio", "execution of flight scheme FAILED")


                    # Setting a value
                    elif str(last_code)[0:len(str(settings.rc_pos_value_prefix))] == str(settings.rc_pos_value_prefix):
                        val = int(str(last_code)[len(str(settings.rc_pos_value_prefix)):999])
                        if focus == RadioOperatorFocus.BackwardForward:
                            val_backwardforward = val
                            event_logging.log("radio", "backwardforward set to " + str(val))
                        elif focus == RadioOperatorFocus.LeftRight:
                            val_leftright = val
                            event_logging.log("radio", "leftright set to " + str(val))
                        elif focus == RadioOperatorFocus.MeanPower:
                            val_meanpower = val
                            event_logging.log("radio", "meanpower set to " + str(val))
                    elif str(last_code)[0:len(str(settings.rc_neg_value_prefix))] == str(settings.rc_neg_value_prefix):
                        val = int(str(last_code)[len(str(settings.rc_pos_value_prefix)):999])
                        if focus == RadioOperatorFocus.BackwardForward:
                            val_backwardforward = val * -1
                            event_logging.log("radio", "backwardforward set to " + str(val*-1))
                        elif focus == RadioOperatorFocus.LeftRight:
                            val_leftright = val * -1
                            event_logging.log("radio", "leftright set to " + str(val*-1))
                        elif focus == RadioOperatorFocus.MeanPower:
                            val_meanpower = val * -1
                            event_logging.log("radio", "meanpower set to " + str(val*-1))


                    


                last_code = None # set last code to nothing
            
            
            # distinct flight controller inputs?
            elif rec.rx_code >= settings.rc_seed and rec.rx_code <= fc_codes.input_to_code(settings.rc_seed, 100, 100, 100): #if the last code is within the range (higher than the seed, lower than the maximum value)
                inputs = fc_codes.code_to_input(settings.rc_seed, rec.rx_code)

                #Set the mean power
                flight_controller.set_mean_power(inputs[0])

                #set the direction
                flight_controller.set_direction(inputs[1], inputs[2])

                #execute
                flight_controller.execute()

                #log
                event_logging.log("radio", "Executed MP: " + str(inputs[0]) + ", BF: " + str(inputs[1]) + ", LR: " + str(inputs[2]))


            
            else: #if we received something but it is not the terminator, store it for the future
                last_code = rec.rx_code
        time.sleep(0.05)
    rec.cleanup()
