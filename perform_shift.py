
# region change pitch
dispatcher = []
current_columns_names.append("shift")
dispatcher_df[["up_boundary", "down_bondary"]] = \
    pd.DataFrame.from_records(
        [instrument_pitch_bondaries[instrument] for instrument in dispatcher_df["instrument"].values])[
        ["max_note", "min_note"]]
for shift in range(-int(max(dispatcher_df["note"].min() - min, 0) // 7),
                   int((127 - dispatcher_df["note"].max()) // 7)):
    observations_in_range_for_current_shift = \
        dispatcher_df.loc[(dispatcher_df["max_note"] + 7 * shift <= dispatcher_df["up_boundary"]) &
                          (dispatcher_df["min_note"] + 7 * shift >= dispatcher_df["down_bondary"])]

    folder_and_name = \
        zip([f'{chunk_to_index({"begin_i": begin_i, "end_i": end_i})}/{instrument}'
             for begin_i, end_i, instrument in
             observations_in_range_for_current_shift[["begin_i", "end_i", "instrument"]]],
            observations_in_range_for_current_shift["name"])


    def f(x):
        augmentations.change_octave(f"{template_folder}/{x[0]}/{x[1]}.mid",
                                    f"{target_folder}/{x[0]}/{instrument}/{x[1]}.mid", shift)


    with Pool(5) as p:
        print(p.map(f, folder_and_name))
    observations_in_range_for_current_shift["shift"] = shift
    dispatcher.append(observations_in_range_for_current_shift[current_columns_names].values)
dispatcher_df = pd.DataFrame(np.concatenate(dispatcher), columns=current_columns_names)
dispatcher_df.to_csv("cur.csv")
