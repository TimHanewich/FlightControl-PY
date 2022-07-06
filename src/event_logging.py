import datetime



class event_log:
    type = ""
    timestamp = datetime.datetime.now()
    description = ""


LOGS = []

def add_log(l:event_log):
    LOGS.insert(0, l)

def log(type:str, desc:str):
    l = event_log()
    l.type = type
    l.description = desc
    add_log(l)