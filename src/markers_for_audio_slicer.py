import os
import json

# === CONFIG ===
input_phoneme_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features\jsons"   # folder containing files like song1.json
output_marker_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features\jsons_new"     # where AudioSlicer-ready marker files will go
max_chunk_duration = 5.0               # seconds (change if needed)

os.makedirs(output_marker_dir, exist_ok=True)

def group_segments(phoneme_entries, max_duration=5.0):
    segments = []
    current_start = None
    current_end = None

    for phone, start, end in phoneme_entries:
        start = float(start)
        end = float(end)

        if current_start is None:
            current_start = start
            current_end = end
        elif end - current_start <= max_duration:
            current_end = end
        else:
            segments.append([round(current_start, 3), round(current_end, 3)])
            current_start = start
            current_end = end

    # add final segment
    if current_start is not None and current_end is not None:
        segments.append([round(current_start, 3), round(current_end, 3)])

    return segments

# Process all JSONs
for file in os.listdir(input_phoneme_dir):
    if not file.endswith(".json"):
        continue

    input_path = os.path.join(input_phoneme_dir, file)
    with open(input_path, 'r') as f:
        data = json.load(f)

    # Skip if invalid format
    if not data or not isinstance(data[0], list) or len(data[0]) != 3:
        print(f"[Skipped] Invalid format in {file}")
        continue

    segments = group_segments(data, max_chunk_duration)
    marker_json = {"segments": segments}

    output_path = os.path.join(output_marker_dir, file)
    with open(output_path, "w") as f:
        json.dump(marker_json, f, indent=2)

    print(f"[✓] Marker created: {file} → {output_path}")

print("\n✅ All marker JSONs are ready for AudioSlicer.")