import cv2
from transform import direct_transform
from multiprocessing import Pool
from config import train_wav_storage_path, test_wav_storage_path
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv(f"{train_wav_storage_path}.csv")

    paths = df.loc[in_train_records.values, "path"].values
    with Pool(5) as p:
        p.map(waviolize_train, paths)
    df.loc[in_train_records.values].to_csv(f"{train_wav_storage_path}.csv")
    in_test_records = (df["name"] != in_train_names[0])
    for name in in_train_names:
        in_test_records = in_test_records & (df["name"] != name)
    for name in out_names:
        in_test_records = in_test_records & (df["name"] != name)
    paths = df.loc[in_test_records.values, "path"].values
    with Pool(5) as p:
        p.map(waviolize_test, paths)
    df.loc[in_test_records.values].to_csv(f"{test_wav_storage_path}.csv")
