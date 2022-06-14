import json
import rythm
import settings
import threading
import resources
#import RPi.GPIO as GPIO
import time
import rythm_driver

f = open(settings.song1, "r")
x = f.read()
y = json.loads(x)

rm = rythm.rythm_machine(y)

idis = rm.to_idis()

map = {"0":11, "1":13}

for i in idis:
    if type(i) != float:
        print(i.id)

rythm_driver.map_id_to_pin(idis, map)

for i in idis:
    if type(i) != float:
        print(i.id)


