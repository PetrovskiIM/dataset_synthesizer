import os
import pandas as pd
from config import template_paths, \
    copies_columns as names, \
    copies_storage_path as storage_path, \
    copies_csv_path as target_csv_path
import warnings

warnings.simplefilter("ignore")

if __name__ == '__main__':
    storage_path.mkdir(parents=True, exist_ok=True)

    i = 0
    observations = []
    for source_folder in template_paths:
        folder_info = {"source_folder": source_folder}
        for root, directories, files in os.walk(source_folder):
            for file in files:
                if file.lower().endswith("mid") | file.lower().endswith("midi"):
                    observation = dict()
                    observation.update(folder_info)
                    observation["name"] = file.split(".")[0]
                    os.system(f'cp {root}/{file} {storage_path}/{observation["name"]}.mid')
                    observation["path"] = f"{storage_path}/{observation['name']}.mid"
                    pd.DataFrame.from_records([observation])[names]\
                        .to_csv(f"{target_csv_path}.csv", index=False, header=False, mode='a')
                    observations.append(observation)
                    i += 1
                    print(f"Copying observations from the provided folders...{str(i).ljust(4, ' ')}", end='\r')
    print(f"Copying observations from the provided folders...{str(i).ljust(4, ' ')}. Done!.")
