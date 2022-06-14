import json
import rythm
import settings
import threading
import resources
import time

f = open(settings.song1, "r")
x = f.read()
y = json.loads(x)

rm = rythm.rythm_machine(y)

instructions = rm.to_idis()
for i in instructions:
    if type(i) == float:
        print("WAIT " + str(i))
    else:
        print("ID: " + str(i.id) + " Status: " + str(i.status))