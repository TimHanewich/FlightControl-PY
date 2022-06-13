import time
import json


class note:
    id = 0
    start = 0.0
    duration = 0.25


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



