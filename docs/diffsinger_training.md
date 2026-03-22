# Complete DiffSinger Training Guide

This guide is based on the **actual production setup** used for this project.

## 📋 Prerequisites

✅ Completed feature extraction (mel, F0, phonemes)  
✅ Created `transcriptions.csv` (see [transcriptions_csv_guide.md](transcriptions_csv_guide.md))  
✅ DiffSinger repository cloned and set up  
✅ Two separate conda/virtual environments (recommended)  

## 🔧 Environment Setup

### Option 1: Separate Environments (Recommended)

**MFA Environment:**
```bash
conda create -n mfa -c conda-forge montreal-forced-aligner python=3.10
conda activate mfa
# Or: pip install -r requirements-mfa.txt
```

**DiffSinger Environment:**
```bash
conda create -n diffsinger python=3.10
conda activate diffsinger
pip install -r requirements-diffsinger.txt

# Install PyTorch with CUDA (adjust for your CUDA version)
pip install torch==2.4.1+cu118 torchaudio==2.4.1+cu118 torchvision==0.19.1+cu118 -f https://download.pytorch.org/whl/torch_stable.html
```

### Option 2: Single Environment (If you must)

Create a combined `requirements-combined.txt` and install everything, but note:
- librosa version conflict (0.9.2 vs 0.11.0)
- numpy version conflict (1.23.5 vs 2.2.6)

**Not recommended due to version conflicts!**

## 📁 Required Directory Structure

Your dataset directory should match this structure:

```
PJS_corpus_ver1.1/
├── dataset/
│   ├── wavs/
│   │   ├── pjs001.wav
│   │   ├── pjs002.wav
│   │   └── ...
│   └── transcriptions.csv   ← CRITICAL FILE
├── binary/                   ← Generated during binarization
└── binary_variance/          ← Generated during variance binarization
```

## ⚙️ Configuration Files

You need TWO config files for training:

### 1. Acoustic Model Config

**File:** `configs/acoustic_pjs_corpus.yaml`

Key sections to update:

```yaml
# Dataset location
datasets:
  - raw_data_dir: Z:\path\to\PJS_corpus_ver1.1\dataset\  # ← Update this path
    speaker: pjs
    spk_id: 0
    language: ja  # or 'en' for English
    test_prefixes:
      - pjs001  # Update with your test file names
      - pjs002
      - pjs003

# Binary output directory
binary_data_dir: Z:\path\to\PJS_corpus_ver1.1\binary  # ← Update this path

# Phoneme dictionary
dictionaries:
  ja: dictionaries/japanese.txt  # or dictionaries/opencpop-extension.txt for English
```

See the included `configs/acoustic_pjs_corpus.yaml` for full example.

### 2. Variance Model Config

**File:** `configs/variance_pjs_corpus.yaml`

Similar structure to acoustic config:

```yaml
datasets:
  - raw_data_dir: Z:\path\to\PJS_corpus_ver1.1\dataset\
    speaker: pjs
    spk_id: 0
    language: ja
    test_prefixes:
      - pjs001
      - pjs002

binary_data_dir: Z:\path\to\PJS_corpus_ver1.1\binary_variance
```

## 🚀 Training Workflow

### Step 1: Binarize Acoustic Data

```bash
# Activate DiffSinger environment
conda activate diffsinger

# Navigate to DiffSinger directory
cd path/to/DiffSinger

# Run binarization
python scripts/binarize.py --config configs/acoustic_pjs_corpus.yaml
```

**What this does:**
- Reads `transcriptions.csv`
- Processes all audio files
- Creates binary data for faster training
- Generates `binary/` directory with `.data` and `.meta` files

**Expected output:**
```
binary/
├── dictionary-en.txt  (or dictionary-ja.txt)
├── lang_map.json
├── spk_map.json
├── phoneme_distribution.jpg
├── train.data
├── train.meta
├── valid.data
└── valid.meta
```

**Common errors:**
- "File not found": Check `raw_data_dir` path
- "Phoneme mismatch": Check transcriptions.csv (see troubleshooting below)
- "No transcriptions.csv": Must be in `raw_data_dir`

### Step 2: Train Acoustic Model

```bash
python scripts/train.py \
    --config configs/acoustic_pjs_corpus.yaml \
    --exp_name shinnosuke \  # Your experiment name
    --reset  # Start fresh (omit to resume)
```

**Training parameters (from config):**
```yaml
max_updates: 160000          # Total training steps
val_check_interval: 2000     # Validation every N steps
max_batch_frames: 4000       # Adjust based on GPU memory
max_batch_size: 8           # Batch size
```

**Monitoring:**
```bash
# In another terminal, start TensorBoard
tensorboard --logdir checkpoints/
```

Navigate to `http://localhost:6006` to see:
- Training loss
- Validation loss
- Generated samples
- Mel-spectrogram comparisons

**Training time:**
- Small dataset (50 songs): ~6-12 hours on RTX 3090
- Medium dataset (200 songs): ~1-2 days
- Large dataset (500+ songs): 3-5 days

### Step 3: Binarize Variance Data

```bash
python scripts/binarize.py --config configs/variance_pjs_corpus.yaml
```

Creates `binary_variance/` directory.

### Step 4: Train Variance Model

```bash
python scripts/train.py \
    --config configs/variance_pjs_corpus.yaml \
    --exp_name shinnosuke_var \
    --reset
```

**Note:** Can train acoustic and variance models simultaneously if you have enough GPU memory.

### Step 5: Inference (Testing)

Create a `.ds` file with your desired input (see `examples/ds_files/pjs_test_rc.ds` for format):

```json
[
  {
    "ph_seq": "r r o b o t i k s pau k r a b b pau",
    "ph_dur": "0.1 0.25 0.1 0.25 0.15 0.2 0.2 0.07 0.2 0.4 0.12 0.2 0.2 0.2 0.1 0.3",
    "f0_seq": "150 155 155 160 160 160 165 165 165 0 155 155 120 110 180",
    "f0_timestep": 0.0116,
    "lang_id": 1,
    "spk_id": 0,
    "pitch_shift": 0,
    "speed": 1.4
  }
]
```

Run inference:
```bash
python scripts/infer.py acoustic ds/pjs_test.ds --exp shinnosuke
```

**Output:** Generated WAV file in `infer_out/`

## 🎯 MFA Integration

The production workflow used these **exact MFA commands**:

```bash
# Activate MFA environment
conda activate mfa

# Run alignment with optimized settings
mfa align \
    Z:\Robotics_Club\DL_MAJOR\mfa_test \
    english_us_arpa \
    english_us_arpa \
    Z:\Robotics_Club\DL_MAJOR\mfa_output_new_v2 \
    --clean \
    --beam 100 \
    --retry_beam 400 \
    --output_format long_textgrid \
    --num_jobs 4
```

**Parameter explanations:**
- `--beam 100`: Beam width for decoding (higher = more accurate, slower)
- `--retry_beam 400`: Retry beam for difficult alignments
- `--output_format long_textgrid`: Full TextGrid format
- `--num_jobs 4`: Use 4 CPU cores
- `--clean`: Remove temporary files after completion

## 🐛 Troubleshooting

### Issue: "Phoneme mismatch in transcriptions.csv"

**Symptom:** Binarization fails with length mismatch errors

**Solution:**
```bash
# Use the validation script
python src/matcher_for_phseq-phdur-f0seq.py
```

Or manually check:
```python
import pandas as pd

df = pd.read_csv('dataset/transcriptions.csv')
for idx, row in df.iterrows():
    ph_seq_len = len(row['ph_seq'].split())
    ph_dur_len = len(row['ph_dur'].split())
    if ph_seq_len != ph_dur_len:
        print(f"ERROR: {row['name']} - ph_seq:{ph_seq_len} != ph_dur:{ph_dur_len}")
```

### Issue: "CUDA out of memory"

**Solution:** Reduce batch size in config:
```yaml
max_batch_frames: 2000  # Reduce from 4000
max_batch_size: 4       # Reduce from 8
```

### Issue: "No such file or directory: transcriptions.csv"

**Solution:** Ensure `transcriptions.csv` is in `raw_data_dir`:
```bash
ls Z:\path\to\dataset/transcriptions.csv
```

### Issue: "Dictionary file not found"

**Solution:** Check dictionary path in config:
```yaml
dictionaries:
  ja: dictionaries/japanese.txt  # Must exist in DiffSinger/dictionaries/
```

### Issue: "Training loss not decreasing"

**Possible causes:**
1. **Bad audio quality** - Use studio-quality isolated vocals
2. **Incorrect transcriptions** - Verify phonemes match audio
3. **Learning rate too high/low** - Try adjusting:
   ```yaml
   optimizer_args:
     lr: 0.0003  # Try 0.0003 instead of 0.0006
   ```
4. **Not enough data** - Minimum 50-100 songs recommended

## 💡 Best Practices (What I Learned)

### Audio Quality

⚠️ **From My Experience - This is Critical:**

I cannot stress this enough: **use studio-quality isolated vocals from the start.** 

I made the mistake of trying to train on vocals that I separated from commercial songs using AI tools. The results were terrible. The model learned the artifacts and separation noise instead of the actual voice characteristics.

**What worked for me:**
1. **Studio-quality recordings** - Professional isolated vocals from the beginning
2. **No background music** - Pure vocals only, not vocals extracted from mixed songs  
3. **Consistent recording environment** - Same microphone, same room conditions
4. **Clean from the start** - Don't rely on separation tools

**What didn't work:**
- ❌ Vocals separated from commercial songs (even with best AI tools)
- ❌ Audio with background music "from the beginning onwards"
- ❌ Mixed quality recordings
- ❌ Inconsistent recording setups

### Dataset Preparation

1. **Minimum dataset size:** 50-100 songs for acceptable quality
2. **Optimal dataset size:** 200-500 songs for good quality
3. **Test set:** Reserve 5-10 songs for testing (specified in `test_prefixes`)

### Training Tips

1. **Monitor validation loss** - Should decrease steadily
2. **Listen to samples** - Check generated audio quality regularly
3. **Save checkpoints** - Keep every 10,000 steps
4. **Use TensorBoard** - Essential for monitoring progress

## 📊 Expected Results

### After Binarization

```
Processing: 100%|██████████| 150/150 [02:30<00:00]
Train samples: 135
Valid samples: 15
Binary data saved to: binary/
```

### During Training

```
Epoch 1/100: 100%|██████████| 1000/1000 [05:23<00:00]
Train loss: 0.523
Valid loss: 0.612
Generated 10 samples
```

### After Training

- Checkpoint files in `checkpoints/shinnosuke/`
- Generated samples in validation logs
- TensorBoard logs showing convergence

## 🔄 Complete Workflow Summary

```
1. Prepare Dataset
   └── Audio (WAV) + Transcripts (TXT)

2. Run MFA
   └── mfa align ... → TextGrid files

3. Extract Features
   └── parse_textgrid.py → phoneme JSONs
   └── Extraction_of_meta_data.py → mel + F0

4. Create transcriptions.csv
   └── ForTranscriptions.py

5. DiffSinger Training
   └── binarize.py (acoustic)
   └── train.py (acoustic)
   └── binarize.py (variance)
   └── train.py (variance)

6. Inference
   └── infer.py → Generated audio!
```

## 📚 Additional Resources

- [DiffSinger Official Repo](https://github.com/openvpi/DiffSinger)
- [transcriptions_csv_guide.md](transcriptions_csv_guide.md) - Critical CSV format guide
- [mfa_setup.md](mfa_setup.md) - MFA installation and usage

---

**Good luck with your training!** 🎵
