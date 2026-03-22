import json
import csv
import os

# Directory containing JSON files
input_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features\jsons"  # Replace with your folder path
output_csv = "phonemes_batch.csv"

# Prepare CSV data
csv_data = [["name", "ph_seq", "ph_dur"]]

# Iterate through JSON files in the directory
for json_file in os.listdir(input_dir):
    if json_file.endswith(".json"):
        # Extract song name from filename (without extension)
        song_name = os.path.splitext(json_file)[0]
        
        # Read JSON file
        with open(os.path.join(input_dir, json_file), "r") as f:
            json_data = json.load(f)
        
        # Calculate durations and prepare phoneme sequence
        ph_seq = []
        ph_dur = []
        for phoneme, start, end in json_data:
            if phoneme and phoneme != "spn":  # Skip empty phonemes and 'spn'
                ph_seq.append(phoneme)
                duration = end - start
                ph_dur.append(round(duration, 3))  # Round to 3 decimal places
        
        # Append to CSV data
        csv_data.append([song_name, " ".join(ph_seq), " ".join(map(str, ph_dur))])

# Write to CSV file
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_data)

print(f"CSV file '{output_csv}' has been generated with data from all JSON files.")