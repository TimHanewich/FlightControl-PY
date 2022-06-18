from enum import IntEnum

class sys_status(IntEnum):
    offline = 0,
    standby = 1

#### UTILITY BELOW #####

def sort_notes(notes):
    topullfrom = []
    for item in notes:
        topullfrom.append(item)
    toreturn = []
    while len(topullfrom) > 0:
        winner = topullfrom[0]
        for n in topullfrom:
            if n.start < winner.start:
                winner = n
        topullfrom.remove(winner)
        toreturn.append(winner)
    return toreturn

# sort idit's by time
def sort_idits(idits):
    topullfrom = []
    for item in idits:
        topullfrom.append(item)
    toreturn = []
    while len(topullfrom) > 0:
        winner = topullfrom[0]
        for n in topullfrom:
            if n.time < winner.time:
                winner = n
        topullfrom.remove(winner)
        toreturn.append(winner)
    return toreturn


# takes a list of idis (instructions for GPIO execution) and replaces the ID's (instrument) with the actual pin number it should fire on, based on the mapping
#idis is the list made from the "to_idis" method in the rythm machine class. mapping is a JSON object that looks like this: map = {"0":11, "1":13}. In that example, mapping ID 0 to pin 11 and mapping ID 1 to pin 13
def map_id_to_pin(idis, mapping):
    for i in idis:
        if type(i) != float:
            nid = mapping[i.id]
            i.id = nid