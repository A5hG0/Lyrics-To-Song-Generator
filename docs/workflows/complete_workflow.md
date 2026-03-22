# Complete End-to-End Workflow

This document describes the **actual production workflow** used to train DiffSinger models from raw audio.

## 🎯 Overview

```
Raw Audio → Feature Extraction → DiffSinger Training → Singing Voice Synthesis
```

**Time estimate:** 2-3 days for a 150-song dataset (including training)

## 📊 Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: DATA PREPARATION                                       │
└─────────────────────────────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Raw Audio Files                          │
    │ - Celebrity vocals (not recommended)     │
    │ - Studio recordings (recommended)        │
    │ - PJS corpus                             │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Audio Quality Check                      │
    │ ⚠️ CRITICAL: Must be studio quality      │
    │ ⚠️ No background music                    │
    │ ⚠️ Isolated vocals from start             │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Optional: copy-wavs.py                   │
    │ Organize files from nested folders      │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Dataset Structure                        │
    │ dataset/wavs/                            │
    │   ├── song_001.wav                       │
    │   ├── song_002.wav                       │
    │   └── ...                                │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Create Transcriptions                    │
    │ song_001.txt: "Hello world"              │
    │ song_002.txt: "Singing voice"            │
    └──────────────────────────────────────────┘
                             
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: FORCED ALIGNMENT (MFA Environment)                     │
└─────────────────────────────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ conda activate mfa                       │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Montreal Forced Aligner                  │
    │ Command:                                 │
    │ mfa align input/ english_us_arpa \       │
    │   english_us_arpa output/ \              │
    │   --clean --beam 100 \                   │
    │   --retry_beam 400 \                     │
    │   --output_format long_textgrid \        │
    │   --num_jobs 4                           │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ TextGrid Files                           │
    │ mfa_output/                              │
    │   ├── song_001.TextGrid                  │
    │   ├── song_002.TextGrid                  │
    │   └── ...                                │
    └──────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: FEATURE EXTRACTION (DiffSinger Environment)            │
└─────────────────────────────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ conda activate diffsinger                │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ parse_textgrid.py                        │
    │ Extracts phoneme timings                 │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Phoneme JSON Files                       │
    │ Features/                                │
    │   ├── song_001_phonemes.json             │
    │   ├── song_002_phonemes.json             │
    │   └── ...                                │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Extraction_of_meta_data.py               │
    │ Extracts mel-spectrograms & F0           │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Audio Features                           │
    │ Features/                                │
    │   ├── song_001_mel.npy                   │
    │   ├── song_001_f0.npy                    │
    │   ├── song_002_mel.npy                   │
    │   ├── song_002_f0.npy                    │
    │   └── ...                                │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ MIDI_Notes.py (Optional)                 │
    │ Converts F0 to MIDI notes                │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Optional Notes Files                     │
    │ Features/                                │
    │   ├── song_001_notes.json                │
    │   └── ...                                │
    └──────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: TRANSCRIPTIONS.CSV GENERATION                          │
│ ⚠️ MOST CRITICAL STEP - Get this wrong, training fails          │
└─────────────────────────────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ ForTranscriptions.py                     │
    │ OR lab-to-csv-gen.py (for PJS)           │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ transcriptions.csv ⭐ CRITICAL FILE      │
    │ Format:                                  │
    │ name,ph_seq,ph_dur                       │
    │ song_001,HH AH L OW,0.15 0.20 0.13 0.18  │
    │                                          │
    │ Rules:                                   │
    │ ✅ ph_seq length == ph_dur length        │
    │ ✅ No empty values                       │
    │ ✅ Names match WAV files                 │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Validation (IMPORTANT!)                  │
    │ Check CSV format is correct              │
    │ See: transcriptions_csv_guide.md         │
    └──────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 5: DIFFSINGER TRAINING                                    │
└─────────────────────────────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Configure YAML Files                     │
    │ - acoustic_pjs_corpus.yaml               │
    │ - variance_pjs_corpus.yaml               │
    │ Update: raw_data_dir, binary_data_dir    │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Binarize Acoustic Data                   │
    │ python scripts/binarize.py \             │
    │   --config acoustic_pjs_corpus.yaml      │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Binary Data Created                      │
    │ binary/                                  │
    │   ├── train.data                         │
    │   ├── train.meta                         │
    │   ├── valid.data                         │
    │   └── valid.meta                         │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Train Acoustic Model                     │
    │ python scripts/train.py \                │
    │   --config acoustic_pjs_corpus.yaml \    │
    │   --exp_name shinnosuke --reset          │
    │                                          │
    │ Training time: 6-48 hours                │
    │ Monitor with TensorBoard                 │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Binarize Variance Data                   │
    │ python scripts/binarize.py \             │
    │   --config variance_pjs_corpus.yaml      │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Train Variance Model                     │
    │ python scripts/train.py \                │
    │   --config variance_pjs_corpus.yaml \    │
    │   --exp_name shinnosuke_var --reset      │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Trained Models                           │
    │ checkpoints/shinnosuke/                  │
    │   ├── model_ckpt_steps_*.ckpt            │
    │   └── ...                                │
    └──────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STAGE 6: INFERENCE                                              │
└─────────────────────────────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Create .ds File                          │
    │ ds/test.ds with desired phonemes         │
    │ See: examples/ds_files/pjs_test_rc.ds    │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Run Inference                            │
    │ python scripts/infer.py acoustic \       │
    │   ds/test.ds --exp shinnosuke            │
    └──────────────────────────────────────────┘
                             ↓
    ┌──────────────────────────────────────────┐
    │ Generated Audio! 🎵                      │
    │ infer_out/test.wav                       │
    └──────────────────────────────────────────┘
```

## ⏱️ Time Estimates

| Stage | Time (150 songs) |
|-------|------------------|
| Data Preparation | 2-4 hours |
| MFA Alignment | 30-60 minutes |
| Feature Extraction | 30-60 minutes |
| CSV Creation | 10 minutes |
| Binarization | 15-30 minutes |
| Acoustic Training | 12-24 hours |
| Variance Training | 6-12 hours |
| **Total** | **~2-3 days** |

## 🎯 Key Success Factors

### 1. Audio Quality (MOST IMPORTANT)

⚠️ **What I Learned the Hard Way:**

After trying multiple approaches, I can tell you: audio quality makes or breaks your model.

**Don't make my mistakes:**
- ❌ Using vocals separated from commercial songs - The quality was terrible, full of artifacts
- ❌ Having any background music in the source - Even subtle backing tracks ruined training
- ❌ Using inconsistent recording setups - Led to a confused model

**What actually worked:**
- ✅ Studio-quality isolated vocals from the very start
- ✅ Professional recording environment  
- ✅ Clean, high-quality stems without any processing artifacts
- ✅ Consistent quality across ALL files

The time I wasted trying to make separated vocals work taught me: just start with clean recordings. It's not worth the struggle.

### 2. Dataset Size

| Songs | Quality |
|-------|---------|
| < 50 | Poor - not recommended |
| 50-100 | Acceptable for testing |
| 150-300 | Good quality |
| 300-500 | Very good quality |
| 500+ | Professional quality |

### 3. transcriptions.csv Accuracy

This is where most people fail. See [transcriptions_csv_guide.md](transcriptions_csv_guide.md).

**Common mistakes:**
- ph_seq and ph_dur length mismatch
- Wrong phoneme symbols
- Missing files
- Empty values

## 🔄 Optional: Audio Slicing

If your audio files are long (>15 seconds), use `spliting.py`:

```python
# Splits audio into chunks based on phoneme count
python src/spliting.py

# Automatically generates:
# 1. Chunked WAV files
# 2. transcriptions.csv
```

Insert this **before** Stage 4 (transcriptions.csv generation).

## 📝 Checklist

Use this to track your progress:

### Data Preparation
- [ ] Audio files collected
- [ ] Audio quality verified (studio quality, no music)
- [ ] Files organized in dataset/wavs/
- [ ] Transcription .txt files created

### MFA
- [ ] MFA environment set up
- [ ] MFA alignment completed
- [ ] TextGrid files generated

### Feature Extraction
- [ ] DiffSinger environment set up
- [ ] parse_textgrid.py run successfully
- [ ] Extraction_of_meta_data.py run successfully
- [ ] All features verified (*_mel.npy, *_f0.npy, *_phonemes.json)

### Transcriptions CSV
- [ ] transcriptions.csv generated
- [ ] CSV format validated
- [ ] ph_seq and ph_dur lengths match
- [ ] All files referenced in CSV exist

### DiffSinger Training
- [ ] Config files updated with correct paths
- [ ] Acoustic binarization completed
- [ ] Acoustic training started
- [ ] Variance binarization completed
- [ ] Variance training started
- [ ] TensorBoard monitoring set up

### Inference
- [ ] .ds file created
- [ ] Inference run successfully
- [ ] Output audio generated

## 🐛 Common Pitfalls

1. **Using vocals separated from songs** ❌
   - Quality will be poor
   - Use studio recordings instead

2. **Skipping validation steps** ❌
   - Always check transcriptions.csv
   - Verify feature files exist

3. **Wrong environment** ❌
   - Use MFA env for alignment
   - Use DiffSinger env for training

4. **Insufficient data** ❌
   - Minimum 50-100 songs
   - More is better

5. **Not monitoring training** ❌
   - Use TensorBoard
   - Check validation loss

## 📚 Related Documentation

- [transcriptions_csv_guide.md](transcriptions_csv_guide.md) - Critical CSV format guide
- [diffsinger_training.md](diffsinger_training.md) - Detailed training guide
- [mfa_setup.md](mfa_setup.md) - MFA installation and usage
- [script_configuration.md](script_configuration.md) - How to update paths in scripts
- [src/README.md](../src/README.md) - Individual script documentation

---

**Follow this workflow exactly, and you'll successfully train a DiffSinger model!** 🎵
