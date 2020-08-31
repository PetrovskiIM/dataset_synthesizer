from multiprocessing import Pool
import pandas as pd
import augmentations
from config import chunks, \
    copies_columns as template_names, \
    chunked_copies_columns as names, \
    copies_storage_path as template_storage_path, \
    chunked_copies_storage_path as target_path, \
    copies_csv_path as template_csv_path, \
    chunked_copies_csv_path as target_csv_path
import warnings

warnings.simplefilter("ignore")

if __name__ == '__main__':
    target_path.mkdir(parents=True, exist_ok=True)

    dispatcher_df = pd.read_csv(f"{template_csv_path}.csv", names=template_names)
    names_of_files = dispatcher_df["name"].values
    for chunk_i, chunk in enumerate(chunks):
        def f(x):
            augmentations.cut_chunk(f"{template_storage_path}/{x}.mid",
                                    f"{target_path}/{x}_{chunk['begin_i']}_{chunk['end_i']}.mid", **chunk)

        with Pool(5) as p:
            p.map(f, names_of_files)
        dispatcher_df["begin_i"] = chunk["begin_i"]
        dispatcher_df["end_i"] = chunk["end_i"]
        dispatcher_df["path"] = \
            [f"{target_path}/{name}_{chunk['begin_i']}_{chunk['end_i']}" for name in names_of_files]
        dispatcher_df[names].to_csv(f"{target_csv_path}.csv", index=False, header=False, mode='a')
