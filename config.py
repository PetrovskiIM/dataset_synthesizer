import pathlib

ROOT_PATH = "./data"

instruments_list = ['Piano', 'EnglishHorn', 'ElectricOrgan', 'Harpsichord', 'PipeOrgan', 'Violin']
instrument_pitch_bondaries = {
    'Piano': {
        "max_note": 107,
        "min_note": 20
    },
    'EnglishHorn': {
        "max_note": 97,
        "min_note": 30
    },
    'ElectricOrgan': {
        "max_note": 97,
        "min_note": 3
    },
    'Harpsichord': {
        "max_note": 107,
        "min_note": 20
    },
    'PipeOrgan': {
        "max_note": 87,
        "min_note": 40
    },
    'Violin': {
        "max_note": 97,
        "min_note": 10
    }
}
template_paths = [f"/home/petrovskiyim/Projects/audio-representation/data/maestro-v2.0.0/{year}" for year in
                  ["2004", "2006", "2008", "2009", "2011", "2013", "2014", "2015", "2017"]]

n_chunks_per_midi = 2
chunk_size = 30
chunks = [{"begin_i": 30, "end_i": 60}, {"begin_i": 30, "end_i": 80}]

n_observations = 40000


copying_files_names = ["source_folder", "name", "path"]
chunked_files_names = copying_files_names + ["begin_i", "end_i"]
names_with_shift_meta = chunked_files_names + ["max_note", "min_note"]
instrument_files_names = names_with_shift_meta + ["instrument"]


midi_files_chunks_storage_path = f"{ROOT_PATH}/chunked"
midi_files_copies_storage_path = pathlib.Path(f"{ROOT_PATH}/cashed")

midi_files_copies_storage_path.mkdir(parents=True, exist_ok=True)

shifting_meta_csv_path = pathlib.Path(f"{ROOT_PATH}/chunked")

shifting_meta_csv_path.mkdir(parents=True, exist_ok=True)

copying_csv_path = midi_files_copies_storage_path
chunking_csv_path = f"{ROOT_PATH}/chunked"
csv_paths_with_shift_meta = copying_csv_path

different_instrument_csv_path = f"{ROOT_PATH}/final"
different_instrument_storage_path = pathlib.Path(f"{ROOT_PATH}/final")
different_instrument_storage_path.mkdir(parents=True, exist_ok=True)


train_wav_storage_path = pathlib.Path(f"{ROOT_PATH}/aug")
train_wav_storage_path.mkdir(parents=True, exist_ok=True)
test_wav_storage_path = pathlib.Path(f"{ROOT_PATH}/aug_test")
test_wav_storage_path.mkdir(parents=True, exist_ok=True)

