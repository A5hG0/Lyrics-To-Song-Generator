import json

# === CONFIGURATION ===
ds_path = "Z:\Robotics_Club\DL_MAJOR\DiffSinger\ds\OutOfTime.ds"      # Input .ds file
output_path = "Z:\Robotics_Club\DL_MAJOR\DiffSinger\ds\OutOfTime_new.ds"  # Output .ds file with only valid entries
expected_count = 50          # <-- Set your desired custom count here
drop_invalid = True          # Set to False to just log and keep everything

# === MAIN SCRIPT ===
def validate_and_filter_ds(ds_path, expected_count, drop_invalid):
    with open(ds_path, 'r') as f:
        data = json.load(f)

    valid_data = []
    for idx, item in enumerate(data):
        ph_seq = item["ph_seq"].split()
        ph_dur = item["ph_dur"].split()
        f0_seq = item["f0_seq"].split() if isinstance(item["f0_seq"], str) else item["f0_seq"]

        len_ph_seq = len(ph_seq)
        len_ph_dur = len(ph_dur)
        len_f0_seq = len(f0_seq)

        if len_ph_seq == len_ph_dur == expected_count:
            valid_data.append(item)
        else:
            print(f"[!] Entry {idx} mismatch:")
            print(f"    ph_seq: {len_ph_seq}, ph_dur: {len_ph_dur}, f0_seq: {len_f0_seq}")
            if not drop_invalid:
                valid_data.append(item)

    with open(output_path, 'w') as f:
        json.dump(valid_data, f, indent=2)
    
    print(f"\n✔ Done. Valid entries saved to: {output_path}")
    print(f"→ {len(valid_data)} entries kept out of {len(data)}")

# === RUN ===
validate_and_filter_ds(ds_path, expected_count, drop_invalid)
