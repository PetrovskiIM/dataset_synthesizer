import pathlib
import yaml

ROOT = "./data"
sample_length = 128
with open("./configs/transforms/nfft2048_hop256_sr22050_mel128_n.yaml", 'r') as transform_config_file:
    try:
        melspectrogram_transform_parameters, normalization_parameters = yaml.safe_load(transform_config_file).values()
    except yaml.YAMLError as exc:
        print(exc)
        exit()

# region instrument configs
instruments_list = ['Piano', 'EnglishHorn', 'ElectricOrgan', 'Harpsichord', 'PipeOrgan', 'Violin']
# instrument_pitch_bondaries = {
#     'Piano': {
#         "max_note": 107,
#         "min_note": 20
#     },
#     'EnglishHorn': {
#         "max_note": 97,
#         "min_note": 30
#     },
#     'ElectricOrgan': {
#         "max_note": 97,
#         "min_note": 3
#     },
#     'Harpsichord': {
#         "max_note": 107,
#         "min_note": 20
#     },
#     'PipeOrgan': {
#         "max_note": 87,
#         "min_note": 40
#     },
#     'Violin': {
#         "max_note": 97,
#         "min_note": 10
#     }
# }

instrument_pitch_bondaries = {
    'Piano': {
        "max_note": 105,
        "min_note": 25
    },
    'EnglishHorn': {
        "max_note": 105,
        "min_note": 25
    },
    'ElectricOrgan': {
        "max_note": 105,
        "min_note": 25
    },
    'Harpsichord': {
        "max_note": 105,
        "min_note": 25
    },
    'PipeOrgan': {
        "max_note": 105,
        "min_note": 25
    },
    'Violin': {
        "max_note": 105,
        "min_note": 25
    }
}
template_paths = [f"/home/petrovskiyim/Projects/audio-representation/data/maestro-v2.0.0/{year}" for year in
                  ["2004", "2006", "2008", "2009", "2011", "2013", "2014", "2015", "2017"]]
# endregion

# n_chunks = 2
chunk_size = 30
chunks = [{"begin_i": 30, "end_i": 60}]#, {"begin_i": 30, "end_i": 80}]
n_observations = 40000


copies_columns = ["source_folder", "name", "path"]
chunked_copies_columns = copies_columns + ["begin_i", "end_i"]
columns_with_shift_meta = chunked_copies_columns + ["max_note", "min_note"]
re_instrumented_chunked_copies_columns_with_shift_meta = columns_with_shift_meta + ["instrument"]
shifted_re_instrumented_chunked_copies_columns_with_shift_meta = \
    re_instrumented_chunked_copies_columns_with_shift_meta + ["shift"]


copies_storage_path = pathlib.Path(f"{ROOT}/copies")
chunked_copies_storage_path = pathlib.Path(f"{ROOT}/chunked_copies")
re_instrumented_chunked_copies_storage_path = pathlib.Path(f"{ROOT}/re_instrumented_chunked_copies")
shifted_re_instrumented_chunked_copies_storage_path = pathlib.Path(f"{ROOT}/shifted_re_instrumented_chunked_copies")

train_wav_storage_path = pathlib.Path(f"{ROOT}/aug")
test_wav_storage_path = pathlib.Path(f"{ROOT}/aug_test")


copies_csv_path = copies_storage_path
chunked_copies_csv_path = chunked_copies_storage_path
csv_paths_with_shift_meta = chunked_copies_csv_path
re_instrumented_chunked_copies_csv_path = re_instrumented_chunked_copies_storage_path
shifted_re_instrumented_chunked_copies_csv_path = shifted_re_instrumented_chunked_copies_storage_path
