# The transcriptions.csv File - CRITICAL GUIDE

## ⚠️ THIS IS THE MOST IMPORTANT FILE

**From my experience:**

I spent weeks searching for proper documentation on this file format. Getting transcriptions.csv right is THE most critical step in the entire pipeline. If this file has errors, DiffSinger training will fail - and often fail silently without clear error messages.

This file is what DiffSinger reads during training. Every mistake here cascades into training problems.

## 📋 Required Format

The `transcriptions.csv` file MUST have exactly 3 columns with these exact headers:

```csv
name,ph_seq,ph_dur
```

### Column Descriptions

1. **name**: Base filename (without .wav extension)
2. **ph_seq**: Space-separated phoneme sequence
3. **ph_dur**: Space-separated phoneme durations (in seconds)

### Example (from actual working dataset)

```csv
name,ph_seq,ph_dur
pjs001,HH AH L OW W ER L D,0.150 0.200 0.130 0.180 0.140 0.210 0.110 0.200
pjs002,S IH NG IH NG IH Z F AH N,0.120 0.180 0.090 0.170 0.160 0.190 0.140 0.180 0.150
pjs003,M AH S IH K M EY K S L AY F,0.170 0.200 0.110 0.180 0.130 0.190 0.160 0.150 0.170 0.180 0.140
```

## ✅ Critical Rules

### 1. **Length Match**
The number of phonemes in `ph_seq` MUST equal the number of durations in `ph_dur`.

```
❌ BAD:
name,ph_seq,ph_dur
song1,HH AH L,0.15 0.20          # 3 phonemes, 2 durations - MISMATCH!

✅ GOOD:
name,ph_seq,ph_dur
song1,HH AH L,0.15 0.20 0.13     # 3 phonemes, 3 durations - MATCH!
```

### 2. **No Empty Values**
Every row must have all three fields filled.

```
❌ BAD:
name,ph_seq,ph_dur
song1,,                           # Empty phonemes

✅ GOOD:
name,ph_seq,ph_dur
song1,HH AH L,0.15 0.20 0.13
```

### 3. **Consistent Phoneme Set**
Use the same phoneme dictionary throughout (e.g., ARPAbet for English, Japanese phoneme set for Japanese).

### 4. **Proper Duration Values**
- Durations should be in seconds
- Typically between 0.05 and 0.50 seconds
- Must be positive numbers
- Should sum to approximate audio length

### 5. **Filename Matching**
The `name` column must match your WAV files (without .wav extension).

```
If you have:  BlindingLights.wav
Then use:     BlindingLights

Dataset structure:
├── wavs/
│   └── BlindingLights.wav
└── transcriptions.csv  (contains "BlindingLights" in name column)
```

## 📁 Directory Structure Requirement

Your dataset directory should look like:

```
dataset/
├── wavs/
│   ├── song_001.wav
│   ├── song_002.wav
│   └── ...
└── transcriptions.csv   ← THIS FILE
```

## 🔧 How to Generate This File

You have **three methods** in this repository:

### Method 1: From Phoneme JSON Files (Most Common)

If you've already run `parse_textgrid.py` and have `*_phonemes.json` files:

```bash
python src/ForTranscriptions.py
```

Update the script paths:
```python
input_dir = "path/to/Features"  # Where *_phonemes.json files are
output_csv = "path/to/dataset/transcriptions.csv"
```

### Method 2: From HTK .lab Files (PJS Corpus)

If you're using a dataset with HTK label files:

```bash
python src/lab-to-csv-gen.py
```

Update the script paths:
```python
ROOT_DIR = "path/to/dataset_with_lab_files"
OUT_CSV = "path/to/dataset/transcriptions.csv"
```

### Method 3: From Audio Chunks (After Slicing)

If you used `spliting.py` to create audio chunks:

```bash
python src/spliting.py
```

This automatically generates `transcriptions.csv` alongside the chunked audio files.

## 🔍 Verification Steps

### 1. Check File Exists
```bash
ls dataset/transcriptions.csv
```

### 2. Check Format
```python
import pandas as pd

# Load CSV
df = pd.read_csv('dataset/transcriptions.csv')

# Check columns
print("Columns:", df.columns.tolist())
# Should be: ['name', 'ph_seq', 'ph_dur']

# Check first few rows
print(df.head())

# Check for empty values
print("Empty values:", df.isnull().sum())

# Check length matches
for idx, row in df.iterrows():
    ph_seq_len = len(row['ph_seq'].split())
    ph_dur_len = len(row['ph_dur'].split())
    if ph_seq_len != ph_dur_len:
        print(f"MISMATCH in {row['name']}: ph_seq={ph_seq_len}, ph_dur={ph_dur_len}")
```

### 3. Check WAV Files Match
```python
import os

wav_dir = 'dataset/wavs'
wav_files = {os.path.splitext(f)[0] for f in os.listdir(wav_dir) if f.endswith('.wav')}

csv_names = set(df['name'])

missing_in_csv = wav_files - csv_names
missing_wavs = csv_names - wav_files

if missing_in_csv:
    print(f"WAV files without CSV entries: {missing_in_csv}")
if missing_wavs:
    print(f"CSV entries without WAV files: {missing_wavs}")
```

## ⚙️ Config File Integration

In your `acoustic_pjs_corpus.yaml` or `variance_pjs_corpus.yaml`, the dataset path should point to the directory containing this file:

```yaml
datasets:
  - raw_data_dir: Z:\path\to\dataset  # ← This directory must contain transcriptions.csv
    speaker: pjs
    spk_id: 0
    language: ja
```

DiffSinger will look for `transcriptions.csv` in the `raw_data_dir`.

## 🐛 Common Issues

### Issue 1: "Phoneme mismatch"
**Cause:** `ph_seq` and `ph_dur` have different lengths

**Fix:**
```python
# Check and filter
df = pd.read_csv('transcriptions.csv')
valid_rows = []
for idx, row in df.iterrows():
    if len(row['ph_seq'].split()) == len(row['ph_dur'].split()):
        valid_rows.append(row)
    else:
        print(f"Skipping {row['name']}: length mismatch")

df_fixed = pd.DataFrame(valid_rows)
df_fixed.to_csv('transcriptions_fixed.csv', index=False)
```

### Issue 2: "File not found"
**Cause:** CSV `name` doesn't match WAV filename

**Fix:** Ensure exact match (case-sensitive on Linux):
```python
# Rename CSV entries to match WAV files
wav_files = {os.path.splitext(f)[0]: f for f in os.listdir('dataset/wavs')}
df['name'] = df['name'].map(lambda x: os.path.splitext(wav_files.get(x + '.wav', ''))[0] or x)
```

### Issue 3: "Empty ph_seq"
**Cause:** Phoneme sequence is empty

**Fix:** Filter out empty rows:
```python
df = df[df['ph_seq'].str.strip() != '']
df = df[df['ph_dur'].str.strip() != '']
```

## 💡 Pro Tips

1. **Keep a backup**: Always keep the original before making changes
2. **Start small**: Test with 5-10 songs first
3. **Validate early**: Check the CSV before running binarization
4. **Use scripts**: Don't manually create this file - use the provided scripts
5. **Check encoding**: Save as UTF-8, especially for non-English phonemes

## 📝 Template

If you need to create one manually (not recommended), use this template:

```csv
name,ph_seq,ph_dur
song_name_here,PHONEME1 PHONEME2 PHONEME3,0.150 0.200 0.180
```

**But seriously, use the scripts!** They handle all the edge cases.

## ✅ Success Indicators

You've got it right when:
- [ ] File exists in `dataset/transcriptions.csv`
- [ ] Has exactly 3 columns: name, ph_seq, ph_dur
- [ ] All ph_seq and ph_dur lengths match
- [ ] All names match WAV files
- [ ] No empty values
- [ ] DiffSinger binarization runs without errors

---

**Remember:** This file is the bridge between your audio files and DiffSinger training. Get this right, and everything else follows!
