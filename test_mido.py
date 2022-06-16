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

# set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)

# play!
rythm_driver.play(instructions, map)
