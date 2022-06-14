import json
import rythm
import settings
import threading
import resources
import RPi.GPIO as GPIO
import time
import rythm_driver

f = open(settings.song1, "r")
x = f.read()
y = json.loads(x)

rm = rythm.rythm_machine(y)

idis = rm.to_idis()

map = {"kick":11, "clap":13}

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

rythm_driver.play(idis, map)

