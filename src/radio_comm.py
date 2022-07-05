import settings
from rpi_rf import RFDevice

# send the terminator
def send_terminator():
    rf = RFDevice(settings.pin_transmitter)
    rf.enable_tx()
    rf.tx_repeat = 10
    rf.tx_code(settings.rf_terminator, 1, 350, 24)
    rf.cleanup()
    print("Done!")

send_terminator()
