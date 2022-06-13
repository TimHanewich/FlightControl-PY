import time
import json
from xmlrpc.client import Boolean
from resources import sort_notes


# The raw input into the system - created by a human by hand!
class note:
    id = 0 #the id of the "instrument" or "device" that this should appear on
    start = 0.0 #what beat to start on
    duration = 0.25 #duration in beats

# "Light operation instruction" - calculated BASED ON the notes above
class lopi:
    status = False # False = light off, True = light on
    duration = 0.0 #duration to hold, in seconds


class rythm_machine:
    __beatsec__:float = 0.0
    bpm = 0
    notes = []
    def __init__(self, json):
        self.__beatsec__ = float(60) / json["bpm"]
        self.bpm = json["bpm"]
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

    # construction of the LOPI for a particular ID
    def calc_lopi(self, id:int):
        idnotes = self.notes_for_id(id)
        idnotes = sort_notes(idnotes)
        toreturn = []
        
        # If the first note (it will be arranged) does not occur on beat 0 (the beginning), create the empty space at first
        if idnotes[0].start != 0:
            eb = lopi()
            eb.status = False
            eb.duration = self.beats_to_seconds(idnotes[0].start)
            toreturn.append(eb)
        
        last_note = None
        for n in idnotes:

            # if last_note is NOT null, it means we need to inject an empty period here
            if last_note != None:
                tlopi = lopi()
                tlopi.status = False
                tlopi.duration = self.beats_to_seconds(n.start - last_note.start)
                toreturn.append(tlopi)
            
            nlopi = lopi()
            nlopi.status = True
            nlopi.duration = self.beats_to_seconds(n.duration)
            toreturn.append(nlopi)

            # mark the last note, so that way it will calculate the empty area on the next loop
            last_note = n
        
        return toreturn

            