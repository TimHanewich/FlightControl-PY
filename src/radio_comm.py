from enum import IntEnum
import settings
from rpi_rf import RFDevice
import flight_control
import time
import event_logging


# sends a code and then follows it with the terminator
def send_code(code:int):
    rf = RFDevice(settings.gpio_transmitter)
    rf.enable_tx()
    rf.tx_repeat = 10

    # send the code
    rf.tx_code(code, 1, 350, 24)

    # send the terminator
    rf.tx_code(settings.rc_terminator, 1, 350, 24)

    rf.cleanup()

class RadioOperatorFocus(IntEnum):
    BackwardForward = 0,
    LeftRight = 1


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


                    # Setting a value
                    elif str(last_code)[0:len(str(settings.rc_pos_value_prefix))] == str(settings.rc_pos_value_prefix):
                        val = int(str(last_code)[len(str(settings.rc_pos_value_prefix)):999])
                        if focus == RadioOperatorFocus.BackwardForward:
                            val_backwardforward = val
                            event_logging.log("radio", "backwardforward set to " + str(val))
                        elif focus == RadioOperatorFocus.LeftRight:
                            val_leftright = val
                            event_logging.log("radio", "leftright set to " + str(val))
                    elif str(last_code)[0:len(str(settings.rc_neg_value_prefix))] == str(settings.rc_neg_value_prefix):
                        val = int(str(last_code)[len(str(settings.rc_pos_value_prefix)):999])
                        if focus == RadioOperatorFocus.BackwardForward:
                            val_backwardforward = val * -1
                            event_logging.log("radio", "backwardforward set to " + str(val*-1))
                        elif focus == RadioOperatorFocus.LeftRight:
                            val_leftright = val * -1
                            event_logging.log("radio", "leftright set to " + str(val*-1))


                last_code = None # set last code to nothing
            else: #if we received something but it is not the terminator, store it for the future
                last_code = rec.rx_code
        time.sleep(0.05)
    rec.cleanup()
