from mido import MidiFile
import mido
import rythm_midi
import resources
import settings
import rythm_driver
import RPi.GPIO as GPIO

mid = MidiFile(settings.song_beautiful_people)
rm = rythm_midi.midi_to_rm(mid)
instructions = rm.to_idis()

# Map the name of each track in the midi file to a GPIO pin number
map = {
    "i1":7,
    "i2":11,
    "i3":13,
    "i4":15,
    "i5":29,
    "i6":31,
    "i7":33,
    "i8":35,
    "i9":37,
    "i10":12,
}

# set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)

# play!
input("Ready to play. Press enter when ready!")
print("playing...")
rythm_driver.play(instructions, map)
print("Done")
