import settings
from rpi_rf import RFDevice
import flight_control
import time


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

# start receiving
def start_receiving():

    # setting up variables that will be used for radio receiving
    rec = RFDevice(settings.gpio_receiver)
    rec.enable_rx()
    ts = None

    # buffer to wait for the termination after each
    last_code = None


    while flight_control.KILL == False:
        if rec.rx_code_timestamp != ts:
            ts = rec.rx_code_timestamp

            if rec.rx_code == settings.rc_terminator:
                if last_code != None:
                    if last_code == settings.rc_focus_all:
                        print("Focus set to all")
                    elif last_code == settings.rc_focus_fl:
                        print("Focus set to front left")
                    else:
                        print("Code '" + str(last_code) + "' not understood.")
                last_code = None # set last code to nothing
            else: #if we received something but it is not the terminator, store it for the future
                last_code = rec.rx_code
        time.sleep(0.05)
    rec.cleanup()
