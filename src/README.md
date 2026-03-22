# Source Code Documentation

This directory contains all the Python scripts used in the DiffSinger voice synthesis pipeline.

## 📁 Scripts Overview

### Data Preparation Scripts

#### 1. `copy-wavs.py`
**Purpose:** Copy and organize WAV files from nested folder structure into a single directory

**What it does:**
- Recursively searches through a parent directory
- Finds WAV files in subfolders
- Copies them to a destination directory
- Optionally renames files based on their folder name

**Configuration:**
```python
PARENT_DIR = "path/to/source"      # Root directory to search
DEST_DIR = "path/to/destination"   # Where to copy files
RENAME_USING_FOLDER = True         # Rename as foldername.wav
```

**Use case:** Organizing datasets like PJS corpus where each song is in its own folder

---

#### 2. `spliting.py` ⭐ **Complex Script**
**Purpose:** Slice long audio files into smaller chunks based on phoneme count

**What it does:**
- Loads audio files and their corresponding phoneme JSON files
- Removes silence from audio
- Splits audio into chunks of N phonemes each
- Exports individual chunk WAV files
- Generates a CSV with phoneme sequences and durations for each chunk

**Features:**
- Silence removal using pydub
- Configurable phonemes per chunk
- Handles remaining phonemes at the end
- Creates matching CSV for DiffSinger training

**Configuration:**
```python
phonemes_per_chunk = 10            # How many phonemes per chunk
silence_thresh = -40               # dB threshold for silence
min_silence_len = 500              # Minimum silence length in ms
```

**Dependencies:**
- pydub
- pandas

**Use case:** Breaking down full songs into training-ready segments

---

### Feature Extraction Scripts

#### 3. `Extraction_of_meta_data.py`
**Purpose:** Extract mel-spectrograms and F0 contours from audio files

**What it does:**
- Loads WAV files
- Resamples to 44.1 kHz if needed
- Computes 80-band mel-spectrogram using torchaudio
- Extracts F0 pitch contour using librosa PYIN
- Saves features as NumPy arrays

**Output files:**
- `*_mel.npy`: Mel-spectrogram (80 x frames)
- `*_f0.npy`: F0 contour (frames,)

**Parameters:**
- Sample rate: 44,100 Hz
- FFT size: 2,048
- Hop length: 512
- Mel bins: 80
- F0 range: C2 to C7

---

#### 4. `Mel-Spectrogram.py`
**Purpose:** Standalone mel-spectrogram computation (incomplete script)

**Note:** This appears to be an alternative/backup version of mel extraction. The complete version is in `Extraction_of_meta_data.py`.

---

#### 5. `MIDI_Notes.py`
**Purpose:** Convert F0 contours to MIDI note numbers for each phoneme

**What it does:**
- Loads previously extracted F0 arrays
- Loads phoneme timing from JSON
- For each phoneme segment:
  - Extracts F0 values in that time range
  - Computes average F0 (ignoring unvoiced frames)
  - Converts to MIDI note number
- Saves as `*_notes.json`: (phoneme, midi_note, duration)

**Output format:**
```json
[
  ["AH", 60, 0.234],
  ["N", 62, 0.156],
  ...
]
```

**Use case:** Adding pitch information for singing voice synthesis

---

### Phoneme Processing Scripts

#### 6. `parse_textgrid.py`
**Purpose:** Parse Montreal Forced Aligner TextGrid files to extract phoneme timings

**What it does:**
- Reads `.TextGrid` files from MFA
- Extracts the 'phones' tier
- Parses phoneme symbols and time boundaries
- Saves as JSON: `[(phoneme, start_time, end_time), ...]`

**Output format:**
```json
[
  ["HH", 0.0, 0.15],
  ["AH", 0.15, 0.35],
  ["L", 0.35, 0.48],
  ...
]
```

---

#### 7. `ForTranscriptions.py`
**Purpose:** Batch convert phoneme JSON files to CSV format

**What it does:**
- Reads all JSON files in a directory
- Extracts phoneme sequences and durations
- Skips 'spn' (spoken noise) phonemes
- Generates a CSV with columns: name, ph_seq, ph_dur

**Output CSV format:**
```csv
name,ph_seq,ph_dur
song1,HH AH L OW,0.150 0.200 0.130 0.180
song2,W ER L D,0.140 0.210 0.110 0.200
```

**Use case:** Creating training metadata for DiffSinger

---

#### 8. `lab-to-csv-gen.py`
**Purpose:** Convert HTK .lab files to CSV format for DiffSinger

**What it does:**
- Recursively searches for .lab files
- Parses HTK format (100ns time units)
- Converts to seconds
- Generates ph_seq and ph_dur strings
- Creates CSV with all songs

**HTK .lab format:**
```
0 1500000 HH
1500000 3500000 AH
```

**Time conversion:** HTK units / 10,000,000 = seconds

**Use case:** Working with datasets that provide HTK label files (like PJS corpus)

---

### DiffSinger Format Scripts

#### 9. `ds_maker.py`
**Purpose:** Create .ds (DiffSinger format) files for inference

**What it does:**
- Loads phoneme JSON and F0 numpy array for a single song
- Formats into DiffSinger JSON structure
- Includes: ph_seq, ph_dur, f0_seq, f0_timestep, speaker_id, language_id

**Output .ds format:**
```json
[{
  "ph_seq": "HH AH L OW W ER L D",
  "ph_dur": "0.15 0.20 0.13 0.18 0.14 0.21 0.11 0.20",
  "f0_seq": "220.5 225.3 230.1 ...",
  "f0_timestep": 0.0116,
  "spk_id": 0,
  "lang_id": 1,
  "pitch_shift": 0,
  "speed": 1.0
}]
```

**Use case:** Creating inference files for testing trained DiffSinger models

---

#### 10. `ds_trimmer.py`
**Purpose:** Normalize sequence lengths in .ds files

**What it does:**
- Loads a .ds file
- Trims or repeats sequences to match target length
- Ensures ph_seq, ph_dur, and f0_seq all have same length

**Configuration:**
```python
TARGET_LENGTH = 1000  # Desired sequence length
```

**Strategies:**
- If too long: truncate
- If too short: repeat sequences
- If exact: keep as is

**Use case:** Fixing length mismatches before training

---

#### 11. `matcher_for_phseq-phdur-f0seq.py`
**Purpose:** Validate and filter .ds files for correct phoneme counts

**What it does:**
- Loads .ds file
- Checks if ph_seq and ph_dur lengths match expected count
- Optionally drops invalid entries
- Saves cleaned .ds file

**Configuration:**
```python
expected_count = 50     # Expected number of phonemes
drop_invalid = True     # Remove mismatched entries
```

**Use case:** Quality control before training

---

### Audio Processing Utilities

#### 12. `markers_for_audio_slicer.py`
**Purpose:** Generate marker files for AudioSlicer tool

**What it does:**
- Reads phoneme JSON files
- Groups phonemes into segments of max N seconds
- Creates AudioSlicer-compatible marker JSON
- Each segment has start and end times

**Output format:**
```json
{
  "segments": [
    [0.0, 4.8],
    [4.8, 9.5],
    [9.5, 14.2]
  ]
}
```

**Configuration:**
```python
max_chunk_duration = 5.0  # Maximum segment length in seconds
```

**Use case:** Preparing long audio files for slicing with AudioSlicer

---

## 🔄 Typical Workflow

### Full Pipeline

```
1. Data Organization
   └── copy-wavs.py
       ↓
   Organized WAV files

2. MFA Alignment (external tool)
   └── Montreal Forced Aligner
       ↓
   TextGrid files

3. Feature Extraction
   └── parse_textgrid.py → phoneme JSONs
   └── Extraction_of_meta_data.py → mel + F0
   └── MIDI_Notes.py → MIDI notes (optional)
       ↓
   Feature files: *_phonemes.json, *_mel.npy, *_f0.npy

4. Data Formatting (choose one path)
   
   Path A: CSV for training
   └── ForTranscriptions.py or lab-to-csv-gen.py
       ↓
   transcriptions.csv
   
   Path B: .ds files for inference
   └── ds_maker.py
   └── ds_trimmer.py (if needed)
   └── matcher_for_phseq-phdur-f0seq.py (validation)
       ↓
   .ds files

5. Optional: Audio Slicing
   └── spliting.py (phoneme-based)
   or
   └── markers_for_audio_slicer.py → AudioSlicer tool
       ↓
   Smaller audio chunks
```

## 📝 Script Dependencies

| Script | Dependencies |
|--------|-------------|
| copy-wavs.py | Standard library only |
| spliting.py | pydub, pandas |
| Extraction_of_meta_data.py | torch, torchaudio, librosa, numpy |
| MIDI_Notes.py | numpy, librosa, json |
| parse_textgrid.py | textgrid |
| ForTranscriptions.py | json, csv |
| lab-to-csv-gen.py | Standard library, glob |
| ds_maker.py | json, numpy |
| ds_trimmer.py | json |
| matcher_for_phseq-phdur-f0seq.py | json |
| markers_for_audio_slicer.py | json |
| Mel-Spectrogram.py | torchaudio, numpy |

## ⚙️ Configuration

All scripts have hardcoded paths like:
```python
"Z:\Robotics_Club\DL_MAJOR\..."
```

**Before using, update these paths to your actual directories!**

## 💡 Tips

1. **Run scripts in order** - many depend on outputs from previous steps
2. **Check paths** - all scripts need path updates for your system
3. **Verify outputs** - check a few files manually after each step
4. **Keep backups** - copy original data before processing
5. **Test small** - run on 2-3 files before full dataset

## 🐛 Common Issues

**Import errors:**
```bash
pip install librosa torchaudio textgrid pydub pandas
```

**Path errors:**
- Update all `Z:\...` paths to your directories
- Use raw strings: `r"path"` or forward slashes on Linux/Mac

**No output files:**
- Check input directory has correct file types
- Verify file naming conventions match
- Look for error messages in console

---

Need help with a specific script? Check the inline comments in each file!
