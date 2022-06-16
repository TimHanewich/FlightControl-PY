import RPi.GPIO as GPIO

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

while True:
    pin = input("Test on pin: ")
    if pin == "":
        quit()
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    print("Pin " + str(pin) + " on high!")
    input("Enter to stop")
    GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup(pin)