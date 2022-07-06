import resources
import settings
import flight_control
import time
import RPi.GPIO as GPIO
import threading
import telemetry
import motor_driver
from motor_driver import Motor, set_motor_power
import flight_controller
import radio_comm
import event_logging

# Set up
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#start the status light indicator
def status_light_controller():
    GPIO.setup(settings.gpio_statuslight, GPIO.OUT)
    while flight_control.KILL == False:
        if flight_control.STATUS == resources.sys_status.offline:
            GPIO.output(settings.gpio_statuslight, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(settings.gpio_statuslight, GPIO.LOW)
            time.sleep(1)
        elif flight_control.STATUS == resources.sys_status.standby:
            GPIO.output(settings.gpio_statuslight, GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(settings.gpio_statuslight, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(settings.gpio_statuslight, GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(settings.gpio_statuslight, GPIO.LOW)
            time.sleep(0.05)
            time.sleep(2)
    
    #cleanup the GPIO that we were using
    GPIO.cleanup(settings.gpio_statuslight)




# LAUNCH EACH THREAD/ACTIVITY!


# start the motor drivers
if settings.enable_quadcopter:
    motor_driver.start_motors()

# Launch status light controller (controls showing the appropriate status light on the status light indicator pin)
if settings.enable_statuslight:
    print("Starting status light controller...")
    tslc = threading.Thread(target=status_light_controller)
    tslc.start()

# Launc the MPU-6050 telemetry reader
if settings.enable_mpu6050:
    print("Launching MPU-6050 telemetry reader...")
    tr = telemetry.MotionSensor()
    tmpu = threading.Thread(target=tr.StartMotionSensor)
    tmpu.start()

# Launch the motion light controller
if settings.enable_motionlight:
    print("Launching motion light controller...")
    tmlc = threading.Thread(target=tr.StartMotionLight)
    tmlc.start()

# Launch the radio receiver
if settings.enable_radio:
    print("Launching radio receiver...")
    radt = threading.Thread(target=radio_comm.start_receiving)
    radt.start()


# COMMAND INTERFACE
print("Proceeding to main interface...")
while True:
    cmd = input("FC>")
    if cmd == "kill" or cmd == "exit":
        flight_control.KILL = True
        print("Killing...")

        # stop the motors
        motor_driver.stop_motors()

        # Wait for each thread that we started to terminate
        if settings.enable_statuslight:
            tslc.join()
        if settings.enable_mpu6050:
            tmpu.join()
        if settings.enable_motionlight:
            tmlc.join()
        if settings.enable_radio:
            radt.join()

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
    elif cmd == "idle":
        motor_driver.set_motor_power(Motor.FrontLeft, 5)
        motor_driver.set_motor_power(Motor.FrontRight, 5)
        motor_driver.set_motor_power(Motor.RearLeft, 5)
        motor_driver.set_motor_power(Motor.RearRight, 5)
        print("Idling at 5% power across all four motors")
    elif len(cmd) >= 2 and cmd[0:2] == "mp": #short for "motor power". i.e. "mp 50" powers all 4 motors to 50%
        parts = cmd.split(" ")
        if len(parts) == 2:
            numf = float(parts[1])
            motor_driver.set_motor_power(Motor.FrontLeft, numf)
            motor_driver.set_motor_power(Motor.FrontRight, numf)
            motor_driver.set_motor_power(Motor.RearLeft, numf)
            motor_driver.set_motor_power(Motor.RearRight, numf)
            print("All 4 motor power now set to " + str(numf) + "% power")
        elif len(parts) == 3:
            try:
                num = float(parts[2])
                if parts[1] == "fl":
                    motor_driver.set_motor_power(Motor.FrontLeft, num)
                    print("Front Left motor set to " + str(num) + "% power")
                elif parts[1] == "fr":
                    motor_driver.set_motor_power(Motor.FrontRight, num)
                    print("Front Right motor set to " + str(num) + "% power")
                elif parts[1] == "rl":
                    motor_driver.set_motor_power(Motor.RearLeft, num)
                    print("Rear Left motor set to " + str(num) + "% power")
                elif parts[1] == "rr":
                    motor_driver.set_motor_power(Motor.RearRight, num)
                    print("Rear Right motor set to " + str(num) + "% power")
                else:
                    print("Motor '" + parts[1] + "' invalid. Please use 'fl', 'fr', 'rl', or 'rr'")
            except:
                print("Unable to convert '" + parts[2] + "' into a floating point number")
    elif cmd == "test-fc":
        
        mp = input("First, set a MEAN_POWER: ")
        flight_controller.set_mean_power(float(mp))

        print("Enter values like this: backward_forward,left_right")
        print("For example: -40.3,50.1")

        while True:
            ip = input("Input:")
            if ip != "":
                vals = ip.split(",")
                if len(vals) != 2:
                    print("You did not provide two values.")
                    break
                ip1 = float(vals[0])
                ip2 = float(vals[1])

                # Go!
                flight_controller.set_direction(ip1, ip2)
            else:
                set_motor_power(Motor.FrontLeft, 0)
                set_motor_power(Motor.FrontRight, 0)
                set_motor_power(Motor.RearLeft, 0)
                set_motor_power(Motor.RearRight, 0)
                break
        
    elif cmd == "logs":
        t = 0
        for l in event_logging.LOGS:
            if t < 10:
                print(str(l.timestamp) + ": " + l.type + " - " + l.description)
            t = t + 1

    elif cmd[0:2] == "tx":
        parts = cmd.split(" ")
        if len(parts) == 3:
            if parts[1] == "mp":
                val = int(parts[2])

                # focus on mean power
                print("Setting focus...")
                radio_comm.send_code(settings.rc_focus_meanpower)

                # set the value
                print("Setting value...")
                radio_comm.send_code(int(str(settings.rc_pos_value_prefix) + str(val)))

            elif parts[1] == "dir":
                dual = parts[2].split(",")
                if len(dual) == 2:
                    bf = int(dual[0])
                    lr = int(dual[1])

                    #set backward forward
                    print("Setting backward_forward focus...")
                    radio_comm.send_code(settings.rc_focus_backwardforward)

                    #set backward forward value
                    print("Setting backward_forward value...")
                    if (bf >= 0):
                        radio_comm.send_code(int(str(settings.rc_pos_value_prefix) + str(bf)))
                    else:
                        radio_comm.send_code(int(str(settings.rc_neg_value_prefix) + str(abs(bf))))

                    #set left right
                    print("Setting left_right forcus...")
                    radio_comm.send_code(settings.rc_focus_leftright)

                    #set left right value
                    print("Setting left_right value...")
                    if (lr >= 0):
                        radio_comm.send_code(int(str(settings.rc_pos_value_prefix) + str(lr)))
                    else:
                        radio_comm.send_code(int(str(settings.rc_neg_value_prefix) + str(abs(lr))))
                    
                else:
                    print("You need to provide the direction like this: -80,20")
                    print("The -80 is the -80% for the backward forward. The 20 is the left-right.")
        elif len(parts) == 2:
            if parts[1] == "exec":
                radio_comm.send_code(settings.rc_fc_exec)
                print("Execution sent!")
            else:
                print("Part '" + parts[1] + "' not understood.")
        else:
            print("tx command was not in the correct format.")


    else:
        print("Command '" + cmd + "' not understood.")
