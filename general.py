import os
import pandas as pd
from multiprocessing import Pool
import pathlib
import augmentations
from config import instruments_list, instrument_pitch_bondaries, chunks
import numpy as np
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


def shift_to_index(shift):
    return f'{shift}'


midi_files_copies_storage_path = pathlib.Path("/home/petrovskiyim/Projects/audio_representaion/data/cashed")
midi_files_copies_storage_path.mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    source_folders = [f"/home/petrovskiyim/Projects/audio-representation/data/maestro-v2.0.0/{year}" for year in
                      ["2004", "2006", "2008", "2009", "2011", "2013", "2014", "2015", "2017"]]

    # region copying midi files
    i = 0
    observations = []
    for source_folder in source_folders:
        folder_info = {"source_folder": source_folder}
        for root, directories, files in os.walk(source_folder):
            for file in files[:10]:
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
    dispatcher_df = pd.DataFrame.from_records(observations)
    # region cut chunks
    template_df = dispatcher_df
    template_folder = midi_files_copies_storage_path
    names = template_df["name"].values

    current_columns_names = ["source_folder", "name", "begin_i", "end_i"]

    dispatcher = []
    for chunk in chunks:
        target_folder = pathlib.Path(f"{template_folder}/{chunk_to_index(chunk)}")
        target_folder.mkdir(parents=True, exist_ok=True)


        def f(x):
            augmentations.cut_chunk(f"{template_folder}/{x}.mid", f"{target_folder}/{x}.mid", **chunk)


        with Pool(5) as p:
            print(p.map(f, names))
        template_df["begin_i"] = chunk["begin_i"]
        template_df["end_i"] = chunk["end_i"]
        template_df.to_csv(f"{target_folder}.csv")
        dispatcher.append(template_df[current_columns_names].values)
    # endregion
    dispatcher_df = pd.DataFrame(np.concatenate(dispatcher), columns=current_columns_names)
    # region itterativly collect step_up step_down meta
    ranges = []
    for name, begin_i, end_i in dispatcher_df[["name", "begin_i", "end_i"]].values:
        target_folder = pathlib.Path(
            f'{template_folder}/{chunk_to_index({"begin_i": begin_i, "end_i": end_i})}/{name}.mid')
        ranges.append(augmentations.determine_range(target_folder))
    ranges_df = pd.DataFrame.from_records(ranges)
    dispatcher_df["max_note"], dispatcher_df["min_note"] = ranges_df["max_note"], ranges_df["min_note"]
    # endregion

    # region change instrument
    dispatcher = []
    current_columns_names.append("instrument")
    for instrument in instruments_list:
        boundaries = instrument_pitch_bondaries[instrument]
        observations_in_range = dispatcher_df.loc[(dispatcher_df["max_note"] <= boundaries["max_note"]) &
                                                  (dispatcher_df["min_note"] >= boundaries["min_note"])]
        if len(observations_in_range) == 0:
            print("no observation in range")
            continue

        folder_and_name = [(f'{chunk_to_index({"begin_i": begin_i, "end_i": end_i})}',name)
                           for begin_i, end_i, name in dispatcher_df[["begin_i", "end_i","name"]].values]
        for chunk in chunks:
            target_folder = pathlib.Path(f"{template_folder}/{chunk_to_index(chunk)}/{instrument}")
            target_folder.mkdir(parents=True, exist_ok=True)

        print(folder_and_name)


        def f(x):
            augmentations.change_instrument(f"{template_folder}/{x[0]}/{x[1]}.mid",
                                            f"{target_folder}/{x[0]}/{instrument}/{x[1]}.mid", instrument)


        with Pool(5) as p:
            print(p.map(f, folder_and_name))
        dispatcher_df["instrument"] = instrument
        dispatcher.append(dispatcher_df[current_columns_names].values)
    # endregion
    dispatcher_df = pd.DataFrame(np.concatenate(dispatcher), columns=current_columns_names)
    # region change pitch
    dispatcher = []
    current_columns_names.append("shift")
    dispatcher_df[["up_boundary", "down_bondary"]] = \
        pd.DataFrame.from_records(
            [instrument_pitch_bondaries[instrument] for instrument in dispatcher_df["instrument"].values])[
            ["max_note", "min_note"]]
    for shift in range(-int(max(dispatcher_df["note"].min() - min, 0) // 7),
                       int((127 - dispatcher_df["note"].max()) // 7)):
        observations_in_range_for_current_shift = \
            dispatcher_df.loc[(dispatcher_df["max_note"] + 7 * shift <= dispatcher_df["up_boundary"]) &
                              (dispatcher_df["min_note"] + 7 * shift >= dispatcher_df["down_bondary"])]

        folder_and_name = \
            zip([f'{chunk_to_index({"begin_i": begin_i, "end_i": end_i})}/{instrument}'
                 for begin_i, end_i, instrument in
                 observations_in_range_for_current_shift[["begin_i", "end_i", "instrument"]]],
                observations_in_range_for_current_shift["name"])


        def f(x):
            augmentations.change_octave(f"{template_folder}/{x[0]}/{x[1]}.mid",
                                        f"{target_folder}/{x[0]}/{instrument}/{x[1]}.mid", shift)


        with Pool(5) as p:
            print(p.map(f, folder_and_name))
        observations_in_range_for_current_shift["shift"] = shift
        dispatcher.append(observations_in_range_for_current_shift[current_columns_names].values)
    dispatcher_df = pd.DataFrame(np.concatenate(dispatcher), columns=current_columns_names)
    dispatcher_df.to_csv("cur.csv")
