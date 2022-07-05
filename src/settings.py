### ENABLEMENT ###
enable_quadcopter = True
enable_mpu6050 = False
enable_statuslight = False
enable_motionlight = False
enable_radio = True
###################

# Pins
pin_mFL = 35 #front left motor (clockwise)
pin_mFR = 36 #front right motor (counter clock wise)
pin_mRL = 37 #rear left motor (counter clock wise)
pin_mRR = 38 #rear right motor (clockwise)
pin_statuslight = 11
pin_motionlight = 40 #Light will be on if it is detected the device is not moving or rotating (relatively still). Off if movement is detected (via the MPU-6050 module)
gpio_receiver = 27 #433mHz radio reciever. GPIO number, not pin number.
gpio_transmitter = 17 #433mHz radio transmitter. GPIO number, not pin number.

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

# Radio Communication settings
rf_terminator = 617833 #the value that represents the last command is now "over" - sent at the end of each message to confirm the last message is finished.
rf_motor_off = 617835 # all motors off (0%)
rf_motor_idle = 617834 #all motors to idle (1% power)

# Radio Communications - focusing
rf_focus_all = 617835 #set focus to all motors (all 4)
rf_focus_fl = 617836 #set focus to front left motor
rf_focus_fr = 617837 #set focus to front right motor
rf_focus_rl = 617838 #set focus to rear left motor
rf_focus_rr = 617839 #set focus to rear right motor

# Radio Communications - power commands
rf_power0 = 617840 #power to 0%
rf_power1 = 617841 #power to 1%

