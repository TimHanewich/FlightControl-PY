import resources
import settings
import flight_control
import time
import RPi.GPIO as GPIO
import threading

# Set up
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#start the status light indicator
def status_light_controller():
    GPIO.setup(settings.pin_statuslight, GPIO.OUT)
    while flight_control.KILL == False:
        if flight_control.STATUS == resources.sys_status.offline:
            GPIO.output(settings.pin_statuslight, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(settings.pin_statuslight, GPIO.LOW)
            time.sleep(1)
        elif flight_control.STATUS == resources.sys_status.standby:
            GPIO.output(settings.pin_statuslight, GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(settings.pin_statuslight, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(settings.pin_statuslight, GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(settings.pin_statuslight, GPIO.LOW)
            time.sleep(0.05)
            time.sleep(2.5)
print("Starting status light controller...")
tslc = threading.Thread(target=status_light_controller)
tslc.start()



# COMMAND INTERFACE
print("Proceeding to main interface...")
while True:
    cmd = input("FC>")
    if cmd == "kill":
        flight_control.KILL = True
        print("Killing...")
        tslc.join()
        break
    elif cmd == "status offline":
        flight_control.STATUS = resources.sys_status.offline
        print("Status set to offline")
    elif cmd == "status standby":
        flight_control.STATUS = resources.sys_status.standby
        print("Status set to standby")
    else:
        print("Command '" + cmd + "' not understood.")
