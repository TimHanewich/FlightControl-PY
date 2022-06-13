import json
import rythm

f = open(r"C:\Users\tahan\Downloads\FlightControl-PY\j.json", "r")
x = f.read()
y = json.loads(x)

rm = rythm.rythm_machine(y)

lopis = rm.calc_lopi(1)
for l in lopis:
    print(str(l.status) + " " + str(l.duration))