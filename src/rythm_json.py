from rythm import rythm_machine
from rythm import note

def json_to_rm(json) -> rythm_machine:
    toreturn = rythm_machine()
    toreturn.__beatsec__ = float(60) / json["bpm"]
    toreturn.bpm = json["bpm"]
    toreturn.offset = json["offset"]
    for n in json["notes"]:
        tn = note()
        tn.id = n["id"]
        tn.start = n["start"]
        tn.duration = n["duration"]
        toreturn.notes.append(tn)
    return toreturn