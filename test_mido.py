from mido import MidiFile
import mido

mid = MidiFile(r"C:\Users\tahan\Downloads\beautiful_people.mid")

#for track in mid.tracks:
#    print(track)

for msg in mid.tracks[2]:
    if msg.type == "note_on":
        print("On: " + str(msg.time))
    elif msg.type == "note_off":
        print("Off: " + str(msg.time))

    

print(str(mido.tick2second(24, mid.ticks_per_beat, 468750)))