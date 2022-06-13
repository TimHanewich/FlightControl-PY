from ast import arg
import json
import rythm
import RPi.GPIO as GPIO
import settings
import light_rythm
import threading

f = open(settings.song1, "r")
x = f.read()
y = json.loads(x)

rm = rythm.rythm_machine(y)

lopis0 = rm.calc_lopi(0)
lopis1 = rm.calc_lopi(1)



GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
rd = light_rythm.rythm_driver(13)
rd2 = light_rythm.rythm_driver(11)

t1 = threading.Thread(target=rd.execute, args=(lopis0, ))
t2 = threading.Thread(target=rd2.execute, args=(lopis1, ))


print("Ready to execute!")
input("Press enter")

t1.start()
t2.start()
t1.join()
t2.join()



print("Done")