from multiprocessing import Pool
import pandas as pd
from config import instrument_pitch_bondaries, shift_step, \
    re_instrumented_chunked_copies_columns_with_shift_meta as template_names, \
    shifted_re_instrumented_chunked_copies_columns_with_shift_meta as names, \
    re_instrumented_chunked_copies_csv_path as template_csv_path, \
    shifted_re_instrumented_chunked_copies_csv_path as target_csv_path, \
    shifted_re_instrumented_chunked_copies_storage_path as target_storage_path
import augmentations

import warnings

warnings.simplefilter("ignore")

if __name__ == '__main__':
    target_storage_path.mkdir(parents=True, exist_ok=True)

    dispatcher_df = pd.read_csv(f"{template_csv_path}.csv", names=template_names)
    boundaries = pd.DataFrame.from_records(
        [instrument_pitch_bondaries[instrument]
         for instrument in dispatcher_df["instrument"].values])[["max_note", "min_note"]]
    dispatcher_df["up_boundary"] = boundaries["max_note"].values
    dispatcher_df["down_boundary"] = boundaries["min_note"].values

    dispatcher_df["shift"] = 0
    paths_df = dispatcher_df[["path"]].copy(deep=True)
    for shift in range(-127 // shift_step, 127 // shift_step):
        criterion_results = (dispatcher_df["max_note"] + shift_step * shift <= dispatcher_df["up_boundary"]) & \
                            (dispatcher_df["min_note"] + shift_step * shift >= dispatcher_df["down_boundary"])
        observations_in_range_for_current_shift = dispatcher_df.loc[criterion_results]
        if len(observations_in_range_for_current_shift) == 0:
            continue
        paths = paths_df.loc[criterion_results, "path"].values


        def f(path):
            augmentations.change_octave(f"{path}.mid",
                                        f"{target_storage_path}/{path.split('/')[-1]}_{shift}.mid", shift)


        with Pool(5) as p:
            p.map(f, paths)
        observations_in_range_for_current_shift["shift"] = shift
        observations_in_range_for_current_shift["path"] = [f"{target_storage_path}/{path.split('/')[-1]}_{shift}"
                                                           for path in paths]
        observations_in_range_for_current_shift[names].to_csv(f"{target_csv_path}.csv", index=False, header=False,
                                                              mode="a")
