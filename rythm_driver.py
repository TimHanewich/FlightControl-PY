import time
import json
from xmlrpc.client import Boolean
from resources import sort_notes
import RPi.GPIO as GPIO
import rythm
from resources import map_id_to_pin
import settings




def play(idis, mapping):

    # first, replace all ID's with pin numbers, based on the mapping
    map_id_to_pin(idis, mapping)

    # now, get a list of pins that we are using
    pins_used = []
    for i in idis:
        if type(i) != float:
            if i.id not in pins_used:
                pins_used.append(i.id)

    # activate each pin
    for pin in pins_used:
        GPIO.setup(pin, GPIO.OUT)
    
    # play!
    for i in idis:
        if type(i) == float:
            time.sleep(max(i - settings.compensation_delay, 0))
        else:
            if i.status == True:
                GPIO.output(i.id, GPIO.HIGH)
            else:
                GPIO.output(i.id, GPIO.LOW)
        
    #clean up each pin
    for pin in pins_used:
        GPIO.cleanup(pin)

