from multiprocessing import Pool
import subprocess
from config import train_wav_storage_path as wav_storage_path, \
    shifted_re_instrumented_chunked_copies_csv_path as template_csv_path, \
    shifted_re_instrumented_chunked_copies_columns_with_shift_meta as template_names
import pandas as pd


def waviolize(path):
    subprocess.run(
        f'timidity --output-24bit -A120 {path}.mid -Ow -o {wav_storage_path}/{path.split("/")[-1]}.wav',
        shell=True, capture_output=True)


if __name__ == '__main__':
    wav_storage_path.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(f"{template_csv_path}.csv", names=template_names)
    paths = df["path"].values

    with Pool(5) as p:
        p.map(waviolize, paths)
    df["path"] = [f'{wav_storage_path}/{path.split("/")[-1]}' for path in paths]
    df[template_names].to_csv(f"{wav_storage_path}.csv", index=False)
