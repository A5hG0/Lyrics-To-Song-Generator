# Project Structure

This document explains the organization of the LyricsToSongGenerator repository.

## 📁 Directory Layout

```
LyricsToSongGenerator/
│
├── 📄 README.md                    # Project overview and main documentation
├── 📄 LICENSE                      # MIT License with copyright disclaimer
├── 📄 USAGE.md                     # Step-by-step usage guide
├── 📄 CHANGELOG.md                 # Version history and updates
├── 📄 CONTRIBUTING.md              # Guidelines for contributors
├── 📄 requirements.txt             # Python dependencies
├── 📄 .gitignore                   # Files/directories to exclude from git
├── 📄 setup_check.py               # Verify setup and dependencies
│
├── 📂 src/                         # Source code
│   ├── Extraction_of_meta_data.py # Extract mel-spectrograms and F0
│   └── parse_textgrid.py          # Parse MFA TextGrid files
│
├── 📂 docs/                        # Documentation
│   ├── dataset_preparation.md     # How to prepare your dataset
│   ├── mfa_setup.md              # Montreal Forced Aligner setup
│   └── training_guide.md         # Training instructions
│
├── 📂 configs/                     # Configuration files
│   └── config_example.yaml        # Example configuration
│
└── 📂 examples/                    # Example scripts and outputs
    └── README.md                  # Examples documentation
```

## 📄 File Descriptions

### Root Level Files

#### README.md
- Main project documentation
- Installation instructions
- Feature overview
- Quick start guide
- Citation information

#### LICENSE
- MIT License for the code
- Important disclaimer about data/content rights
- Copyright notice

#### USAGE.md
- Step-by-step usage instructions
- Complete workflow from data to features
- Troubleshooting section
- Expected file structures

#### CONTRIBUTING.md
- Guidelines for contributing
- Code style standards
- Pull request process
- Community standards

#### CHANGELOG.md
- Version history
- List of changes in each release
- Planned features

#### requirements.txt
- All Python package dependencies
- Version specifications
- Installation via `pip install -r requirements.txt`

#### .gitignore
- Prevents committing large files
- Excludes datasets and models
- Protects copyrighted content
- Keeps repository clean

#### setup_check.py
- Verifies installation
- Checks dependencies
- Tests environment
- Provides diagnostic info

### 📂 src/ Directory

Contains **12 Python scripts** for the complete DiffSinger pipeline.

#### Data Preparation (2 scripts)

**copy-wavs.py**
- Organizes WAV files from nested folders
- Copies to single directory
- Optional renaming based on folder names
- **Use for:** PJS corpus, nested datasets

**spliting.py** (207 lines)
- Advanced audio slicer
- Phoneme-based chunking
- Silence removal with pydub
- Generates CSV + chunked WAV files
- **Use for:** Long audio files (>15 seconds)

#### Feature Extraction (3 scripts)

**Extraction_of_meta_data.py**
- Extracts mel-spectrograms (80 bins)
- Extracts F0 pitch contours (PYIN)
- Resamples to 44.1 kHz
- **Outputs:** `*_mel.npy`, `*_f0.npy`

**MIDI_Notes.py**
- Converts F0 to MIDI note numbers
- Per-phoneme pitch averaging
- **Outputs:** `*_notes.json`

**Mel-Spectrogram.py**
- Incomplete/backup script
- **Note:** Use Extraction_of_meta_data.py instead

#### Phoneme Processing (3 scripts)

**parse_textgrid.py**
- Parses MFA TextGrid files
- Extracts phoneme timings
- **Outputs:** `*_phonemes.json`

**ForTranscriptions.py**
- Batch converts phoneme JSONs to CSV
- Skips 'spn' phonemes
- **Outputs:** CSV with ph_seq and ph_dur

**lab-to-csv-gen.py**
- Converts HTK .lab files to CSV
- Handles PJS corpus format
- Time unit conversion (100ns → seconds)
- **Outputs:** metadata.csv

#### DiffSinger Format (3 scripts)

**ds_maker.py**
- Creates .ds files for DiffSinger
- Combines ph_seq, ph_dur, f0_seq
- Adds speaker/language metadata

**ds_trimmer.py**
- Normalizes sequence lengths
- Trims or repeats to target length
- Ensures consistent array sizes

**matcher_for_phseq-phdur-f0seq.py**
- Validates .ds file sequences
- Checks length consistency
- Filters invalid entries

#### Utilities (1 script)

**markers_for_audio_slicer.py**
- Generates AudioSlicer markers
- Groups phonemes into time segments
- **Outputs:** Marker JSON files

### 📂 docs/ Directory

Comprehensive documentation for each stage of the project.

#### dataset_preparation.md
- Legal and ethical considerations
- Audio quality requirements
- Transcription guidelines
- Directory structure
- Preprocessing steps
- Quality control checklist

#### mfa_setup.md
- What is MFA and why use it
- Installation instructions
- Downloading models
- Running alignment
- Understanding TextGrid output
- Troubleshooting

#### training_guide.md
- Training prerequisites
- Feature extraction details
- DiffSinger setup
- Training process
- Hyperparameter tuning
- Evaluation and inference
- Common issues and solutions

### 📂 configs/ Directory

Configuration file templates.

#### config_example.yaml
- Example configuration for the pipeline
- Dataset paths and parameters
- Model architecture settings
- Training hyperparameters
- Copy and customize for your use

### 📂 examples/ Directory

Example scripts and sample data (when available).

Currently contains:
- README explaining what goes here
- Placeholder for future examples

Future additions:
- Visualization scripts
- Data validation utilities
- Example notebooks
- Small sample files (with proper licensing)

## 🔄 Typical Workflow

```
1. Prepare Dataset
   └── Audio files (.wav) + Transcripts (.txt)
   
2. Run MFA Alignment
   └── Generates .TextGrid files
   
3. Extract Features
   └── src/Extraction_of_meta_data.py
   └── Creates *_mel.npy and *_f0.npy
   
4. Parse TextGrids
   └── src/parse_textgrid.py
   └── Creates *_phonemes.json
   
5. Training (Not in this repo)
   └── Use DiffSinger or similar framework
   └── See docs/training_guide.md
```

## 🚫 What's NOT Included

This repository intentionally excludes:

### ❌ Not in Repository
- Audio datasets (copyrighted content)
- Pre-trained model weights
- Large binary files
- User-specific data
- Generated audio samples (except small demos)

### ✅ Why These Are Excluded
- **Legal**: Avoid copyright issues
- **Size**: Keep repository lightweight
- **Privacy**: Protect user data
- **Portability**: Easy to clone and share

## 📝 Adding Your Own Files

### Local Files (Not Committed)
Create these directories for your work:
```
LyricsToSongGenerator/
├── data/              # Your datasets
├── models/            # Model checkpoints
├── outputs/           # Generated results
└── experiments/       # Your experiments
```

These are in `.gitignore` and won't be committed.

### Files You Can Commit
- Bug fixes to existing scripts
- New utility scripts
- Documentation improvements
- Configuration examples
- Small test files (<1MB, properly licensed)

## 🔄 Keeping Up to Date

```bash
# Pull latest changes
git pull origin main

# Check for new dependencies
pip install -r requirements.txt

# Run setup check
python setup_check.py
```

## 📚 Documentation Organization

### For Beginners
1. Start with: **README.md**
2. Then read: **USAGE.md**
3. Follow: **docs/dataset_preparation.md**

### For Contributors
1. Read: **CONTRIBUTING.md**
2. Check: **PROJECT_STRUCTURE.md** (this file)
3. Review: Existing code in **src/**

### For Researchers
1. Review: **docs/training_guide.md**
2. Check: **configs/config_example.yaml**
3. Examine: Feature extraction in **src/**

## 💡 Best Practices

### When Using This Repository

1. **Fork it**: Create your own fork for your work
2. **Update paths**: Change hardcoded paths in scripts
3. **Keep clean**: Don't commit datasets or models
4. **Document**: Note your changes and experiments
5. **Backup**: Keep original data separate

### When Contributing

1. **Follow structure**: Put files in appropriate directories
2. **Update docs**: Document any new features
3. **Test first**: Verify changes work
4. **Keep focused**: One feature per pull request
5. **Respect copyright**: Never commit copyrighted content

## 🎯 Quick Reference

| Need to... | Go to... |
|-----------|----------|
| Understand the project | README.md |
| Get started | USAGE.md |
| Prepare dataset | docs/dataset_preparation.md |
| Setup MFA | docs/mfa_setup.md |
| Train a model | docs/training_guide.md |
| Contribute | CONTRIBUTING.md |
| Check setup | Run setup_check.py |
| See what changed | CHANGELOG.md |
| Understand layout | PROJECT_STRUCTURE.md (this file) |

---

This structure is designed to be clear, organized, and easy to navigate. If you have suggestions for improvements, please see CONTRIBUTING.md!
