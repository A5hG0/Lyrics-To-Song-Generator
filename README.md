# LyricsToSongGenerator 🎵

A deep learning project for singing voice synthesis using the DiffSinger model. This repository contains the code and methodology for creating custom voice models trained on vocal datasets.

## 📖 Overview

I built this toolkit to make DiffSinger training easier and more accessible. After spending months figuring out the complete pipeline, I'm sharing everything I learned - from data preparation to actual training.

**What is this?**
This is a **companion toolkit** for [DiffSinger](https://github.com/openvpi/DiffSinger) that provides:
- 12 production scripts for data preprocessing
- Complete documentation I wish I had when starting
- Production-tested config files
- Step-by-step guides based on real experience

**What is DiffSinger?**
DiffSinger is a diffusion-based acoustic model for singing voice synthesis (you'll install it separately).

**The pipeline includes:**
- Audio preprocessing and feature extraction
- Phoneme alignment using Montreal Forced Aligner (MFA)
- Mel-spectrogram and F0 (pitch) extraction
- Ready-to-use configs for DiffSinger training

## ✨ Features

- **Complete Pipeline**: 12 Python scripts covering every step from data preparation to DiffSinger format
- **Data Organization**: Tools to organize and copy files from complex directory structures
- **Advanced Audio Slicing**: Phoneme-based audio slicing with silence removal
- **Feature Extraction**: Automated extraction of mel-spectrograms, F0 contours, and MIDI notes
- **Phoneme Processing**: Parse MFA TextGrid files and convert to various formats
- **Format Conversion**: Tools for CSV, .ds, HTK .lab, and JSON formats
- **Quality Control**: Validation and filtering tools for training data
- **AudioSlicer Integration**: Generate marker files for external slicing tools
- **Flexible Training**: Support for both custom and pre-existing datasets

## 🛠️ Requirements

```bash
Python 3.8+
PyTorch 1.10+
torchaudio
librosa
numpy
textgrid
Montreal Forced Aligner (MFA)
```

## 🔗 Prerequisites - Important!

This repository provides **preprocessing tools and documentation** for DiffSinger. You need to install DiffSinger separately.

### Step 1: Install DiffSinger (Official Repo)

```bash
# Clone official DiffSinger repository
git clone https://github.com/openvpi/DiffSinger.git
cd DiffSinger

# Follow their installation instructions
pip install -r requirements.txt
```

See [DiffSinger's installation guide](https://github.com/openvpi/DiffSinger) for details.

### Step 2: Clone This Toolkit

```bash
# Clone this preprocessing toolkit
git clone https://github.com/Ashish00734/LyricsToSongGenerator.git
cd LyricsToSongGenerator

# Install preprocessing dependencies
pip install -r requirements-diffsinger.txt
```

### Step 3: Install MFA (Separate Environment Recommended)

```bash
# Create MFA environment
conda create -n mfa -c conda-forge montreal-forced-aligner
conda activate mfa

# Or with pip
pip install -r requirements-mfa.txt
```

See [docs/mfa_setup.md](docs/mfa_setup.md) for detailed MFA setup.

## 📁 How These Repos Work Together

```
┌─────────────────────────────────────────────────────┐
│ DiffSinger (Official - Training Engine)             │
│ - Model training code                               │
│ - Inference scripts                                 │
│ - Base configurations                               │
└─────────────────────────────────────────────────────┘
                        +
┌─────────────────────────────────────────────────────┐
│ LyricsToSongGenerator (This Repo - Data Toolkit)    │
│ - Data preprocessing scripts                        │
│ - Feature extraction tools                          │
│ - Production configs & documentation                │
└─────────────────────────────────────────────────────┘
                        =
            Complete Workflow!
```

## 📦 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/LyricsToSongGenerator.git
cd LyricsToSongGenerator
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Montreal Forced Aligner:
```bash
# Follow the official MFA installation guide
# https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html
```

## 📁 Project Structure

```
LyricsToSongGenerator/
├── src/                          # Source code
│   ├── Extraction_of_meta_data.py    # Feature extraction script
│   └── parse_textgrid.py             # TextGrid parsing for phonemes
├── configs/                      # Configuration files
├── docs/                         # Documentation
│   ├── dataset_preparation.md    # Guide for creating datasets
│   ├── training_guide.md         # Training instructions
│   └── mfa_setup.md             # MFA setup guide
├── examples/                     # Example outputs (samples only)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Pipeline Overview

The complete workflow uses **both repositories**:

```
This Repo (Preprocessing)  →  DiffSinger (Training)  →  Generated Audio
```

### Complete Workflow

#### Phase 1: Data Preparation (This Repo)

**1. Organize your dataset:**

```bash
python src/copy-wavs.py  # If files are in nested folders
```

**2. Run MFA alignment:**

```bash
conda activate mfa

mfa align \
    /path/to/your_dataset \
    english_us_arpa \
    english_us_arpa \
    /path/to/mfa_output \
    --clean
```

**3. Extract features:**

```bash
conda activate diffsinger  # Switch to DiffSinger environment

# Parse TextGrid files
python src/parse_textgrid.py

# Extract mel-spectrograms and F0
python src/Extraction_of_meta_data.py

# Optional: Generate MIDI notes
python src/MIDI_Notes.py
```

**4. Create transcriptions.csv:**

```bash
# From JSON phoneme files
python src/ForTranscriptions.py

# OR from HTK .lab files (for PJS corpus)
python src/lab-to-csv-gen.py
```

**Result:** You now have:
- `dataset/wavs/*.wav` - Audio files
- `dataset/Features/*_phonemes.json` - Phoneme timings
- `dataset/Features/*_mel.npy` - Mel-spectrograms  
- `dataset/Features/*_f0.npy` - F0 contours
- `dataset/transcriptions.csv` - **Critical file for training**

#### Phase 2: DiffSinger Training

**1. Copy configs to DiffSinger:**

```bash
# Copy your production configs
cp configs/acoustic_pjs_corpus.yaml ../DiffSinger/configs/
cp configs/variance_pjs_corpus.yaml ../DiffSinger/configs/
```

**2. Update paths in configs:**

Edit the copied YAML files:
```yaml
datasets:
  - raw_data_dir: /path/to/your/dataset/  # Update this
```

**3. Binarize and train:**

```bash
cd ../DiffSinger

# Binarize acoustic data
python scripts/binarize.py --config configs/acoustic_pjs_corpus.yaml

# Train acoustic model
python scripts/train.py \
    --config configs/acoustic_pjs_corpus.yaml \
    --exp_name my_model \
    --reset

# Binarize variance data
python scripts/binarize.py --config configs/variance_pjs_corpus.yaml

# Train variance model  
python scripts/train.py \
    --config configs/variance_pjs_corpus.yaml \
    --exp_name my_model_var \
    --reset
```

**4. Run inference:**

```bash
# Create a .ds file (see examples/ds_files/)
python scripts/infer.py acoustic ds/test.ds --exp my_model
```

### Before Running Scripts

⚠️ **All scripts have hardcoded paths like `Z:\Robotics_Club\...`**

**Option A: Create config.py (Recommended)**
```python
# config.py
PROJECT_ROOT = "/path/to/your/project"  # Change this one line!
```

**Option B: Update each script manually**
- See [docs/script_configuration.md](docs/script_configuration.md)

### Training

For complete training instructions, see:
- [docs/diffsinger_training.md](docs/diffsinger_training.md) - My production workflow
- [docs/transcriptions_csv_guide.md](docs/transcriptions_csv_guide.md) - Critical CSV format
- [docs/workflows/complete_workflow.md](docs/workflows/complete_workflow.md) - Visual pipeline

## 📚 Documentation

- **[Dataset Preparation Guide](docs/dataset_preparation.md)**: How to prepare your singing voice dataset
- **[MFA Setup Guide](docs/mfa_setup.md)**: Setting up Montreal Forced Aligner
- **[Training Guide](docs/training_guide.md)**: Training your own DiffSinger model

## 🔧 Configuration

Key parameters in the feature extraction:

| Parameter | Value | Description |
|-----------|-------|-------------|
| Sample Rate | 44100 Hz | Audio sample rate |
| FFT Size | 2048 | Fast Fourier Transform window size |
| Hop Length | 512 | Number of samples between frames |
| Mel Bins | 80 | Number of mel-frequency bins |
| F0 Range | C2-C7 | Pitch detection range |

## ⚠️ Important Notes

### Copyright and Data Usage

- **This repository does NOT include any copyrighted audio files or datasets**
- Users are responsible for ensuring they have proper rights to any audio data they use
- Do not train models on copyrighted music without permission
- Commercial use requires appropriate licensing

### Dataset Sources

If you're looking for datasets to use, consider:
- Recording your own vocals (with proper consent if not your voice)
- Using royalty-free music libraries
- Publicly available singing voice datasets with permissive licenses (always check the license)
- Obtaining proper licenses for commercial music

## 🙏 Acknowledgments

This project is built upon the following works:

- **DiffSinger**: Liu, J., Li, C., Ren, Y., Chen, F., & Zhao, Z. (2022). DiffSinger: Singing Voice Synthesis via Shallow Diffusion Mechanism. *AAAI 2022*.
  - Original paper: https://arxiv.org/abs/2105.02446
  - Official repository: https://github.com/openvpi/DiffSinger

- **Montreal Forced Aligner**: McAuliffe, M., Socolof, M., Mihuc, S., Wagner, M., & Sonderegger, M. (2017). Montreal Forced Aligner: Trainable Text-Speech Alignment Using Kaldi.
  - Official repository: https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner

- **Libraries**:
  - PyTorch and torchaudio teams
  - librosa: McFee, B., et al. (2015). librosa: Audio and Music Signal Analysis in Python.
  - TextGrid tools

- **Datasets**: PJS Corpus for testing and validation

## 👨‍💻 About

I'm a student who uses NPTEL and SWAYAM platforms for learning. I built this toolkit while working on my DL major project, documenting everything I learned along the way.

After struggling for weeks to figure out the DiffSinger pipeline, I decided to create the documentation I wish I had when I started. This repository represents months of trial and error, reading scattered documentation, and lots of debugging.

**Tested on:**
- PJS Corpus (Japanese dataset)
- Custom datasets (with varying success based on audio quality)

**GitHub**: [@Ashish00734](https://github.com/Ashish00734)

## 📄 MIT License

**Note**: The license of this code does not grant rights to any copyrighted audio data. Users must obtain proper licenses for any copyrighted content they use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📧 Contact

**Ashish (A5hG0)**
- GitHub: [@A5hG0](https://github.com/A5hG0)
- Repository: [LyricsToSongGenerator](https://github.com/A5hG0/LyricsToSongGenerator)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## ❓ Getting Help

If you're stuck:
1. **Check the documentation** - Most common issues are covered
   - [transcriptions_csv_guide.md](docs/transcriptions_csv_guide.md) - For CSV format issues
   - [script_configuration.md](docs/script_configuration.md) - For path configuration
   - [diffsinger_training.md](docs/diffsinger_training.md) - For training issues

2. **Open an issue** on GitHub with:
   - What you're trying to do
   - What error you're getting
   - What you've already tried

3. **Check DiffSinger's documentation** for training-specific issues
