from mpu6050 import mpu6050
import settings
import flight_control
import time
import RPi.GPIO as GPIO
import math

def IsMoving(acc_x:float, acc_y:float, acc_z:float):
    pt = (acc_x * acc_x) + (acc_y * acc_y) + (acc_z * acc_z)
    g = pt / 9.81
    print("g: " + str(g))
    if g >= 1.25:
        return True
    else:
        return False
    

class MotionSensor:

    # This method only will continuously read the MPU-6050 module and store the telemetry data from that module in the appropriate values in the flight_control module.
    def StartMotionSensor(self):

        #create the mpu module class for transacting with it
        mpu = mpu6050(settings.mpu6050_address)

        while flight_control.KILL == False:
            acc = mpu.get_accel_data() #get accelerometer data
            gyro = mpu.get_gyro_data() #get gyroscop data

            # plug them in where they belong in the flight_control module:
            flight_control.AccX = acc["x"]
            flight_control.AccY = acc["y"]
            flight_control.AccZ = acc["z"]
            flight_control.GyroX = gyro["x"]
            flight_control.GyroY = gyro["y"]
            flight_control.GyroZ = gyro["z"]

            # wait the specified time in the settings module
            time.sleep(settings.mpu6050_refresh)


    def StartMotionLight(self):
        GPIO.setup(settings.pin_motionlight, GPIO.OUT) #set up the GPIO
        while flight_control.KILL == False:
            if IsMoving(flight_control.AccX, flight_control.AccY, flight_control.AccZ):
                GPIO.output(settings.pin_motionlight, GPIO.HIGH)
            else:
                GPIO.output(settings.pin_motionlight, GPIO.LOW)
            time.sleep(0.5) # wait a little bit
        GPIO.output(settings.pin_motionlight, GPIO.LOW) # turn off the light if it is on now
        GPIO.cleanup(settings.pin_motionlight)


