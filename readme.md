## In a MIDI file:
- BPM = 60,000,000 / the tempo in the message that looks like this: MetaMessage('set_tempo', tempo=468750, time=0)
    - http://midi.teragonaudio.com/tech/midifile/ppqn.htm
    - https://www.recordingblogs.com/wiki/time-division-of-a-midi-file
- Example of converting ticks to seconds: print(str(mido.tick2second(24, mid.ticks_per_beat, 468750)))
    - 24 is the ticks
    - mid is the midi object, ticks_per_beat is a property of the class
    - The tempo is provided in a meta message. This is used to divide 60,000,000 to get the BPM of the song (see above)