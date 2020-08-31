import os
import pandas as pd
import pathlib
from config import template_paths, \
    copying_files_names as names, \
    midi_files_copies_storage_path as storage_path, \
    copying_csv_path as target_csv_path

import warnings

warnings.simplefilter("ignore")


def form_index(observation_meta):
    return f'{observation_meta["name"]}_' \
           f'{observation_meta["instrument"]}_' \
           f'{observation_meta["shift"]}_' \
           f'{observation_meta["begin_i"]}_' \
           f'{observation_meta["end_i"]}'


def chunk_to_index(chunk):
    return f'{chunk["begin_i"]}_{chunk["end_i"]}'



midi_files_copies_storage_path = pathlib.Path("/home/petrovskiyim/Projects/audio_representaion/data/cashed")
midi_files_copies_storage_path.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':

    i = 0
    observations = []
    for source_folder in template_paths:
        folder_info = {"source_folder": source_folder}
        for root, directories, files in os.walk(source_folder):
            for file in files[:10]:
                if file.lower().endswith("mid") | file.lower().endswith("midi"):
                    observation = dict()
                    observation.update(folder_info)
                    observation["name"] = file.split(".")[0]
                    os.system(f'cp {root}/{file} {storage_path}/{observation["name"]}.mid')
                    observation["path"] = f"{storage_path}/{observation['name']}.mid"
                    pd.DataFrame.from_records([observation])[names]\
                        .to_csv(f"{target_csv_path}.csv", index=False, header=False, mode='a')
                    observations.append(observation)
                    i += 1
                    print(f"Copying observations from the provided folders...{str(i).ljust(4, ' ')}", end='\r')
    print(f"Copying observations from the provided folders...{str(i).ljust(4, ' ')}. Done!.")
