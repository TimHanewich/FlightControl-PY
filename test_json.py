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

for n in rm.notes:
    print(n.id)

input()

instructions = rm.to_idis()
for i in instructions:
    if type(i) == float:
        print("WAIT " + str(i))
    else:
        print("ID: " + str(i.id) + " Status: " + str(i.status))


map = {"kick":11, "clap":13}

resources.map_id_to_pin(instructions, map)
for i in instructions:
    if type(i) == float:
        print("WAIT " + str(i))
    else:
        print("ID: " + str(i.id) + " Status: " + str(i.status))
