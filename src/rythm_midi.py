import mido
import rythm

def midi_to_rm(midi_file:mido.MidiFile) -> rythm.rythm_machine:
    toreturn = rythm.rythm_machine()

    # first, get the tempo
    tempo = 0
    for t in midi_file.tracks:
        for msg in t:
            if "set_tempo" in str(msg):
                tempo = msg.tempo
    
    # get the bpm, using that tempo
    toreturn.bpm = 60000000/tempo

    # calculate how many seconds per beat
    toreturn.__beatsec__ = 60 / toreturn.bpm

    # set offset to 0
    toreturn.offset = 0

    # now, calculate each note:
    for t in midi_file.tracks:

        # does this track contain note on/off? If it does, it is a track so we need to convert the messages in this track to notes
        contains_note_on_off = False
        for msg in t:
            if "note_on" in str(msg):
                contains_note_on_off = True
            elif "note_off" in str(msg):
                contains_note_on_off = True

        # if it is a note track, convert
        if contains_note_on_off:
            
            # get the name
            track_name = ""
            for msg in t:
                if "track_name" in str(msg):
                    track_name = msg.name

            # get each on and off:
            current_note = rythm.note()
            current_time = 0 # the current time we are on, in TICKS
            for msg in t:

                # handle the time increment (upwards)
                if "note_on" in str(msg) or "note_off" in str(msg):
                    current_time = current_time + msg.time

                # handle the note notation
                if "note_on" in str(msg):
                    current_note = rythm.note()
                    current_note.id = track_name

                    # calculate the start (beat) via a tick
                    ticks = current_time
                    seconds = mido.tick2second(ticks, midi_file.ticks_per_beat, tempo) # the seconds that should have passed since the last "on" message.
                    time_beats = seconds / toreturn.__beatsec__ # the duration of this note, in beats, not seconds (required for the rythm machine, but will later be converted to seconds of course for the GPIO operations)
                    current_note.start = time_beats
                elif "note_off" in str(msg):
                    if current_note != None:
                        ticks = msg.time
                        seconds = mido.tick2second(ticks, midi_file.ticks_per_beat, tempo) # the seconds that should have passed since the last "on" message.
                        duration_beats = seconds / toreturn.__beatsec__ # the duration of this note, in beats, not seconds (required for the rythm machine, but will later be converted to seconds of course for the GPIO operations)
                        current_note.duration = duration_beats

                        # close the note (and save)
                        toreturn.notes.append(current_note)


    return toreturn
                    
                




            
        