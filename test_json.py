import json
import rythm
import settings
import threading
import resources

f = open(settings.song1, "r")
x = f.read()
y = json.loads(x)

rm = rythm.rythm_machine(y)

#v = rm.to_gpioits()
#v = resources.sort_gpioits(v)
#for vv in v:
#    print(str(vv.pin) + " " + str(vv.status) + " " + str(vv.time))


gpiois = rm.to_gpiois()
for g in gpiois:
    if type(g) == float:
        print("Wait " + str(g) + " seconds")
    else:
        print("Pin " + str(g.pin) + ": " + str(g.status))