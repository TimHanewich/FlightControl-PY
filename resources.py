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