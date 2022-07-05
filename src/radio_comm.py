import settings
from rpi_rf import RFDevice


def send_code(code:int):
    rf = RFDevice(settings.gpio_transmitter)
    rf.enable_tx()
    rf.tx_repeat = 10

    # send the code
    rf.tx_code(code, 1, 350, 24)

    # send the terminator
    rf.tx_code(settings.rf_terminator, 1, 350, 24)

    rf.cleanup()
    print("Done!")

