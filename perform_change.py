from multiprocessing import Pool
import pandas as pd
from config import instruments_list, instrument_pitch_bondaries, \
    columns_with_shift_meta as template_names, \
    re_instrumented_chunked_copies_columns_with_shift_meta as names, \
    csv_paths_with_shift_meta as template_csv_path, \
    re_instrumented_chunked_copies_csv_path as target_csv_path, \
    re_instrumented_chunked_copies_storage_path as target_storage_path
import augmentations

import warnings

warnings.simplefilter("ignore")

if __name__ == '__main__':
    target_storage_path.mkdir(parents=True, exist_ok=True)

    dispatcher_df = pd.read_csv(f"{template_csv_path}.csv", names=template_names)
    dispatcher_df["instrument"] = "Piano"
    path_df = dispatcher_df["path"].copy(deep=True)

    for instrument in instruments_list:
        boundaries = instrument_pitch_bondaries[instrument]
        observations_in_range = dispatcher_df.loc[(dispatcher_df["max_note"] <= boundaries["max_note"]) &
                                                  (dispatcher_df["min_note"] >= boundaries["min_note"])]
        paths = path_df[(dispatcher_df["max_note"] <= boundaries["max_note"]) &
                        (dispatcher_df["min_note"] >= boundaries["min_note"])].values
        if len(paths) == 0:
            print("no observation in range")
            continue

        def f(x):
            augmentations.change_instrument(f"{x}.mid",
                                            f"{target_storage_path}/{x.split('/')[-1]}_{instrument}.mid", instrument)
        with Pool(5) as p:
            p.map(f, paths)

        observations_in_range["instrument"] = instrument
        observations_in_range["path"] = [f"{target_storage_path}/{path.split('/')[-1]}_{instrument}" for path in paths]
        observations_in_range[names].to_csv(f"{target_csv_path}.csv", index=False, header=False, mode='a')
