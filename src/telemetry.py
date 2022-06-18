from mpu6050 import mpu6050
import settings
import flight_control
import time
import RPi.GPIO as GPIO
import math

def IsMoving(acc_x:float, acc_y:float, acc_z:float, gyro_x:float, gyro_y:float, gyro_z:float):
    
    # Calculate via accelerometer
    pt = math.sqrt((acc_x * acc_x) + (acc_y * acc_y) + (acc_z * acc_z))
    g = pt / 9.81
    if g >= 1.06: #if the g force from the accelerometer exceeds this threshold, we are moving
        return True

    # Calculate via the gyro
    gsqrt = math.sqrt((gyro_x * gyro_x) + (gyro_y * gyro_y) + (gyro_z * gyro_z))
    if gsqrt > 1.8:
        return True

    #If we've gotten this far, that means we must not be moving. We've passed both
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
            if IsMoving(flight_control.AccX, flight_control.AccY, flight_control.AccZ, flight_control.GyroX, flight_control.GyroY, flight_control.GyroZ): 
                # if it is moving, light off
                GPIO.output(settings.pin_motionlight, GPIO.LOW)
            else: # If it is NOT moving, show the light on
                GPIO.output(settings.pin_motionlight, GPIO.HIGH)
            time.sleep(0.5) # wait a little bit
        GPIO.output(settings.pin_motionlight, GPIO.LOW) # turn off the light if it is on now
        GPIO.cleanup(settings.pin_motionlight)


