# Configuration Files

This directory contains example configuration files for DiffSinger training.

## 📁 Files

### `acoustic_pjs_corpus.yaml`
Configuration for training the **acoustic model** (main model that generates mel-spectrograms).

**Key settings:**
- Dataset paths
- Audio parameters (sample rate, FFT size, hop length)
- Model architecture (LynxNet backbone)
- Training parameters (batch size, learning rate)
- Data augmentation settings

### `variance_pjs_corpus.yaml`
Configuration for training the **variance model** (predicts pitch, duration, energy).

**Key settings:**
- Pitch prediction parameters
- Duration prediction parameters
- Energy/breathiness/voicing parameters
- Model architecture (WaveNet backbone)

## ⚙️ How to Use

### 1. Copy and Rename

```bash
cp configs/acoustic_pjs_corpus.yaml configs/acoustic_my_dataset.yaml
cp configs/variance_pjs_corpus.yaml configs/variance_my_dataset.yaml
```

### 2. Update Paths

**Critical paths to update:**

```yaml
datasets:
  - raw_data_dir: Z:\path\to\YOUR_DATASET\dataset\  # ← Change this
    speaker: your_speaker_name                      # ← Change this
    test_prefixes:
      - song_001  # ← Change to your test files
      - song_002

binary_data_dir: Z:\path\to\YOUR_DATASET\binary     # ← Change this
```

### 3. Update Dictionary (if needed)

For English:
```yaml
dictionaries:
  en: dictionaries/opencpop-extension.txt
```

For Japanese:
```yaml
dictionaries:
  ja: dictionaries/japanese.txt
```

### 4. Adjust Test Files

List the files you want to use for validation/testing:

```yaml
test_prefixes:
  - pjs001  # These will be held out for testing
  - pjs002
  - pjs003
```

## 🎯 Key Parameters to Adjust

### For GPU Memory Issues

If you get "CUDA out of memory":

```yaml
max_batch_frames: 2000  # Reduce from 4000
max_batch_size: 4       # Reduce from 8
```

### For Training Speed

```yaml
max_updates: 80000     # Reduce from 160000 for faster (lower quality)
val_check_interval: 1000  # Validate more frequently
```

### For Better Quality

```yaml
max_updates: 200000    # Increase for better convergence
permanent_ckpt_start: 120000  # Save more checkpoints
```

## 📊 Understanding Config Sections

### Audio Processing

```yaml
audio_sample_rate: 44100  # Must match your audio files
hop_size: 512            # Time resolution
fft_size: 2048           # Frequency resolution
win_size: 2048           # Window size
```

### Model Architecture

```yaml
hidden_size: 256         # Model capacity (larger = more parameters)
enc_ffn_kernel_size: 3   # Encoder kernel size
use_rope: true           # Rotary position embeddings
```

### Data Augmentation

```yaml
augmentation_args:
  random_pitch_shifting:
    enabled: true
    range: [-5., 5.]     # Semitones
    scale: 0.75          # Probability
  random_time_stretching:
    enabled: true
    range: [0.5, 2.]     # Speed multipliers
```

### Diffusion Settings

```yaml
diffusion_type: reflow   # Diffusion algorithm
K_step: 300             # Training diffusion steps
K_step_infer: 500       # Inference diffusion steps
sampling_steps: 20      # Inference sampling steps
```

## 🔧 Advanced Settings

### Shallow Diffusion

For faster inference with slight quality tradeoff:

```yaml
use_shallow_diffusion: true
T_start: 0.4            # Start diffusion at 40%
T_start_infer: 0.4      # Inference start point
```

### Multi-Speaker

For multiple voices in one model:

```yaml
use_spk_id: true
num_spk: 3              # Number of speakers

datasets:
  - raw_data_dir: path/to/speaker1
    spk_id: 0
  - raw_data_dir: path/to/speaker2
    spk_id: 1
  - raw_data_dir: path/to/speaker3
    spk_id: 2
```

### Fine-tuning

To fine-tune from a pretrained model:

```yaml
finetune_enabled: true
finetune_ckpt_path: checkpoints/pretrained/model.ckpt
finetune_strict_shapes: true
```

## ✅ Validation Checklist

Before training, verify:

- [ ] `raw_data_dir` points to directory with transcriptions.csv
- [ ] `binary_data_dir` is writeable
- [ ] Dictionary file exists
- [ ] Test files listed in `test_prefixes` exist
- [ ] Audio parameters match your dataset (sample rate, etc.)

## 📚 Documentation

For more details, see:
- [diffsinger_training.md](../docs/diffsinger_training.md) - Complete training guide
- [transcriptions_csv_guide.md](../docs/transcriptions_csv_guide.md) - CSV format guide
- [DiffSinger Official Docs](https://github.com/openvpi/DiffSinger) - Full documentation

## 🆘 Common Issues

**Issue:** "Dictionary not found"
- Check `dictionaries/` folder exists in DiffSinger directory
- Verify dictionary filename matches config

**Issue:** "No such file: transcriptions.csv"
- Must be in `raw_data_dir`
- Check exact path and filename

**Issue:** "Test file not found"
- Files in `test_prefixes` must exist in dataset
- Check spelling and extension

---

**These configs are production-tested and ready to use!**
