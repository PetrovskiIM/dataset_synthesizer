from multiprocessing import Pool
import pandas as pd
import augmentations
from config import copying_files_names as template_names, \
    midi_files_copies_storage_path as template_storage_path, \
    chunks, \
    chunked_files_names as names, \
    midi_files_chunks_storage_path as target_path, \
    chunking_csv_path as target_csv_path
import warnings

warnings.simplefilter("ignore")

if __name__ == '__main__':
    dispatcher_df = pd.read_csv(f"{template_storage_path}.csv", names=template_names)
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
