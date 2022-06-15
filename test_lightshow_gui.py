import json
import tkinter
import mido
import rythm
import rythm_midi
import math
import resources
import time

##### SETTINGS ######
canvas_width = 800
canvas_height = 600
#####################

# get the midi file and convert it into a rythm machine
midi_file = mido.MidiFile(r"C:\Users\tahan\Downloads\midi_projects\Chris Brown - Beautiful People\midi\bp1.mid")
rm = rythm_midi.midi_to_rm(midi_file)

# calculate the # of rows and columns we will need based on the # of tracks
columns_needed = math.ceil(math.sqrt(len(rm.all_ids())))
rows_needed = math.ceil(len(rm.all_ids()) / columns_needed)

print("Cols: " + str(columns_needed))
print("Rows: " + str(rows_needed))

# calculate the height and width of each square we will make, based on how many we need and how many we have
square_width = canvas_width / columns_needed
square_height = canvas_height / rows_needed


# create the visuals
window = tkinter.Tk("Light Show Test")
canvas = tkinter.Canvas(height=canvas_height, width=canvas_width)
canvas.pack()

# get a list of all of the ID's used in the file
ids = rm.all_ids()
print(json.dumps(ids))

# create each square
pads = []
on_pos_x = 0
on_pos_y = 0
for r in range(0, rows_needed):
    for c in range(0, columns_needed):
        if len(pads) < len(ids):
            pad = canvas.create_rectangle(on_pos_x, on_pos_y, on_pos_x + square_width, on_pos_y + square_height, fill="blue")
            pads.append(pad)
        on_pos_x = on_pos_x + square_width
    on_pos_x = 0 # reset
    on_pos_y = on_pos_y + square_height

# create a mapping that we will use to map the instrument ID's to the index square (not worrying about GPIO mappings at all)
map = {}
pn = 0
for id in rm.all_ids():
    map[id] = pn
    pn = pn + 1

# convert the notes to instructions to follow
instructions = rm.to_idis()

# re-map it to the square indexes
resources.map_id_to_pin(instructions, map)



# show it
window.mainloop()


# now play!
for i in instructions:
    if type(i) == float:
        time.sleep(i)
    else:
        if i.status == True:
            canvas.itemconfig(pads[i.id], fill="red")
        else:
            canvas.itemconfig(pads[i.id], fill="blue")

