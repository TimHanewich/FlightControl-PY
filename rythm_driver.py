import time
import json
from xmlrpc.client import Boolean
from resources import sort_notes
import RPi.GPIO as GPIO
import rythm

# takes a list of idis (instructions for GPIO execution) and replaces the ID's (instrument) with the actual pin number it should fire on, based on the mapping
#idis is the list made from the "to_idis" method in the rythm machine class. mapping is a JSON object that looks like this: map = {"0":11, "1":13}. In that example, mapping ID 0 to pin 11 and mapping ID 1 to pin 13
def map_id_to_pin(idis, mapping):
    for i in idis:
        if type(i) != float:
            nid = mapping[str(i.id)]
            i.id = nid


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
            time.sleep(i)
        else:
            if i.status == True:
                GPIO.output(i.id, GPIO.HIGH)
            else:
                GPIO.output(i.id, GPIO.LOW)
        
    #clean up each pin
    for pin in pins_used:
        GPIO.cleanup(pin)

