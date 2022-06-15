from mido import MidiFile
import mido
import rythm_midi
import resources

mid = MidiFile(r"C:\Users\tahan\Downloads\beautiful_people.mid")

rm = rythm_midi.midi_to_rm(mid)

for n in rm.notes:
    print(n.id + " Start: " + str(n.start) + " Duration: " + str(n.duration))

instructions = rm.to_idis()

map = {"808 Kick": 11, "808 HiHat": 13}

resources.map_id_to_pin(instructions, map)

for i in instructions:
    if type(i) == float:
        print("WAIT " + str(i))
    else:
        print("ID: " + str(i.id) + " Status: " + str(i.status))
