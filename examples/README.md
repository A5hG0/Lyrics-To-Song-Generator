# Examples

This directory contains example files and outputs from the DiffSinger pipeline.

## 📁 Directory Structure

```
examples/
├── ds_files/              # Example .ds files for inference
│   └── pjs_test_rc.ds    # Sample inference file
├── transcriptions/        # Example transcriptions.csv files
└── README.md             # This file
```

## 🎵 ds_files/

### What are .ds files?

`.ds` files contain instructions for DiffSinger inference. They specify:
- Phoneme sequence (`ph_seq`)
- Phoneme durations (`ph_dur`)  
- Pitch contour (`f0_seq`)
- Speaker ID, language ID
- Pitch shift, speed adjustments

### Example: `pjs_test_rc.ds`

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

**Field descriptions:**

| Field | Description | Example |
|-------|-------------|---------|
| `ph_seq` | Space-separated phonemes | `"HH AH L OW"` |
| `ph_dur` | Duration per phoneme (seconds) | `"0.15 0.20 0.13 0.18"` |
| `f0_seq` | Pitch in Hz (0 = unvoiced) | `"150 155 160 0"` |
| `f0_timestep` | Time per F0 frame (seconds) | `0.0116` |
| `lang_id` | Language identifier | `1` (Japanese) |
| `spk_id` | Speaker identifier | `0` |
| `pitch_shift` | Semitones to shift | `-3` to `+3` |
| `speed` | Speed multiplier | `0.5` to `2.0` |

### Creating Your Own .ds Files

#### Method 1: From Dataset

Use `ds_maker.py` to create from extracted features:

```bash
python src/ds_maker.py
```

This creates a .ds file from:
- `*_phonemes.json`
- `*_f0.npy`

#### Method 2: Manual Creation

```json
[
  {
    "ph_seq": "YOUR PHONEMES HERE",
    "ph_dur": "0.1 0.2 0.15 ...",
    "f0_seq": "150 155 160 ...",
    "f0_timestep": 0.0116,
    "lang_id": 1,
    "spk_id": 0,
    "pitch_shift": 0,
    "speed": 1.0
  }
]
```

**Important:**
- Number of phonemes must equal number of durations
- F0 sequence length can be different
- Save as `.ds` extension

### Running Inference

```bash
python scripts/infer.py acoustic ds/pjs_test.ds --exp your_model_name
```

Output will be saved in `infer_out/`

## 📚 Related Documentation

- [diffsinger_training.md](../docs/diffsinger_training.md) - How to train models
- [src/README.md](../src/README.md) - Scripts that create .ds files
- [transcriptions_csv_guide.md](../docs/transcriptions_csv_guide.md) - CSV format guide

---

**Use these examples as templates for your own inference experiments!** 🎵
