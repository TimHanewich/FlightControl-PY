### ENABLEMENT ###
enable_quadcopter = True
enable_mpu6050 = False
enable_statuslight = False
enable_motionlight = False
enable_radio = True
###################

# Pins
gpio_mFL = 19 #front left motor (clockwise)
gpio_mFR = 16 #front right motor (counter clock wise)
gpio_mRL = 26 #rear left motor (counter clock wise)
gpio_mRR = 20 #rear right motor (clockwise)
gpio_statuslight = 17
gpio_motionlight = 21 #Light will be on if it is detected the device is not moving or rotating (relatively still). Off if movement is detected (via the MPU-6050 module)
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
rc_terminator = 617833 #the value that represents the last command is now "over" - sent at the end of each message to confirm the last message is finished.
rc_motor_off = 617835 # all motors off (0%)
rc_fc_exec = 617844 # execute the values we have saved on the flight controller

# Radio Communications - focusing
rc_focus_backwardforward = 617842 #set focus to backwardforward
rc_focus_leftright = 617843 #set focus to leftright


# Radio Communications - value
rc_pos_value_prefix = 771 #starts every value command. For example, entering in 89% would be 77789
rc_neg_value_prefix = 769 #starts every value command that is negative. For example, -77% would be 76977

