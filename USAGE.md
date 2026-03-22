# Quick Start Usage Guide

This guide provides step-by-step instructions for using this repository with your actual scripts.

## 🎯 Complete Workflow

### Prerequisites

✅ Python 3.8+ installed  
✅ All dependencies installed: `pip install -r requirements.txt`  
✅ Montreal Forced Aligner installed (see [docs/mfa_setup.md](docs/mfa_setup.md))  
✅ **All script paths configured** (see [docs/script_configuration.md](docs/script_configuration.md))  

**⚠️ CRITICAL:** Before running any script, update the hardcoded paths! See the [Script Configuration Guide](docs/script_configuration.md).

---

## 📋 Step-by-Step Pipeline

### Step 0: Configure All Scripts

**This is the most important step!**

1. Read [docs/script_configuration.md](docs/script_configuration.md)
2. Update paths in every script you plan to use
3. Create your directory structure

Suggested structure:
```
my_project/
├── raw_audio/          # Your original files
├── dataset/
│   ├── wavs/          # Organized audio
│   └── Features/      # Extracted features
├── mfa_output/        # MFA results
├── processed/         # Sliced chunks
└── outputs/           # Final CSVs/.ds files
```

---

### Step 1: Organize Your Audio Files

If your audio files are in nested folders (like PJS corpus):

```bash
python src/copy-wavs.py
```

**What it does:**
- Searches through nested directories
- Copies all WAV files to one location
- Optionally renames based on folder name

**Before running:**
- Update `PARENT_DIR` (where your audio is)
- Update `DEST_DIR` (where to copy them)
- Set `RENAME_USING_FOLDER = True/False`

**Result:**
```
dataset/wavs/
├── song_001.wav
├── song_002.wav
└── ...
```

---

### Step 2: Create Transcriptions

Create matching text files for each audio:

```
dataset/wavs/
├── song_001.wav
├── song_001.txt  ← "Hello world how are you"
├── song_002.wav
├── song_002.txt  ← "Singing is so much fun"
└── ...
```

Each `.txt` file should contain the lyrics sung in the corresponding audio.

See [docs/dataset_preparation.md](docs/dataset_preparation.md) for guidelines.

---

### Step 3: Run Montreal Forced Aligner

```bash
# Activate MFA environment
conda activate aligner

# Download models (first time only)
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa

# Run alignment
mfa align \
    /path/to/dataset/wavs \
    english_us_arpa \
    english_us_arpa \
    /path/to/mfa_output \
    --clean
```

**Result:**
```
mfa_output/
├── song_001.TextGrid
├── song_002.TextGrid
└── ...
```

See [docs/mfa_setup.md](docs/mfa_setup.md) for detailed instructions.

---

### Step 4: Parse TextGrid Files

```bash
python src/parse_textgrid.py
```

**What it does:**
- Reads all `.TextGrid` files from MFA
- Extracts phoneme symbols and timings
- Saves as JSON files

**Before running:**
- Update `textgrid_dir` (where MFA saved TextGrids)
- Update `output_dir` (where to save JSONs)

**Result:**
```
dataset/Features/
├── song_001_phonemes.json
├── song_002_phonemes.json
└── ...
```

**JSON format:**
```json
[
  ["HH", 0.0, 0.15],
  ["AH", 0.15, 0.35],
  ["L", 0.35, 0.48],
  ...
]
```

---

### Step 5: Extract Audio Features

```bash
python src/Extraction_of_meta_data.py
```

**What it does:**
- Loads each WAV file
- Resamples to 44.1 kHz if needed
- Computes mel-spectrogram (80 bins)
- Extracts F0 pitch contour
- Saves as NumPy arrays

**Before running:**
- Update `input_dir` (where your WAV files are)
- Update `ouput_dir` → `output_dir` (fix the typo!)
- Fix line 26 (see [docs/script_configuration.md](docs/script_configuration.md))

**Result:**
```
dataset/Features/
├── song_001_mel.npy
├── song_001_f0.npy
├── song_002_mel.npy
├── song_002_f0.npy
└── ...
```

---

### Step 6 (Optional): Generate MIDI Notes

```bash
python src/MIDI_Notes.py
```

**What it does:**
- Loads F0 arrays and phoneme JSONs
- Converts average F0 per phoneme to MIDI note number
- Saves as `*_notes.json`

**Before running:**
- Update `output_dir` and `audio_dir`

**Result:**
```
dataset/Features/
├── song_001_notes.json
├── song_002_notes.json
└── ...
```

**Format:** `[(phoneme, midi_note, duration), ...]`

---

### Step 7: Choose Your Output Format

You now have all the features! Choose based on your goal:

#### **Option A: CSV for Training** (Most Common)

**From JSON phoneme files:**
```bash
python src/ForTranscriptions.py
```

**OR from HTK .lab files:**
```bash
python src/lab-to-csv-gen.py
```

**Result:** `phonemes_batch.csv` or `metadata.csv`

```csv
name,ph_seq,ph_dur
song_001,HH AH L OW,0.150 0.200 0.130 0.180
song_002,W ER L D,0.140 0.210 0.110 0.200
```

#### **Option B: .ds Files for Inference**

For testing with DiffSinger:

```bash
# Create .ds file for one song
python src/ds_maker.py

# Normalize lengths (if needed)
python src/ds_trimmer.py

# Validate before use
python src/matcher_for_phseq-phdur-f0seq.py
```

**Before running:**
- Update song name and paths in each script

**Result:** `.ds` files ready for DiffSinger inference

---

### Step 8 (Optional): Slice Long Audio

If your audio files are too long (>15 seconds):

#### **Method 1: Phoneme-based slicing with silence removal**

```bash
python src/spliting.py
```

**What it does:**
- Removes silence from audio
- Splits into chunks of N phonemes
- Exports chunk WAV files + CSV

**Configuration:**
```python
phonemes_per_chunk = 10  # Adjust as needed
```

**Result:**
```
processed/chunks/
├── song_001_chunk_0.wav
├── song_001_chunk_1.wav
└── ...

outputs/transcriptions.csv
```

#### **Method 2: AudioSlicer integration**

```bash
# Generate markers
python src/markers_for_audio_slicer.py

# Then use AudioSlicer tool externally
```

---

## 🔍 Verify Your Results

After each step, verify outputs:

### Check Phoneme JSONs
```python
import json
with open('dataset/Features/song_001_phonemes.json') as f:
    phonemes = json.load(f)
print(f"Phonemes: {len(phonemes)}")
print(f"First 3: {phonemes[:3]}")
```

### Check Features
```python
import numpy as np

mel = np.load('dataset/Features/song_001_mel.npy')
f0 = np.load('dataset/Features/song_001_f0.npy')

print(f"Mel shape: {mel.shape}")  # Should be (1, 80, frames)
print(f"F0 shape: {f0.shape}")    # Should be (frames,)
```

### Check CSV
```python
import pandas as pd
df = pd.read_csv('outputs/metadata.csv')
print(df.head())
print(f"Total songs: {len(df)}")
```

---

## 🛠️ Troubleshooting

### "No such file or directory"
- ✅ Check you updated the paths in the script
- ✅ Verify input files exist
- ✅ Make sure output directories exist

### "Module not found"
```bash
pip install -r requirements.txt
```

### "No .TextGrid files found"
- ✅ Check MFA ran successfully
- ✅ Verify `textgrid_dir` path in parse_textgrid.py

### "Mismatch in ph_seq and ph_dur lengths"
- This is normal for some files
- The scripts filter these out
- Check your transcriptions are accurate

---

## 📊 Expected File Counts

After full pipeline:

```
dataset/Features/
├── song_001_phonemes.json  ┐
├── song_001_mel.npy        ├─ For each song
├── song_001_f0.npy         │
└── song_001_notes.json     ┘  (optional)
```

**Files per song:** 3-4 (depending on if you ran MIDI_Notes.py)

---

## 🎯 Next Steps: Training

Once you have your CSV or .ds files, refer to:
- [docs/training_guide.md](docs/training_guide.md) for DiffSinger training
- Official DiffSinger repository for model setup

---

## 💡 Pro Tips

1. **Start small**: Test with 2-3 songs before processing your full dataset
2. **Check outputs**: Manually inspect a few files after each step
3. **Keep backups**: Never delete original audio files
4. **Document changes**: Note what settings worked best
5. **Use version control**: Track your script modifications

---

**Need help?** Check:
- [Script Configuration Guide](docs/script_configuration.md)
- [src/README.md](src/README.md) for detailed script documentation
- Individual script comments

Happy synthesizing! 🎵
