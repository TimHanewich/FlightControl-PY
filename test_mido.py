from mido import MidiFile
import mido
import rythm_midi

mid = MidiFile(r"C:\Users\tahan\Downloads\beautiful_people.mid")

rm = rythm_midi.midi_to_rm(mid)

for n in rm.notes:
    try:
        print(n.id + " Start: " + str(n.start) + " Duration: " + str(n.duration))
    except:
        print("error")
    