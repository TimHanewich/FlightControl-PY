import resources
import settings
import flight_control
import time
import RPi.GPIO as GPIO
import threading
import telemetry

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
            time.sleep(2)
    
    #cleanup the GPIO that we were using
    GPIO.cleanup(settings.pin_statuslight)


# LAUNCH EACH THREAD!

# Launch status light controller (controls showing the appropriate status light on the status light indicator pin)
print("Starting status light controller...")
tslc = threading.Thread(target=status_light_controller)
tslc.start()

# Launc the MPU-6050 telemetry reader
tr = telemetry.MotionSensor()
tmpu = threading.Thread(target=tr.StartMotionSensor)
tmpu.start()



# COMMAND INTERFACE
print("Proceeding to main interface...")
while True:
    cmd = input("FC>")
    if cmd == "kill" or cmd == "exit":
        flight_control.KILL = True
        print("Killing...")

        # Wait for each thread that we started to terminate
        tslc.join()
        tmpu.join()

        break
    elif cmd == "status offline":
        flight_control.STATUS = resources.sys_status.offline
        print("Status set to offline")
    elif cmd == "status standby":
        flight_control.STATUS = resources.sys_status.standby
        print("Status set to standby")
    elif cmd == "tele":
        print("AccX: " + str(flight_control.AccX))
        print("AccY: " + str(flight_control.AccY))
        print("AccZ: " + str(flight_control.AccZ))
        print("GyroX: " + str(flight_control.GyroX))
        print("GyroY: " + str(flight_control.GyroY))
        print("GyroZ: " + str(flight_control.GyroZ))
    else:
        print("Command '" + cmd + "' not understood.")
