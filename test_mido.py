from mido import MidiFile

mid = MidiFile(r"C:\Users\tahan\Downloads\beautiful_people.mid")

#for track in mid.tracks:
#    print(track)

for msg in mid.tracks[1]:
    print(msg)