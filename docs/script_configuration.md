# Script Configuration Guide

All scripts in this repository contain hardcoded paths that need to be updated before use. This guide helps you configure them for your system.

## ⚠️ Important: Update Paths Before Running

Every script has paths like:
```python
"Z:\Robotics_Club\DL_MAJOR\..."
```

These are **Windows paths from the original development environment** and will not work on your system.

## 🔧 How to Configure Scripts

### Step 1: Decide Your Directory Structure

Create a working directory structure like:
```
my_project/
├── raw_audio/          # Original audio files
├── dataset/
│   ├── wavs/          # Organized WAV files
│   └── Features/      # Extracted features
├── mfa_output/        # MFA TextGrid files
├── processed/         # Sliced audio chunks
└── outputs/           # Final .ds files or CSVs
```

### Step 2: Update Each Script

Here's what to change in each script:

---

### 📄 copy-wavs.py

**Lines to update:**
```python
PARENT_DIR = r"Z:\Robotics_Club\DL_MAJOR\PJS_corpus_ver1.1"
DEST_DIR   = r"Z:\Robotics_Club\DL_MAJOR\PJS_corpus_ver1.1\dataset\wavs"
```

**Replace with:**
```python
PARENT_DIR = r"/path/to/your/raw_audio"  # or "C:\path\to\your\raw_audio" on Windows
DEST_DIR   = r"/path/to/your/dataset/wavs"
```

---

### 📄 Extraction_of_meta_data.py

**Lines to update:**
```python
input_dir = "Z:\Robotics_Club\DL_MAJOR\Vocals\Done"
ouput_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features"
```

**Replace with:**
```python
input_dir = "/path/to/your/dataset/wavs"
output_dir = "/path/to/your/dataset/Features"  # Note: also fix the typo!
```

**Also fix line 26:**
Change:
```python
np.save(os.path.join(ouput_dir),f"{utt_id}_mel.npy",mel_spec.numpy())
```
To:
```python
np.save(os.path.join(output_dir, f"{utt_id}_mel.npy"), mel_spec.numpy())
```

---

### 📄 parse_textgrid.py

**Lines to update:**
```python
textgrid_dir = "Z:\Robotics_Club\DL_MAJOR\mfa_output_new_v2"
output_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features"
```

**Replace with:**
```python
textgrid_dir = "/path/to/your/mfa_output"
output_dir = "/path/to/your/dataset/Features"
```

---

### 📄 MIDI_Notes.py

**Lines to update:**
```python
output_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features"
audio_dir = "Z:\Robotics_Club\DL_MAJOR\Vocals\Done"
```

**Replace with:**
```python
output_dir = "/path/to/your/dataset/Features"
audio_dir = "/path/to/your/dataset/wavs"
```

---

### 📄 ForTranscriptions.py

**Lines to update:**
```python
input_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features\jsons"
output_csv = "phonemes_batch.csv"
```

**Replace with:**
```python
input_dir = "/path/to/your/dataset/Features"  # Where *_phonemes.json files are
output_csv = "/path/to/your/outputs/phonemes_batch.csv"
```

---

### 📄 lab-to-csv-gen.py

**Lines to update:**
```python
ROOT_DIR = r"Z:\Robotics_Club\DL_MAJOR\PJS_corpus_ver1.1"
OUT_CSV  = r"Z:\Robotics_Club\DL_MAJOR\PJS_corpus_ver1.1\metadata.csv"
```

**Replace with:**
```python
ROOT_DIR = r"/path/to/your/dataset_with_lab_files"
OUT_CSV  = r"/path/to/your/outputs/metadata.csv"
```

---

### 📄 ds_maker.py

**Lines to update:**
```python
phonemes = json.load(open("Z:\Robotics_Club\DL_MAJOR\dataset\Features\OutOfTime_phonemes.json"))
f0 = np.load("Z:\Robotics_Club\DL_MAJOR\dataset\Features\OutOfTime_f0.npy")
# ... later ...
with open("Z:\Robotics_Club\DL_MAJOR\Generated_ds_for_testing\OutOfTime.ds", "w") as f:
```

**Replace with:**
```python
song_name = "OutOfTime"  # Change this
features_dir = "/path/to/your/dataset/Features"
output_dir = "/path/to/your/outputs"

phonemes = json.load(open(f"{features_dir}/{song_name}_phonemes.json"))
f0 = np.load(f"{features_dir}/{song_name}_f0.npy")
# ... later ...
with open(f"{output_dir}/{song_name}.ds", "w") as f:
```

---

### 📄 ds_trimmer.py

**Lines to update:**
```python
with open('Z:\Robotics_Club\DL_MAJOR\DiffSinger\ds\OutOfTime.ds', 'r') as f:
# ... later ...
with open('Z:\Robotics_Club\DL_MAJOR\DiffSinger\ds\OutOfTime_new.ds', 'w') as f:
```

**Replace with:**
```python
input_ds = "/path/to/your/outputs/OutOfTime.ds"
output_ds = "/path/to/your/outputs/OutOfTime_trimmed.ds"

with open(input_ds, 'r') as f:
# ... later ...
with open(output_ds, 'w') as f:
```

---

### 📄 matcher_for_phseq-phdur-f0seq.py

**Lines to update:**
```python
ds_path = "Z:\Robotics_Club\DL_MAJOR\DiffSinger\ds\OutOfTime.ds"
output_path = "Z:\Robotics_Club\DL_MAJOR\DiffSinger\ds\OutOfTime_new.ds"
```

**Replace with:**
```python
ds_path = "/path/to/your/outputs/OutOfTime.ds"
output_path = "/path/to/your/outputs/OutOfTime_validated.ds"
```

---

### 📄 markers_for_audio_slicer.py

**Lines to update:**
```python
input_phoneme_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features\jsons"
output_marker_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features\jsons_new"
```

**Replace with:**
```python
input_phoneme_dir = "/path/to/your/dataset/Features"
output_marker_dir = "/path/to/your/outputs/markers"
```

---

### 📄 spliting.py

**Lines to update (at the bottom, line 165-171):**
```python
input_audio_dir = r"Z:\Robotics_Club\DL_MAJOR\Vocals\wavs_original"
input_json_dir = r"Z:\Robotics_Club\DL_MAJOR\dataset\Features\jsons"
output_audio_dir = r"Z:\Robotics_Club\DL_MAJOR\Vocals\Done\wavs_new"
output_csv = r"Z:\Robotics_Club\DL_MAJOR\Vocals\Done\Transcriptions_new.csv"
```

**Replace with:**
```python
input_audio_dir = r"/path/to/your/dataset/wavs"
input_json_dir = r"/path/to/your/dataset/Features"
output_audio_dir = r"/path/to/your/processed/chunks"
output_csv = r"/path/to/your/outputs/transcriptions.csv"
```

---

## 💡 Quick Tips

### For Linux/Mac Users

Use forward slashes:
```python
input_dir = "/home/user/project/dataset/wavs"
```

### For Windows Users

Use raw strings with backslashes:
```python
input_dir = r"C:\Users\YourName\project\dataset\wavs"
```

Or use forward slashes (works on Windows too):
```python
input_dir = "C:/Users/YourName/project/dataset/wavs"
```

### Using Environment Variables (Advanced)

Create a config file:
```python
# config.py
import os

PROJECT_ROOT = os.path.expanduser("~/my_project")
DATASET_DIR = os.path.join(PROJECT_ROOT, "dataset")
FEATURES_DIR = os.path.join(DATASET_DIR, "Features")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")
```

Then in your scripts:
```python
from config import FEATURES_DIR, OUTPUT_DIR

input_dir = FEATURES_DIR
output_dir = OUTPUT_DIR
```

## ✅ Verification Checklist

Before running each script:

- [ ] All paths are updated to your system
- [ ] Input directories exist and contain expected files
- [ ] Output directories are created (or script creates them)
- [ ] Paths use correct separators for your OS
- [ ] No syntax errors from path strings

## 🔄 Recommended Order

Update scripts in the order you'll use them:

1. ✅ copy-wavs.py
2. ✅ (Run MFA externally)
3. ✅ parse_textgrid.py
4. ✅ Extraction_of_meta_data.py
5. ✅ MIDI_Notes.py (optional)
6. ✅ ForTranscriptions.py OR lab-to-csv-gen.py
7. ✅ spliting.py (optional)

## 🆘 Common Issues

**Issue: "No such file or directory"**
- Check paths are correct
- Verify input files exist
- Make sure output directories are created

**Issue: "Invalid escape sequence"**
- Use raw strings: `r"path"` or forward slashes

**Issue: "Permission denied"**
- Check folder permissions
- Try running with appropriate privileges

---

**Tip:** Keep a copy of your configured paths somewhere safe so you don't lose them!
