import time
import json
from xmlrpc.client import Boolean
from resources import sort_notes


# The raw input into the system - created by a human by hand!
class note:
    id = 0 #the id of the "instrument" or "device" that this should appear on
    start = 0.0 #what beat to start on
    duration = 0.25 #duration in beats


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



            