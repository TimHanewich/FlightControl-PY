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
    rf.tx_code(settings.rf_terminator, 1, 350, 24)

    rf.cleanup()

# start receiving
def start_receiving():
    rec = RFDevice(settings.gpio_receiver)
    rec.enable_rx()
    ts = None
    while flight_control.KILL == False:
        if rec.rx_code_timestamp != ts:
            ts = rec.rx_code_timestamp
            print("Code received: " + str(rec.rx_code))
        time.sleep(0.05)
    rec.cleanup()

flight_control.KILL = False
print("Listening...")
start_receiving()
print("Done!")

