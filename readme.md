## Attached Devices
Each drone will have the following attached devices:
- Raspberry Pi Zero W
- 4 motors
- GPS Module
- MPU-6050 (Accelerometer, Gyroscope, Temperature sensor)
- Digital Compass
- Radio receiver

### I2C
Of the above attached devices, the following require the I2C protocol:
- MPU-6050
- GPS Module
- Digital Compass
- Radio receiver


## In a MIDI file:
- BPM = 60,000,000 / the tempo in the message that looks like this: MetaMessage('set_tempo', tempo=468750, time=0)
    - http://midi.teragonaudio.com/tech/midifile/ppqn.htm
    - https://www.recordingblogs.com/wiki/time-division-of-a-midi-file
- Example of converting ticks to seconds: print(str(mido.tick2second(24, mid.ticks_per_beat, 468750)))
    - 24 is the ticks
    - mid is the midi object, ticks_per_beat is a property of the class
    - The tempo is provided in a meta message. This is used to divide 60,000,000 to get the BPM of the song (see above)


## Examples
### Parsing a MIDI into a series of instructions for the GPIO:
```
from mido import MidiFile
import mido
import rythm_midi
import resources

mid = MidiFile(r"C:\Users\tahan\Downloads\midi_projects\Chris Brown - Beautiful People\midi\bp1.mid")

rm = rythm_midi.midi_to_rm(mid)

for n in rm.notes:
    print(n.id + " Start: " + str(n.start) + " Duration: " + str(n.duration))

instructions = rm.to_idis()

# Map the name of each track in the midi file to a GPIO pin number
map = {
    "i1":1,
    "i2":2,
    "i3":3,
    "i4":4,
    "i5":5,
    "i6":6,
    "i7":7,
    "i8":8,
    "i9":9,
    "i10":10,
}
resources.map_id_to_pin(instructions, map)

for i in instructions:
    if type(i) == float:
        print("WAIT " + str(i))
    else:
        print("ID: " + str(i.id) + " Status: " + str(i.status))

```

## How to get the MPU-6050 Module (Gyroscope, Accelerator, Temperature Sensor) to work
- https://www.youtube.com/watch?v=JTFa5l7zAA4
- Backup of the above video: https://youtu.be/jREIJ80rwz0
- MPU6050 Hexadecimal Address: `0x68`
- MPU6050 decimal address: `104`

1. Enable I2C (IIC) on raspberry PI:
    1. sudo raspi-config
    2. Go to "Interfacing options"
    3. Select "I2C"
    4. Select "Yes"
2. We need to use the "i2cdetect" commad in bash to determine the address of the MPU-6050 module. To use this command, you must have i2c tools installed: `sudo apt-get install i2c-tools`
3. Run command `i2cdetect -y 1` to get the address of the MPU-6050 module. The number you see will be the address and **will be used in the code later**.
4. Install the software to use this module. Run command `sudo apt install python3-smbus` 
5. Install the Python library for interfacing with this module (easily): `python3 -m pip install mpu6050-raspberrypi`

Example Code:
```
from mpu6050 import mpu6050

mpu = mpu6050(0x68)

while True:
        temp = mpu.get_temp()
        print("Temperature: " + str(temp))

        acc = mpu.get_accel_data()
        print("AccX: " + str(acc["x"]))
        print("AccY: " + str(acc["y"]))
        print("AccZ: " + str(acc["z"]))

        gyro = mpu.get_gyro_data()
        print("GyroX: " + str(gyro["x"]))
        print("GyroY: " + str(gyro["y"]))
        print("GyroZ: " + str(gyro["z"]))


        ip = input("Enter to try agian, 'exit' to exit: ")
        if ip == "exit":
                exit()
```

## Double-Transistor Amplification Circuit Design
- Both the input from the Raspberry Pi into the first transistor and the input into the second transistor (the one that directly drives the motor) are to use a 15 ohm resistor on the base.
    - I've tested that this will only allow a draw of ~ 0.6 mA from one of the GPIO pins at full speed. Well below the 16 mA limit.

## Radio Communications
- Repo with demo code for using RPI-RF: https://github.com/milaq/rpi-rf
- Using the radio transmitter + receiver w/ RPI: https://www.instructables.com/RF-433-MHZ-Raspberry-Pi/
- All about the modules, antennas, etc: https://www.youtube.com/watch?v=b5C9SPVlU4U&ab_channel=DroneBotWorkshop
- **Important to note** - the rpi-rf module accepts the GPIO # for the transmitter/receiver pin, NOT the board number. For example, pin # 11 would need to be given to it as GPIO # 17.



## Learnings about transistors
- Beta is the same thing as hFe (DC current gain)
    - This is the ratio of the collector current to the base current.
    - i.e. if we want the collector current to be 1 amp and the beta of the transistor is 5, base current would have to be 200mA.


## Connecting an Xbox Controller
- Run `lsusb` in bash to list the connected USB devices.
- Install xboxdrv: `sudo apt-get install xboxdrv`
- Run `xboxdrv -L` to get a list of attached controllers (will only recognize Xbox 360 controllers)
- Clone and run this: https://github.com/FRC4564/Xbox/blob/master/sample.py
    - You will need the sample code and xbox.py code in the same repository
- It is important to run the python scripts with sudo. i.e. `sudo python3 rc.py` for my radio transmitter module.

## Notes on Raspberry Pi Zero W Current Draw (all at 5V)
- Turned off, yet plugged in: 0.031A

## Drone Wiring Schematics
- Positives needed
    - Front left motor
    - Front right motor
    - Rear left motor
    - Rear right motor
    - DC-DC Converter (for Pi)
- Negatives needed
    - 

## NEO-6M GPS Module Usage (https://www.amazon.com/dp/B07P8YMVNT?smid=A1N6DLY3NQK2VM)
Guide on how to use this with the Raspberry Pi (in normal Python, not MicroPython): https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/
- You will need the [pyserial package](https://pypi.org/project/pyserial/). That is not mentioned in the guide above.
- You will be installing the [pynmea2 package](https://pypi.org/project/pynmea2/). GitHub repo [here](https://github.com/Knio/pynmea2).

Example code (works on a micro-computer, so not the Raspberry Pi Pico):
```
import serial
import time
import string
import pynmea2

while True:
        port="/dev/ttyAMA0"
        ser=serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata=ser.readline()

        newdatastr = newdata.decode("utf-8")
        if "GPGGA" in newdatastr:
                msg = pynmea2.parse(newdatastr)
                print(str(msg.latitude) + ", " + str(msg.longitude) + " - " + str(msg.altitude))
```