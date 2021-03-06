import pathlib
from mido import MidiFile
from music21 import converter, instrument
from format import convert_to_axillary_representation, convert_to_midi_track, count_up_steps, count_down_steps
import pretty_midi

instruments_dictionary = {
    "Piano": instrument.Piano(),
    "EnglishHorn": instrument.EnglishHorn(),
    "ElectricOrgan": instrument.ElectricOrgan(),
    "Harpsichord": instrument.Harpsichord(),
    "PipeOrgan": instrument.PipeOrgan(),
    "Violin": instrument.Violin()
}


def change_instrument_in_mid(mid, instrument_name, buffer_file_path="./data/buffer/temporary.mid"):
    pathlib.Path(buffer_file_path).parent.mkdir(parents=True, exist_ok=True)

    mid.save(buffer_file_path)
    s = converter.parse(buffer_file_path)

    instrument_to_play = instruments_dictionary[instrument_name]
    for el in s.recurse():
        if 'Instrument' in el.classes:
            el.activeSite.replace(el, instrument_to_play)

    s.write('midi', buffer_file_path)
    return MidiFile(buffer_file_path, clip=True)


# region augmentation that works with paths
def change_instrument(path, target_path, instrument_name='Piano'):
    s = converter.parse(path)
    instrument_to_play = instruments_dictionary[instrument_name]
    # for el in s.recurse():
    #     if 'Instrument' in el.classes:
    #         el.activeSite.replace(el, instrument_to_play)
    for p in s.parts:
        p.insert(0, instrument_to_play)
    s.write('midi', target_path)


def change_octave(path, target_path, shift=1, shift_step=7):
    pm = pretty_midi.PrettyMIDI(path)
    for instrument in pm.instruments:
        # Skip drum instruments - their notes aren't pitched!
        if instrument.is_drum:
            continue
        for note in instrument.notes:
            note.pitch += shift_step*shift
    pm.write(target_path)
    # mido_object = MidiFile(path, clip=True)
    # # print(len(mido_object.tracks))
    # track_i = 1
    # if len(mido_object.tracks) ==1:
    #     print("SOMETHING WENT WRONG AND MIDO FILE WAS RECIVED WITH SINGLE TRACK")
    #     track_i = 0
    # readable_track_df, begin_of_track, end_of_track = convert_to_axillary_representation(mido_object.tracks[track_i])
    # readable_track_df["note"] += shift * 7
    # mido_object.tracks[track_i] = convert_to_midi_track(readable_track_df, begin_of_track, end_of_track)
    # mido_object.save(target_path)


def cut_chunk(path, target_path, begin_i=20, end_i=60):
    mido_object = MidiFile(path, clip=True)
    readable_track_df, begin_of_track, end_of_track = convert_to_axillary_representation(mido_object.tracks[1])
    mido_object.tracks[1] = convert_to_midi_track(readable_track_df.iloc[begin_i:end_i], begin_of_track, end_of_track)
    mido_object.save(target_path)


def determine_range(path):
    mido_object = MidiFile(path, clip=True)
    readable_track_df, begin_of_track, end_of_track = convert_to_axillary_representation(mido_object.tracks[1])
    return {"min_note": readable_track_df["note"].min(),
            "max_note": readable_track_df["note"].max()}
# endregion
