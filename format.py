import pandas as pd
import mido
import numpy as np
from mido import MidiFile, MidiTrack


def measure_duration_in_ticks(track):
    return np.sum([msg.time for msg in track])


def convert_to_axillary_representation(track):
    ordered_events_list = []
    current_time = 0
    for msg in track:
        current_time += msg.time
        msg_meta = {"pause_duration": msg.time, "time": current_time}

        if msg.type in ["note_off", "note_on"]:
            msg_meta["type"] = "note_on"
        else:
            msg_meta["type"] = msg.type
        if msg_meta["type"] == "note_on":
            msg_meta.update({"velocity": msg.velocity, "note": msg.note})
        ordered_events_list.append(msg_meta)
    events_df = pd.DataFrame.from_records(ordered_events_list)
    events_df["duration"] = 0
    for note in events_df["note"].value_counts().index.values:
        specific_note_events = events_df.loc[events_df["note"] == note]
        if len(specific_note_events) < 2:
            continue
        events_df["duration"].iloc[specific_note_events.index[:-1].values] = \
            specific_note_events["time"].values[1:] - specific_note_events["time"].values[:-1]
    return events_df[["type", "time", "velocity", "note", "duration"]].loc[
               (events_df["velocity"].astype(float) != .0) &
               ((events_df["type"] == "note_on") | (events_df["type"] == "note_off"))], track[0], track[-1]


def convert_to_midi_track(axillary_event_df, begin_event, end_event):
    track = MidiTrack()
    track.append(begin_event)
    note_on_events = axillary_event_df[axillary_event_df["type"] == "note_on"].copy()
    note_on_events["time"] = note_on_events["time"].values + note_on_events["duration"].values
    note_on_events["velocity"] = 0
    axillary_event_df = \
        axillary_event_df.append(note_on_events, ignore_index=True).sort_values(by="time", ascending=True)
    axillary_event_df["pause_duration"] = 0
    axillary_event_df["pause_duration"].iloc[1:] = \
        axillary_event_df["time"].values[1:] - axillary_event_df["time"].values[:-1]
    for event in axillary_event_df.to_dict("records"):
        track.append(mido.Message(event["type"],
                                  note=int(event["note"]),
                                  velocity=int(event["velocity"]),
                                  time=int(event["pause_duration"])))

    track.append(end_event)
    return track


def count_up_steps(axillary_event_df, step=7):
    return int((127 - axillary_event_df["note"].max()) // step)


def count_down_steps(axillary_event_df, step=7, min=35):
    return int(max(axillary_event_df["note"].min()-min, 0) // step)


def idealize_durations(axillary_event_df, delta=3):
    axillary_event_df = axillary_event_df.copy()
    durations = axillary_event_df["duration"].value_counts().index.values[::-1]
    for duration in durations:
        axillary_event_df["duration"].loc[(axillary_event_df["duration"] < duration + delta) &
                                          (axillary_event_df["duration"] > duration - delta)] = duration
    return axillary_event_df


