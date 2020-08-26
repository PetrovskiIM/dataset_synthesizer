import os
import pandas as pd
from scripts.midi.config import midi_files_copies_storage_path
from scripts.midi.format import convert_to_axillary_representation
from mido import MidiFile


def form_index(observation_meta):
    return f'{observation_meta["name"]}_' \
           f'{observation_meta["instrument"]}_' \
           f'{observation_meta["shift"]}_' \
           f'{observation_meta["begin_i"]}_' \
           f'{observation_meta["end_i"]}'


source_folders = [f"./data/maestro-v2.0.0/{year}" for year in
                  ["2004", "2006", "2008", "2009", "2011", "2013", "2014", "2015", "2017"]]



# region copying midi files
i = 0
observations = []
for source_folder in source_folders:
    folder_info = {"source_folder": source_folder}
    for root, directories, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith("mid") | file.lower().endswith("midi"):
                observation = dict()
                observation.update(folder_info)
                observation["name"] = file.split(".")[0]
                os.system(f'cp {root}/{file} {midi_files_copies_storage_path}/{observation["name"]}.mid')
                observations.append(observation)
                i += 1
                print(f"Copying observations from the provided folders...{str(i).ljust(4, ' ')}", end='\r')
print(f"Copying observations from the provided folders...{str(i).ljust(4, ' ')}. Done!.")
# endregion


dispatcher_df = pd.DataFrame.from_records(observations)[["source_folder", "name"]]
template_observations_meta = []
for template_observation_name in dispatcher_df["name"].values:
    MIDI_file_path = f"{midi_files_copies_storage_path}/{template_observation_name}.mid"
    mid_file = MidiFile(MIDI_file_path, clip=True)
    readable_track_df, begin_of_track, end_of_track = convert_to_axillary_representation(mid_file.tracks[1])
    meta = {"name": template_observation_name, "number_of_events": len(readable_track_df)}
    print(readable_track_df.iloc[:16])
    break
print("Done!")
# load all templates -> analysis -> train \ test split -> augmentation -> save

# print(dispatcher_df)
# steps_up: (aug_config[instrument] - max_note) // step,
# "steps_down": min_note // step,
