from scripts.midi.config import midi_files_copies_storage_path, \
    templates_storage_path, wav_storage_path, \
    train_wav_path, test_wav_path, instrument_pitch_bondaries, instruments_list, n_chunks_per_midi, chunk_size, \
    n_observations
import os
import subprocess
import pandas as pd
from scripts.midi.format import convert_to_axillary_representation, convert_to_midi_track, \
    count_down_steps, count_up_steps
from scripts.midi.augmentations import change_instrument_in_mid
from mido import MidiFile
import pathlib
import warnings

warnings.simplefilter("ignore")

begin_i, end_i = 0, 10
first = True
observations_counter = 0
partition = "train"


template_observations_storage_path = pathlib.Path(
    str(templates_storage_path) + "/" + str(begin_i) + str(end_i))
template_observations_storage_path.mkdir(parents=True, exist_ok=True)

dispatcher_df = pd.read_csv(f"{midi_files_copies_storage_path}.csv",
                            names=["source_folder", "name"]).to_dict("records")

# region create test\train csv with header
names = ['index', 'name', 'source_folder', 'note_shift', 'min_note', 'max_note', 'chunk_index', 'instrument']
if (partition == "train") & first:
    pd.DataFrame.from_records([{name: name for name in names}])[names].to_csv(f"{train_wav_path}.csv",
                                                                              index=False, header=False)
if partition == "test":
    pd.DataFrame.from_records([{name: name for name in names}]).to_csv(f"{test_wav_path}.csv", index=False,
                                                                       header=False)
# endregions

clean_up_cashe = True


varied_observations_meta = []
n_templates_observations = len(dispatcher_df)
for observation_id in range(max(int(begin_i), 0), min(int(end_i), len(dispatcher_df))):
    observation_meta = dispatcher_df[observation_id]
    if observations_counter > n_observations:
        break
    MIDI_file_path = f"{midi_files_copies_storage_path}/{str(observation_meta['name'])}.mid"
    mid_file = MidiFile(MIDI_file_path, clip=True)
    readable_track_df, begin_of_track, end_of_track = convert_to_axillary_representation(mid_file.tracks[1])
    lower_bound, upper_bound = -count_down_steps(readable_track_df, min=0), count_up_steps(readable_track_df)
    for note_shift in range(lower_bound, upper_bound):
        midi_representation = MidiFile(MIDI_file_path, clip=True)
        readable_track_df, begin_of_track, end_of_track = \
            convert_to_axillary_representation(midi_representation.tracks[1])
        readable_track_df["note"] += 7 * note_shift
        for chunk_index in range(1, min(len(readable_track_df) // chunk_size, n_chunks_per_midi)):
            midi_representation.tracks[1] = \
                convert_to_midi_track(
                    readable_track_df.iloc[chunk_index * chunk_size:(chunk_index + 1) * chunk_size],
                    begin_of_track,
                    end_of_track)
            for instrument in instruments_list:
                if observations_counter > n_observations:
                    break
                if (readable_track_df["note"].min() < instrument_pitch_bondaries[instrument]["min_note"]) | \
                        (readable_track_df["note"].max() > instrument_pitch_bondaries[instrument]["max_note"]):
                    continue
                change_instrument_in_mid(midi_representation, instrument).save(f'{template_observations_storage_path}/{observations_counter}.mid')
                subprocess.run(f'timidity --output-24bit -A120 {template_observations_storage_path}/{observations_counter}.mid -Ow -o {wav_storage_path}/{observations_counter}.wav',
                    shell=True, capture_output=True)

                print(f"[ID]{str(observation_id).rjust(4, ' ')}/{n_templates_observations}"
                      f"[shift]{str(note_shift).rjust(2, ' ')} in "  # |=\=
                      f"[{str(lower_bound).rjust(2, ' ')}, {str(upper_bound).rjust(2, ' ')}]"
                      f"[chunk]{str(chunk_index).rjust(3, ' ')} in "  # |=\=
                      f"[1, {min(len(readable_track_df) // chunk_size, n_chunks_per_midi)}]"
                      f"[instrument]{str(instrument).rjust(14, ' ')} in {instruments_list}"
                      f"[Total]{str(observations_counter).rjust(6, ' ')}", end='\r')

                # region collecting augmentation meta
                varied_observation_meta = dict()
                varied_observation_meta.update(observation_meta)
                varied_observation_meta.update({
                    "index": observations_counter,
                    "note_shift": note_shift,
                    "min_note": readable_track_df["note"].min(),
                    "max_note": readable_track_df["note"].max()
                })
                varied_observation_meta["chunk_index"] = chunk_index
                varied_observation_meta["instrument"] = instrument
                # endregion
                if partition == "train":
                    path = train_wav_path
                else:
                    path = test_wav_path
                pd.DataFrame.from_records([varied_observation_meta])[names] \
                    .to_csv(f"{path}.csv", index=False, header=False, mode='a')
                os.system(f"mv {wav_storage_path}/{observations_counter}.wav {path}/{observations_counter}.wav")
                observations_counter += 1
print("Done!")
