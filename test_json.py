import json
import rythm
import settings
import threading
import resources
import RPi.GPIO as GPIO
import time

f = open(settings.song1, "r")
x = f.read()
y = json.loads(x)

rm = rythm.rythm_machine(y)


GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)



idis = rm.to_idis()
for g in idis:
    if type(g) == float:
        print("Wait " + str(g) + " seconds")
        time.sleep(g)
    else:
        print("Pin " + str(g.pin) + ": " + str(g.status))
        if g.pin == 0 and g.status == True:
            GPIO.output(11, GPIO.HIGH)
        elif g.pin == 1 and g.status == True:
            GPIO.output(13, GPIO.HIGH)
        if g.pin == 0 and g.status == False:
            GPIO.output(11, GPIO.LOW)
        elif g.pin == 1 and g.status == False:
            GPIO.output(13, GPIO.LOW)
        
        

print("DONE!")
GPIO.cleanup()
