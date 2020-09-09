import pathlib
import yaml
import os

ROOT = os.path.join(os.getenv('HOME'), "datasets")

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
template_paths = [f"{ROOT}/maestro-v2.0.0/{year}" for year in
                  ["2004", "2006", "2008", "2009", "2011", "2013", "2014", "2015", "2017"]]
# endregion

# n_chunks = 2
chunk_size = 30
chunks = [{"begin_i": 30, "end_i": 90}]  # , {"begin_i": 30, "end_i": 80}]
n_observations = 40000

shift_step = 2

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

# casted_observations = [
#     'MIDI-Unprocessed_08_R2_2006_01_ORIG_MID--AUDIO_08_R2_2006_01_Track01_wav',
#     'MIDI-Unprocessed_25_R3_2011_MID--AUDIO_R3-D9_02_Track02_wav',
#     'MIDI-Unprocessed_07_R1_2008_01-04_ORIG_MID--AUDIO_07_R1_2008_wav--4',
#     'MIDI-Unprocessed_03_R1_2009_03-08_ORIG_MID--AUDIO_03_R1_2009_03_R1_2009_05_WAV',
#     'ORIG-MIDI_02_7_8_13_Group__MID--AUDIO_11_R2_2013_wav--3',
#     'MIDI-Unprocessed_21_R1_2011_MID--AUDIO_R1-D8_07_Track07_wav',
#     'MIDI-Unprocessed_11_R3_2008_01-04_ORIG_MID--AUDIO_11_R3_2008_wav--2',
#     'MIDI-Unprocessed_19_R2_2009_01_ORIG_MID--AUDIO_19_R2_2009_19_R2_2009_03_WAV',
#     'MIDI-Unprocessed_R1_D1-1-8_mid--AUDIO-from_mp3_03_R1_2015_wav--4',
#     'ORIG-MIDI_01_7_8_13_Group__MID--AUDIO_02_R2_2013_wav--5',
#     'MIDI-Unprocessed_14_R1_2006_01-05_ORIG_MID--AUDIO_14_R1_2006_04_Track04_wav',
#     'MIDI-Unprocessed_19_R1_2006_01-07_ORIG_MID--AUDIO_19_R1_2006_01_Track01_wav',
#     'ORIG-MIDI_02_7_10_13_Group_MID--AUDIO_11_R3_2013_wav--1',
#     'MIDI-UNPROCESSED_21-22_R1_2014_MID--AUDIO_21_R1_2014_wav--2',
#     'MIDI-Unprocessed_R1_D2-13-20_mid--AUDIO-from_mp3_17_R1_2015_wav--1',
#     'MIDI-Unprocessed_SMF_17_R1_2004_01-02_ORIG_MID--AUDIO_20_R2_2004_06_Track06_wav',
#     'MIDI-Unprocessed_21_R1_2011_MID--AUDIO_R1-D8_10_Track10_wav',
#     'MIDI-Unprocessed_074_PIANO074_MID--AUDIO-split_07-08-17_Piano-e_2-04_wav--1',
#     'ORIG-MIDI_03_7_8_13_Group__MID--AUDIO_17_R2_2013_wav--3',
#     'MIDI-Unprocessed_R1_D1-1-8_mid--AUDIO-from_mp3_05_R1_2015_wav--3',
#     'MIDI-Unprocessed_048_PIANO048_MID--AUDIO-split_07-06-17_Piano-e_2-05_wav--1',
#     'MIDI-Unprocessed_09_R2_2008_01-05_ORIG_MID--AUDIO_09_R2_2008_wav--3',
#     'MIDI-Unprocessed_04_R3_2011_MID--AUDIO_R3-D2_05_Track05_wav',
#     'MIDI-Unprocessed_04_R1_2011_MID--AUDIO_R1-D2_02_Track02_wav',
#     'ORIG-MIDI_01_7_6_13_Group__MID--AUDIO_03_R1_2013_wav--3',
#     'MIDI-Unprocessed_08_R1_2006_01-04_ORIG_MID--AUDIO_08_R1_2006_Disk1_02_Track02_wav',
#     'ORIG-MIDI_03_7_6_13_Group__MID--AUDIO_10_R1_2013_wav--3',
#     'MIDI-Unprocessed_071_PIANO071_MID--AUDIO-split_07-08-17_Piano-e_1-04_wav--4',
#     'MIDI-Unprocessed_14_R1_2009_06-08_ORIG_MID--AUDIO_14_R1_2009_14_R1_2009_08_WAV',
#     'MIDI-Unprocessed_059_PIANO059_MID--AUDIO-split_07-07-17_Piano-e_2-03_wav--1',
#     'MIDI-Unprocessed_09_R1_2009_01-04_ORIG_MID--AUDIO_09_R1_2009_09_R1_2009_04_WAV',
#     'MIDI-Unprocessed_17_R1_2009_01-03_ORIG_MID--AUDIO_17_R1_2009_17_R1_2009_03_WAV',
#     'MIDI-UNPROCESSED_21-22_R1_2014_MID--AUDIO_22_R1_2014_wav--2',
#     'MIDI-Unprocessed_R2_D1-2-3-6-7-8-11_mid--AUDIO-from_mp3_03_R2_2015_wav--1',
#     'MIDI-Unprocessed_11_R2_2008_01-05_ORIG_MID--AUDIO_11_R2_2008_wav--2',
#     'ORIG-MIDI_01_7_6_13_Group__MID--AUDIO_04_R1_2013_wav--1',
#     'MIDI-Unprocessed_13_R1_2006_01-06_ORIG_MID--AUDIO_13_R1_2006_05_Track05_wav',
#     'MIDI-Unprocessed_17_R2_2008_01-04_ORIG_MID--AUDIO_17_R2_2008_wav--2',
#     'MIDI-Unprocessed_066_PIANO066_MID--AUDIO-split_07-07-17_Piano-e_3-02_wav--1',
#     'MIDI-Unprocessed_19_R1_2006_01-07_ORIG_MID--AUDIO_19_R1_2006_03_Track03_wav',
#     'MIDI-Unprocessed_03_R3_2011_MID--AUDIO_R3-D1_07_Track07_wav',
#     'MIDI-UNPROCESSED_16-18_R1_2014_MID--AUDIO_16_R1_2014_wav--1',
#     'ORIG-MIDI_02_7_7_13_Group__MID--AUDIO_15_R1_2013_wav--4',
#     'MIDI-UNPROCESSED_04-08-12_R3_2014_MID--AUDIO_08_R3_2014_wav',
#     'MIDI-UNPROCESSED_19-20_R1_2014_MID--AUDIO_19_R1_2014_wav--8',
#     'MIDI-Unprocessed_SMF_12_01_2004_01-05_ORIG_MID--AUDIO_12_R1_2004_10_Track10_wav',
#     'MIDI-Unprocessed_04_R1_2009_04-06_ORIG_MID--AUDIO_04_R1_2009_04_R1_2009_05_WAV',
#     'MIDI-UNPROCESSED_06-08_R1_2014_MID--AUDIO_07_R1_2014_wav--6',
#     'MIDI-Unprocessed_065_PIANO065_MID--AUDIO-split_07-07-17_Piano-e_3-01_wav--1',
#     'MIDI-Unprocessed_15_R1_2011_MID--AUDIO_R1-D6_10_Track10_wav',
#     'MIDI-Unprocessed_25_R3_2011_MID--AUDIO_R3-D9_06_Track06_wav',
#     'MIDI-Unprocessed_04_R2_2008_01-04_ORIG_MID--AUDIO_04_R2_2008_wav--4',
#     'MIDI-Unprocessed_09_R2_2008_01-05_ORIG_MID--AUDIO_09_R2_2008_wav--5',
#     'ORIG-MIDI_01_7_7_13_Group__MID--AUDIO_11_R1_2013_wav--1',
#     'MIDI-UNPROCESSED_21-22_R1_2014_MID--AUDIO_21_R1_2014_wav--4',
#     'MIDI-Unprocessed_08_R1_2008_01-05_ORIG_MID--AUDIO_08_R1_2008_wav--5',
#     'ORIG-MIDI_03_7_8_13_Group__MID--AUDIO_19_R2_2013_wav--4',
#     'MIDI-Unprocessed_05_R1_2011_MID--AUDIO_R1-D2_12_Track12_wav',
#     'MIDI-Unprocessed_SMF_17_R1_2004_01-03_ORIG_MID--AUDIO_17_R1_2004_02_Track02_wav--1',
#     'MIDI-Unprocessed_17_R3_2011_MID--AUDIO_R3-D6_06_Track06_wav',
#     'MIDI-UNPROCESSED_01-03_R1_2014_MID--AUDIO_02_R1_2014_wav--2',
#     'MIDI-Unprocessed_25_R2_2011_MID--AUDIO_R2-D6_07_Track07_wav',
#     'MIDI-Unprocessed_12_R3_2011_MID--AUDIO_R3-D4_02_Track02_wav',
#     'MIDI-Unprocessed_SMF_17_R1_2004_04_ORIG_MID--AUDIO_17_R1_2004_09_Track09_wav',
#     'MIDI-Unprocessed_R1_D2-21-22_mid--AUDIO-from_mp3_21_R1_2015_wav--4',
#     'MIDI-Unprocessed_04_R3_2008_01-07_ORIG_MID--AUDIO_04_R3_2008_wav--6',
#     'MIDI-Unprocessed_XP_14_R1_2004_04_ORIG_MID--AUDIO_14_R1_2004_04_Track04_wav',
#     'MIDI-Unprocessed_22_R2_2011_MID--AUDIO_R2-D5_11_Track11_wav',
#     'MIDI-Unprocessed_03_R1_2011_MID--AUDIO_R1-D1_19_Track19_wav',
#     'MIDI-Unprocessed_14_R1_2009_01-05_ORIG_MID--AUDIO_14_R1_2009_14_R1_2009_04_WAV',
#     'MIDI-UNPROCESSED_21-22_R1_2014_MID--AUDIO_22_R1_2014_wav--4',
#     'MIDI-Unprocessed_16_R1_2008_01-04_ORIG_MID--AUDIO_16_R1_2008_wav--1',
#     'MIDI-Unprocessed_10_R2_2008_01-05_ORIG_MID--AUDIO_10_R2_2008_wav--1',
#     'MIDI-Unprocessed_R1_D1-1-8_mid--AUDIO-from_mp3_01_R1_2015_wav--1',
#     'MIDI-Unprocessed_R2_D1-2-3-6-7-8-11_mid--AUDIO-from_mp3_03_R2_2015_wav--2',
#     'MIDI-UNPROCESSED_11-13_R1_2014_MID--AUDIO_13_R1_2014_wav--4',
#     'MIDI-Unprocessed_XP_04_R1_2004_03-05_ORIG_MID--AUDIO_04_R1_2004_05_Track05_wav',
#     'MIDI-Unprocessed_XP_01_R1_2004_04-05_ORIG_MID--AUDIO_01_R1_2004_06_Track06_wav',
#     'MIDI-UNPROCESSED_11-13_R1_2014_MID--AUDIO_11_R1_2014_wav--1',
#     'MIDI-Unprocessed_SMF_07_R1_2004_01_ORIG_MID--AUDIO_07_R1_2004_12_Track12_wav',
#     'MIDI-Unprocessed_081_PIANO081_MID--AUDIO-split_07-09-17_Piano-e_2_-02_wav--1',
#     'ORIG-MIDI_03_7_10_13_Group_MID--AUDIO_17_R3_2013_wav--1',
#     'MIDI-Unprocessed_10_R1_2008_01-04_ORIG_MID--AUDIO_10_R1_2008_wav--1',
#     'MIDI-Unprocessed_03_R3_2011_MID--AUDIO_R3-D1_05_Track05_wav',
#     'MIDI-Unprocessed_R2_D2-12-13-15_mid--AUDIO-from_mp3_12_R2_2015_wav--2',
#     'ORIG-MIDI_01_7_7_13_Group__MID--AUDIO_13_R1_2013_wav--1',
#     'MIDI-UNPROCESSED_06-08_R1_2014_MID--AUDIO_07_R1_2014_wav--5',
#     'MIDI-Unprocessed_060_PIANO060_MID--AUDIO-split_07-07-17_Piano-e_2-04_wav--1',
#     'MIDI-Unprocessed_04_R3_2011_MID--AUDIO_R3-D2_04_Track04_wav',
#     'MIDI-Unprocessed_XP_15_R1_2004_04_ORIG_MID--AUDIO_15_R1_2004_04_Track04_wav',
#     'MIDI-UNPROCESSED_04-05_R1_2014_MID--AUDIO_05_R1_2014_wav--1',
#     'MIDI-Unprocessed_05_R1_2011_MID--AUDIO_R1-D2_08_Track08_wav',
#     'MIDI-Unprocessed_16_R2_2011_MID--AUDIO_R2-D4_08_Track08_wav',
#     'MIDI-Unprocessed_18_R1_2006_01-05_ORIG_MID--AUDIO_18_R1_2006_02_Track02_wav',
#     'MIDI-Unprocessed_13_R1_2006_01-06_ORIG_MID--AUDIO_13_R1_2006_04_Track04_wav',
#     'MIDI-Unprocessed_11_R1_2008_01-04_ORIG_MID--AUDIO_11_R1_2008_wav--1',
#     'MIDI-Unprocessed_02_R1_2006_01-04_ORIG_MID--AUDIO_02_R1_2006_03_Track03_wav',
#     'MIDI-Unprocessed_14_R1_2011_MID--AUDIO_R1-D6_03_Track03_wav',
#     'MIDI-UNPROCESSED_06-08_R1_2014_MID--AUDIO_06_R1_2014_wav--1',
#     'MIDI-Unprocessed_03_R2_2011_MID--AUDIO_R2-D1_06_Track06_wav'
# ]
