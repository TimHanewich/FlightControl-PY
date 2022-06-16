import RPi.GPIO as GPIO

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

while True:
    pin = input("Test on pin: ")
    if pin == "":
        quit()
    GPIO.setup(int(pin), GPIO.OUT)
    GPIO.output(int(pin), GPIO.HIGH)
    print("Pin " + str(pin) + " on high!")
    input("Enter to stop")
    GPIO.output(int(pin), GPIO.LOW)
    GPIO.cleanup(int(pin))