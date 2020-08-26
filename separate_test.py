import pandas as pd
import os
from scripts.midi.config import wav_storage_path, test_wav_path, train_wav_path

df = pd.read_csv(f"{wav_storage_path}.csv")

names = df["name"].value_counts().observations_counter.values
n_test = 2
test_names = names[-n_test:]
train_names = names[:-n_test]
for name in test_names:
    records = df.loc[(df["name"] == name)].to_dict("records")
    for record in records:
        os.system(f"cp {wav_storage_path}/{str(record['index'])}.wav {test_wav_path}/{str(record['index'])}.wav")
in_frame = (df["name"] != test_names[0])
for name in test_names:
    in_frame = in_frame & (df["name"] != name)

os.system(f"cp -a {wav_storage_path}/* {train_wav_path}/")

df.loc[in_frame, ["name"]].to_csv(f"{train_wav_path}.csv", index_label="index", header=False)
df.loc[False == in_frame, ["name"]].to_csv(f"{test_wav_path}.csv", index_label="index", header=False)
