import json
import numpy as np

# Load files
phonemes = json.load(open("Z:\Robotics_Club\DL_MAJOR\dataset\Features\OutOfTime_phonemes.json"))
f0 = np.load("Z:\Robotics_Club\DL_MAJOR\dataset\Features\OutOfTime_f0.npy")

# Set timestep for f0
f0_timestep = 0.0116

# Prepare phoneme sequence and durations
ph_seq = []
ph_dur = []
for p, start, end in phonemes:
    ph_seq.append(p)
    ph_dur.append(round(end - start, 4))  # Round to 4 decimal places for safety

# Convert f0 to a space-separated string (remove 0s if needed)
f0_seq = " ".join(str(round(v, 2)) for v in f0 if v > 1)  # Ignore unvoiced frames
ph_seq_str = " ".join(ph_seq)
ph_dur_str = " ".join(str(d) for d in ph_dur)

# Output dict
ds_data = [{
    "ph_seq": ph_seq_str,
    "ph_dur": ph_dur_str,
    "f0_seq": f0_seq,
    "f0_timestep": f0_timestep,
    "spk_id": 0,
    "lang_id": 1,
    "pitch_shift": 0,
    "speed": 1.0
}]

# Save to .ds file
with open("Z:\Robotics_Club\DL_MAJOR\Generated_ds_for_testing\OutOfTime.ds", "w") as f:
    json.dump(ds_data, f, indent=2)