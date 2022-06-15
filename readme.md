## In a MIDI file:
- BPM = 60,000,000 / the tempo in the message that looks like this: MetaMessage('set_tempo', tempo=468750, time=0)
    - http://midi.teragonaudio.com/tech/midifile/ppqn.htm
    - https://www.recordingblogs.com/wiki/time-division-of-a-midi-file
- Example of converting ticks to seconds: print(str(mido.tick2second(24, mid.ticks_per_beat, 468750)))
    - 24 is the ticks
    - mid is the midi object, ticks_per_beat is a property of the class
    - The tempo is provided in a meta message. This is used to divide 60,000,000 to get the BPM of the song (see above)


## Examples
### Parsing a MIDI into a series of instructions for the GPIO:
```
from mido import MidiFile
import mido
import rythm_midi
import resources

mid = MidiFile(r"C:\Users\tahan\Downloads\midi_projects\Chris Brown - Beautiful People\midi\bp1.mid")

rm = rythm_midi.midi_to_rm(mid)

for n in rm.notes:
    print(n.id + " Start: " + str(n.start) + " Duration: " + str(n.duration))

instructions = rm.to_idis()

# Map the name of each track in the midi file to a GPIO pin number
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

```