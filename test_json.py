import json
import rythm

f = open(r"C:\Users\tahan\Downloads\FlightControl-PY\j.json", "r")
x = f.read()
y = json.loads(x)

rm = rythm.rythm_machine(y)

notes = rm.notes_for_id(0)
for n in notes:
    print(n.start)

notesa = rythm.sort_notes(notes)
print(len(notesa))