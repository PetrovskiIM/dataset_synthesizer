import pathlib
#
# templates_storage_path = pathlib.Path(f"./data/template")
# midi_files_copies_storage_path = pathlib.Path(f"./data/casted")
# wav_storage_path = pathlib.Path(f"./data/aug_wav")
# train_wav_path, test_wav_path = pathlib.Path(f"./data/for_demo"), pathlib.Path(f"./data/aug_test")
# pathes = [templates_storage_path, midi_files_copies_storage_path, train_wav_path, test_wav_path, wav_storage_path]
# for path in pathes:
#     path.mkdir(parents=True, exist_ok=True)

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

n_chunks_per_midi = 2
chunk_size = 30
chunks = [{"begin_i":30, "end_i":60}, {"begin_i":30, "end_i":80}]

n_observations = 40000