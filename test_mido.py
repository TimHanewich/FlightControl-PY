from mido import MidiFile
import mido
import rythm_midi
import resources

mid = MidiFile(r"C:\Users\tahan\Downloads\midi_projects\Chris Brown - Beautiful People\midi\bp1.mid")

rm = rythm_midi.midi_to_rm(mid)

for n in rm.notes:
    print(n.id + " Start: " + str(n.start) + " Duration: " + str(n.duration))

instructions = rm.to_idis()

map = {
    "i1":1,
    "i2":2,
    "i3":3,
    "i4":4,
    "i5":5,
    "i6":6,
    "i7":7,
    "i8":8,
    "i9":9,
    "i10":10,
}
resources.map_id_to_pin(instructions, map)

for i in instructions:
    if type(i) == float:
        print("WAIT " + str(i))
    else:
        print("ID: " + str(i.id) + " Status: " + str(i.status))
