import json

def normalize_length(target_len, string_sequence):
    items = string_sequence.strip().split()
    if len(items) == target_len:
        return ' '.join(items)
    elif len(items) > target_len:
        return ' '.join(items[:target_len])
    else:
        # If fewer, repeat until target length is reached
        repeated = (items * ((target_len // len(items)) + 1))[:target_len]
        return ' '.join(repeated)

# Choose your target output length
TARGET_LENGTH = 1000

# Load .ds file (contains JSON-formatted text)
with open('Z:\Robotics_Club\DL_MAJOR\DiffSinger\ds\OutOfTime.ds', 'r') as f:
    ds_data = json.load(f)

# Process each entry in the list
for entry in ds_data:
    entry['ph_seq'] = normalize_length(TARGET_LENGTH, entry['ph_seq'])
    entry['ph_dur'] = normalize_length(TARGET_LENGTH, entry['ph_dur'])
    entry['f0_seq']  = normalize_length(TARGET_LENGTH, entry['f0_seq'])

# Save to new .ds file
with open('Z:\Robotics_Club\DL_MAJOR\DiffSinger\ds\OutOfTime_new.ds', 'w') as f:
    json.dump(ds_data, f, indent=2)

print(f"✅ Done. All sequences now have exactly {TARGET_LENGTH} items.")