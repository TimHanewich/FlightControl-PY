import time
import json
from xmlrpc.client import Boolean
from resources import sort_notes
import resources


# The raw input into the system - created by a human by hand!
class note:
    id = 0 #the id of the "instrument" or "device" that this should appear on
    start = 0.0 #what beat to start on
    duration = 0.25 #duration in beats

# GPIOI - short for "GPIO instruction"
class gpioi:
    pin = 0 # pin to trigger
    status = False #False means turn it off, True means turn it on

# "GPIO instruction with time"
class gpioit(gpioi):
    time = 0.0 # time (in seconds) that this should be triggered on


class rythm_machine:
    __beatsec__:float = 0.0
    bpm = 0
    offset = 0.0 #how many seconds to "offset" before the first beat - i.e. if the MP3 file of the song starts and then has 1.3 seconds of silence before the first beat, this would be 1.3
    notes = []
    def __init__(self, json):
        self.__beatsec__ = float(60) / json["bpm"]
        self.bpm = json["bpm"]
        self.offset = json["offset"]
        for n in json["notes"]:
            tn = note()
            tn.id = n["id"]
            tn.start = n["start"]
            tn.duration = n["duration"]
            self.notes.append(tn)
    
    def all_ids(self):
        ids = []
        for n in self.notes:
            if n.id not in ids:
                ids.append(n.id)
        return ids

    # Gets notes only for a specific ID
    def notes_for_id(self, id:int):
        toreturn = []
        for n in self.notes:
            if (n.id == id):
                toreturn.append(n)
        return toreturn

    def beats_to_seconds(self, beat:float) -> float:
        toreturn = beat * self.__beatsec__
        return toreturn

    def to_gpiois(self):
        toreturn = []
        snotes = resources.sort_notes(self.notes)

        # if there is an offset, add a wait
        if self.offset > 0:
            toreturn.append(self.offset)
        
        # if the first note is not on the first beat, add a wait
        if snotes[0].start != 0:
            toreturn.append(self.beats_to_seconds(snotes[0].start))

        last_note = None
        for n in snotes:
            g = gpioi()
            g.pin = n.id
            g.status = True
            toreturn.append(g)


    def to_gpioits(self):
        toreturn = []
        snotes = resources.sort_notes(self.notes)
        
        for n in snotes:

            #Do the on
            go = gpioit()
            go.pin = n.id
            go.status = True
            go.time = self.beats_to_seconds(n.start) + self.offset
            toreturn.append(go)

            #Do the off
            gf = gpioit()
            gf.pin = n.id
            gf.status = False
            gf.time = go.time + self.beats_to_seconds(n.duration)
            toreturn.append(gf)

        return toreturn



            