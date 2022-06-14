import time
import json
from xmlrpc.client import Boolean
from resources import sort_notes
#import RPi.GPIO as GPIO
import rythm

def map_id_to_pin(idis, mapping):
    for i in idis:
        if type(i) != float:
            nid = mapping[str(i.id)]
            i.id = nid


#def play(idis, mapping):


