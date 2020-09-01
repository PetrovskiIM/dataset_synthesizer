import pretty_midi
import numpy as np
import os
import sys

from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib import colors
import pretty_midi
import pandas as pd


midi_data = pretty_midi.PrettyMIDI("/home/petrovskiyim/Projects/dataset_synthesizer/data/re_instrumented_chunked_copies/MIDI-Unprocessed_02_R1_2008_01-05_ORIG_MID--AUDIO_02_R1_2008_wav--1_30_60_ElectricOrgan.mid")

midi_list = []
print(midi_data.instruments)
for instrument in midi_data.instruments:
    for note in instrument.notes:
        start = note.start
        end = note.end
        pitch = note.pitch
        velocity = note.velocity
        midi_list.append([start, end, pitch, velocity, instrument.name])

midi_list = sorted(midi_list, key=lambda x: (x[0], x[2]))

df = pd.DataFrame(midi_list, columns=['Start', 'End', 'Pitch', 'Velocity', 'Instrument'])
print(df)
