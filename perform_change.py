from multiprocessing import Pool
import pandas as pd
import augmentations
from config import instruments_list, instrument_pitch_bondaries, \
    names_with_shift_meta as template_names, \
    midi_files_chunks_storage_path as template_storage_path, \
    midi_files_chunks_storage_path as target_path, \
    shifting_meta_csv_path as template_csv_path

import warnings

warnings.simplefilter("ignore")

if __name__ == '__main__':
    dispatcher_df = pd.read_csv(f"{template_csv_path}.csv", names=template_names)

    # region change instrument
    dispatcher = []
    for instrument in instruments_list:
        boundaries = instrument_pitch_bondaries[instrument]
        observations_in_range = dispatcher_df.loc[(dispatcher_df["max_note"] <= boundaries["max_note"]) &
                                                  (dispatcher_df["min_note"] >= boundaries["min_note"])]
        if len(observations_in_range) == 0:
            print("no observation in range")
            continue

        folder_and_name = [(f'{chunk_to_index({"begin_i": begin_i, "end_i": end_i})}', name)
                           for begin_i, end_i, name in dispatcher_df[["begin_i", "end_i", "name"]].values]
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