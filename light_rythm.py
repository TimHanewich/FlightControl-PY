import time
import json
from xmlrpc.client import Boolean
from resources import sort_notes
import RPi.GPIO as GPIO

class rythm_driver:
    pin = 0
    
    def __init__(self, pin):
        self.pin = pin
    
    def execute(self, lopis):
        GPIO.setup(self.pin, GPIO.OUT) # set up the pin to be used

        for l in lopis:
            if l.status == True:
                GPIO.output(self.pin, GPIO.HIGH)
            else:
                GPIO.output(self.pin, GPIO.LOW)
            time.sleep(l.duration)
        
        GPIO.cleanup(self.pin) # close the single pin we have worked on
