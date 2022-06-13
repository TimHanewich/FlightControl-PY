import json
import rythm
import RPi.GPIO as GPIO

f = open(r"C:\Users\tahan\Downloads\FlightControl-PY\j.json", "r")
x = f.read()
y = json.loads(x)

rm = rythm.rythm_machine(y)

lopis = rm.calc_lopi(1)
for l in lopis:
    print(str(l.status) + " " + str(l.duration))



GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
rd = rythm.rythm_driver(11)
print("Ready to execute!")
input("Press enter")
rd.execute(lopis)


print("Done")
GPIO.cleanup()