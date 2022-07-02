### ENABLEMENT ###
enable_quadcopter = True
enable_mpu6050 = False
enable_statuslight = False
enable_motionlight = False
###################

# Pins
pin_mFL = 35 #front left motor (clockwise)
pin_mFR = 36 #front right motor (counter clock wise)
pin_mRL = 37 #rear left motor (counter clock wise)
pin_mRR = 38 #rear right motor (clockwise)
pin_statuslight = 11
pin_motionlight = 40 #Light will be on if it is detected the device is not moving or rotating (relatively still). Off if movement is detected (via the MPU-6050 module)

#Music
song1 = r"C:\Users\tahan\Downloads\FlightControl-PY\j.json"
song_beautiful_people = r"C:\Users\tahan\Downloads\FlightControl-PY\beautiful_people.json"

# Music
compensation_delay = 0.05 #it takes a little bit of time for each GPIO operation to occur, so naturally, by the end of the song, the GPIO display will be a little bit behind the normal beat. This is how much time to take OFF of the normal wait time. For example, if it is supposed to wait 1 second in between a beat (say, 60 BPM), instead of waiting 1 full second, actually wait 0.98 seconds to accomodate for the delay in processor speed. Will have to eye-ball it, no way to make it that precise

# MPU-6050 (acc, gyro, temp)
mpu6050_address = 0x68 #hexadecimal address of the MPU-6050 module (see readme for finding this after it is wired up)
mpu6050_refresh = 1 # how many seconds to wait in between each refresh of the MPU-6050 data (acceleromoter/gyro)

# Flight controller settings
slip_diff = 10 # the difference in percent that a single motor on the quadcopter can deviate from the set power level. For example, if the power is set to 50% and the slip diff is set to 25, a single motor can go up to 75% and down to 25% to accomodate needs.