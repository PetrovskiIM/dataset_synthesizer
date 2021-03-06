import pandas as pd
import augmentations
from config import chunked_copies_columns as template_names, \
    columns_with_shift_meta as names, \
    chunked_copies_csv_path as template_path, \
    csv_paths_with_shift_meta as target_csv_path

import warnings

warnings.simplefilter("ignore")

if __name__ == '__main__':
    dispatcher_df = pd.read_csv(f"{template_path}.csv", names=template_names)
    ranges = [augmentations.determine_range(f"{path}.mid") for path in dispatcher_df["path"].values]
    ranges_df = pd.DataFrame.from_records(ranges)
    dispatcher_df["max_note"], dispatcher_df["min_note"] = ranges_df["max_note"], ranges_df["min_note"]
    dispatcher_df[names].to_csv(f"{target_csv_path}.csv", index=False, header=False)
