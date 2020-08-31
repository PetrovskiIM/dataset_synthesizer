from multiprocessing import Pool
import subprocess
from config import train_wav_storage_path, test_wav_storage_path, \
    shifted_re_instrumented_chunked_copies_csv_path as template_csv_path, \
    shifted_re_instrumented_chunked_copies_columns_with_shift_meta as template_names
import pandas as pd


def waviolize_train(path):
    subprocess.run(
        f'timidity --output-24bit -A120 {path}.mid -Ow -o {train_wav_storage_path}/{path.split("/")[-1]}.wav',
        shell=True, capture_output=True)


def waviolize_test(path):
    subprocess.run(
        f'timidity --output-24bit -A120 {path}.mid -Ow -o {test_wav_storage_path}/{path.split("/")[-1]}.wav',
        shell=True, capture_output=True)


if __name__ == '__main__':
    train_wav_storage_path.mkdir(parents=True, exist_ok=True)
    test_wav_storage_path.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(f"{template_csv_path}.csv", names=template_names)
    unique_names = df["name"].value_counts().index.values
    in_train_names = unique_names[:100]
    in_test_names = unique_names[100:101]
    train_in_out_names = unique_names[100:]
    out_names = unique_names[101:]
    in_train_records = (df["name"] != in_test_names[0])
    for name in in_test_names:
        in_train_records = in_train_records & (df["name"] != name)
    for name in out_names:
        in_train_records = in_train_records & (df["name"] != name)

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
