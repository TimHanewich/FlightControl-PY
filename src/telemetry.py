from mpu6050 import mpu6050
import settings
import flight_control
import time

class MotionSensor:

    # This method only will continuously read the MPU-6050 module and store the telemetry data from that module in the appropriate values in the flight_control module.
    def StartMotionSensor():

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


