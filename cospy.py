# import os
# import pandas as pd
# from scripts.midi.config import midi_files_copies_storage_path
#
#
# source_folders = [f"./data/maestro-v2.0.0/{year}" for year in
#                   ["2004", "2006", "2008", "2009", "2011", "2013", "2014", "2015", "2017"]]
#
# # region copying midi files
# i = 0
# observations = []
# for source_folder in source_folders:
#     folder_info = {"source_folder": source_folder}
#     for root, directories, files in os.walk(source_folder):
#         for file in files:
#             if file.lower().endswith("mid") | file.lower().endswith("midi"):
#                 observation = dict()
#                 observation.update(folder_info)
#                 observation["name"] = file.split(".")[0]
#                 os.system(f'cp {root}/{file} {midi_files_copies_storage_path}/{observation["name"]}.mid')
#                 observations.append(observation)
#                 i += 1
#                 print(f"Copying observations from the provided folders...{str(i).ljust(4, ' ')}", end='\r')
# print("Copying observations from the provided folders... Done!")
# # endregion
#
# pd.DataFrame.from_records(observations)[["source_folder", "name"]].to_csv(f"{midi_files_copies_storage_path}.csv", header=False, index=False)
