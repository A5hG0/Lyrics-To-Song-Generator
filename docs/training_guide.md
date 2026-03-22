# Training Guide

This guide covers the complete training pipeline for DiffSinger models using your prepared dataset.

## 📋 Prerequisites

Before training, ensure you have completed:

- [x] Dataset preparation (see [dataset_preparation.md](dataset_preparation.md))
- [x] Feature extraction (`Extraction_of_meta_data.py`)
- [x] MFA alignment (see [mfa_setup.md](mfa_setup.md))
- [x] TextGrid parsing (`parse_textgrid.py`)

## 📁 Expected Data Structure

After preprocessing, you should have:

```
dataset/
└── Features/
    ├── audio_001_mel.npy         # Mel-spectrogram
    ├── audio_001_f0.npy          # F0 contour
    ├── audio_001_phonemes.json   # Phoneme alignments
    ├── audio_002_mel.npy
    ├── audio_002_f0.npy
    ├── audio_002_phonemes.json
    └── ...
```

## 🔧 Feature Extraction Details

### What Gets Extracted

1. **Mel-Spectrogram** (`*_mel.npy`)
   - 80-dimensional mel-frequency spectrogram
   - Captures timbral information
   - Computed from audio waveform

2. **F0 Contour** (`*_f0.npy`)
   - Fundamental frequency (pitch) over time
   - Extracted using PYIN algorithm
   - Range: C2 to C7

3. **Phoneme Alignments** (`*_phonemes.json`)
   - Phoneme symbols from MFA
   - Start and end times for each phoneme
   - Parsed from TextGrid files

### Running Feature Extraction

```bash
# Make sure to update paths in the script first
python src/Extraction_of_meta_data.py
```

**Key Parameters:**
- Sample rate: 44,100 Hz
- FFT size: 2,048
- Hop length: 512
- Mel bins: 80

### Verification

Check that features were extracted correctly:

```python
import numpy as np
import json

# Load mel-spectrogram
mel = np.load('dataset/Features/audio_001_mel.npy')
print(f"Mel shape: {mel.shape}")  # Should be (80, num_frames)

# Load F0
f0 = np.load('dataset/Features/audio_001_f0.npy')
print(f"F0 shape: {f0.shape}")    # Should be (num_frames,)

# Load phonemes
with open('dataset/Features/audio_001_phonemes.json', 'r') as f:
    phonemes = json.load(f)
print(f"Phonemes: {phonemes[:5]}")  # First 5 phonemes
```

## 🎯 Training Setup

### 1. Install DiffSinger

Follow the official DiffSinger repository for installation:

```bash
# Clone DiffSinger repository
git clone https://github.com/MoonInTheRiver/DiffSinger.git
cd DiffSinger

# Install dependencies
pip install -r requirements.txt

# Install PyTorch (adjust for your CUDA version)
pip install torch torchvision torchaudio
```

### 2. Organize Data for DiffSinger

DiffSinger expects a specific format. You may need to create a data configuration:

```yaml
# config.yaml example
data:
  dataset_name: "your_dataset"
  data_dir: "path/to/Features"
  sample_rate: 44100
  hop_size: 512
  fft_size: 2048
  mel_bins: 80
  
model:
  hidden_size: 256
  encoder_layers: 4
  decoder_layers: 4
  
training:
  batch_size: 16
  learning_rate: 0.0001
  max_steps: 100000
  save_interval: 5000
```

### 3. Data Preprocessing for DiffSinger

Create the binary data format DiffSinger expects:

```bash
# This step depends on DiffSinger's specific preprocessing
# Refer to DiffSinger documentation for exact commands
python preprocess.py --config config.yaml
```

## 🚀 Training Process

### Starting Training

```bash
# Basic training command
python train.py --config config.yaml

# With GPU specification
CUDA_VISIBLE_DEVICES=0 python train.py --config config.yaml

# Resume from checkpoint
python train.py --config config.yaml --resume checkpoints/model_step_50000.pt
```

### Monitoring Training

1. **TensorBoard**
   ```bash
   tensorboard --logdir=logs/
   ```
   
   Monitor:
   - Training loss
   - Validation loss
   - Mel-spectrogram quality
   - Generated samples

2. **Checkpoints**
   - Saved periodically during training
   - Keep best performing checkpoint
   - Test intermediate checkpoints

### Training Duration

Expected training time depends on:
- Dataset size (hours of audio)
- Model complexity
- Hardware (GPU type)
- Batch size

**Typical times:**
- Small dataset (1 hour): 10-20 hours on modern GPU
- Medium dataset (3 hours): 1-3 days
- Large dataset (10+ hours): 3-7 days

## 📊 Hyperparameters

### Key Parameters to Tune

1. **Learning Rate**
   - Default: 0.0001
   - Too high: Unstable training
   - Too low: Slow convergence

2. **Batch Size**
   - Depends on GPU memory
   - Larger = more stable but slower
   - Typical: 8-32

3. **Model Size**
   - hidden_size: 256-512
   - More parameters = better quality but slower

4. **Training Steps**
   - 100,000-300,000 steps typical
   - Monitor validation loss to prevent overfitting

## 🎼 Inference (Generating Audio)

### After Training

Once training completes:

```bash
# Generate singing voice from text
python inference.py \
    --config config.yaml \
    --checkpoint checkpoints/best_model.pt \
    --text "Your lyrics here" \
    --output output.wav
```

### Controlling Generation

You can control various aspects:

1. **Pitch (F0)**
   - Provide MIDI notes or F0 contour
   - Shift pitch up/down

2. **Duration**
   - Specify phoneme durations
   - Control tempo

3. **Expression**
   - Adjust energy/loudness
   - Control vibrato

## 🔍 Evaluation

### Quality Metrics

1. **Objective Metrics**
   - Mel Cepstral Distortion (MCD)
   - F0 RMSE (Root Mean Square Error)
   - Voicing Decision Error

2. **Subjective Evaluation**
   - Listen to generated samples
   - Compare to ground truth
   - Rate naturalness and intelligibility

### Testing

```python
# Generate test samples
python generate_samples.py \
    --checkpoint best_model.pt \
    --test_set test_data.txt \
    --output_dir samples/
```

## ⚠️ Common Issues

### Problem: Poor Audio Quality

**Solutions:**
- Train longer
- Increase model size
- Improve dataset quality
- Check feature extraction

### Problem: Overfitting

**Symptoms:**
- Training loss decreases, validation loss increases
- Generated audio sounds robotic

**Solutions:**
- Add more training data
- Use data augmentation
- Reduce model complexity
- Add regularization

### Problem: Training Instability

**Symptoms:**
- Loss spikes
- NaN values

**Solutions:**
- Reduce learning rate
- Use gradient clipping
- Check data preprocessing
- Normalize features properly

### Problem: Out of Memory (OOM)

**Solutions:**
- Reduce batch size
- Reduce model size
- Use gradient accumulation
- Use mixed precision training

## 💾 Checkpointing Strategy

Best practices for saving models:

1. **Regular Checkpoints**
   - Save every 5,000-10,000 steps
   - Keep last 3-5 checkpoints

2. **Best Model**
   - Track validation loss
   - Save best performing model separately

3. **Final Model**
   - Save at end of training
   - Include config and preprocessing info

## 🎯 Next Steps After Training

1. **Model Evaluation**
   - Generate test samples
   - Calculate metrics
   - Compare with baseline

2. **Fine-tuning**
   - Adjust hyperparameters
   - Train with more data
   - Experiment with model variants

3. **Deployment**
   - Optimize for inference
   - Create inference API
   - Build user interface

## 📚 Advanced Topics

### Transfer Learning

Use a pre-trained model as starting point:

```bash
python train.py \
    --config config.yaml \
    --pretrained pretrained_model.pt \
    --finetune
```

### Multi-Speaker Training

Train on multiple voices:
- Add speaker embeddings
- Condition on speaker ID
- Requires labeled multi-speaker dataset

### Data Augmentation

Improve generalization:
- Pitch shifting
- Time stretching
- Adding noise
- Speed perturbation

## 🔧 Optimization Tips

1. **Mixed Precision Training**
   ```python
   # Faster training on modern GPUs
   from torch.cuda.amp import autocast, GradScaler
   ```

2. **Distributed Training**
   ```bash
   # Use multiple GPUs
   python -m torch.distributed.launch \
       --nproc_per_node=2 \
       train.py --config config.yaml
   ```

3. **Gradient Accumulation**
   ```python
   # Simulate larger batch size
   accumulation_steps = 4
   ```

## 📝 Documentation

Keep track of:
- Dataset details
- Hyperparameters used
- Training duration
- Best checkpoint info
- Evaluation results

## 📞 Getting Help

If stuck:
1. Check DiffSinger GitHub issues
2. Review your data preprocessing
3. Verify feature extraction
4. Test with smaller model first

---

**Remember**: Training is iterative. Start with a small dataset and simple model, then scale up as you understand the process better.

## 🔗 Related Resources

- [DiffSinger Paper](https://arxiv.org/abs/2105.02446)
- [DiffSinger GitHub](https://github.com/MoonInTheRiver/DiffSinger)
- [Original Documentation](https://github.com/MoonInTheRiver/DiffSinger/wiki)
