# Montreal Forced Aligner (MFA) Setup Guide

This guide will help you set up and use Montreal Forced Aligner for phoneme-level alignment of your singing voice dataset.

## 📋 What is MFA?

Montreal Forced Aligner (MFA) is a tool that automatically aligns speech (or singing) with text transcripts at the phoneme level. It generates TextGrid files that contain precise timing information for each phoneme.

**Why do we need it?**
- DiffSinger requires phoneme-level timing to know when each sound occurs
- Manual annotation would be extremely time-consuming
- MFA automates this process with high accuracy

## 🔧 Installation

### Option 1: Conda Installation (Recommended)

```bash
# Create a new conda environment
conda create -n aligner -c conda-forge montreal-forced-aligner

# Activate the environment
conda activate aligner

# Verify installation
mfa version
```

### Option 2: Using Pip (Alternative)

```bash
pip install montreal-forced-aligner
```

### System Requirements

- **OS**: Windows, macOS, or Linux
- **RAM**: At least 4GB (8GB+ recommended)
- **Disk Space**: ~2GB for MFA and models
- **Python**: 3.8 or higher

## 📦 Downloading Pretrained Models

MFA requires:
1. **Acoustic Model**: Pre-trained model for your language
2. **Dictionary**: Pronunciation dictionary (word → phonemes)

### Download Models

```bash
# List available acoustic models
mfa model download acoustic

# Download English acoustic model
mfa model download acoustic english_us_arpa

# Download English dictionary
mfa model download dictionary english_us_arpa

# List available models
mfa model list
```

### For Other Languages

```bash
# List all available languages
mfa model download acoustic --list

# Example: Download German model
mfa model download acoustic german_mfa

# Download corresponding dictionary
mfa model download dictionary german_mfa
```

## 📁 Preparing Your Data

MFA expects a specific directory structure:

```
input_directory/
├── audio_001.wav
├── audio_001.txt
├── audio_002.wav
├── audio_002.txt
└── ...
```

**Important:**
- Audio files and text files must have matching names
- Text files contain the transcript (lyrics)
- All files in one directory

### Example Transcript File (audio_001.txt)

```
Twinkle twinkle little star, how I wonder what you are.
```

## 🚀 Running Alignment

### Basic Command

```bash
mfa align <input_directory> <dictionary> <acoustic_model> <output_directory>
```

### Example

```bash
# Using the english_us_arpa model
mfa align \
    /path/to/your/dataset \
    english_us_arpa \
    english_us_arpa \
    /path/to/output
```

### With Specific Paths

```bash
# More explicit version
mfa align \
    ~/LyricsToSongGenerator/data/wavs \
    english_us_arpa \
    english_us_arpa \
    ~/LyricsToSongGenerator/data/textgrids \
    --clean
```

### Common Options

```bash
# Run with more verbose output
mfa align input/ dictionary model output/ --verbose

# Use multiple cores for faster processing
mfa align input/ dictionary model output/ -j 4

# Clean temporary files after completion
mfa align input/ dictionary model output/ --clean

# Overwrite existing output
mfa align input/ dictionary model output/ --overwrite
```

## 📊 Understanding the Output

### TextGrid File Structure

MFA generates `.TextGrid` files with three tiers:

1. **Words tier**: Word-level boundaries
2. **Phones tier**: Phoneme-level boundaries
3. **Utterances tier**: Full utterance info

### Example TextGrid Content

```
File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0
xmax = 2.5
tiers? <exists>
size = 2
item []:
    item [1]:
        class = "IntervalTier"
        name = "words"
        xmin = 0
        xmax = 2.5
        intervals: size = 5
        intervals [1]:
            xmin = 0.0
            xmax = 0.5
            text = "hello"
        ...
    item [2]:
        class = "IntervalTier"
        name = "phones"
        xmin = 0
        xmax = 2.5
        intervals: size = 10
        intervals [1]:
            xmin = 0.0
            xmax = 0.15
            text = "HH"
        intervals [2]:
            xmin = 0.15
            xmax = 0.25
            text = "AH"
        ...
```

## 🔍 Validating Your Data

Before running alignment, validate your dataset:

```bash
# Validate dataset structure
mfa validate <input_directory> <dictionary>

# Example
mfa validate ~/data/wavs english_us_arpa
```

This will check for:
- Missing transcriptions
- Audio format issues
- Words not in dictionary
- Other common problems

## ⚠️ Troubleshooting

### Problem: "No alignment found"

**Solutions:**
- Check that audio and text files match
- Verify audio quality (no silence, corruption)
- Ensure transcripts are accurate
- Try with a different acoustic model

### Problem: "Word not in dictionary"

**Solutions:**
- Add missing words to a custom dictionary
- Check spelling in transcripts
- Use Out-Of-Vocabulary (OOV) handling

**Creating Custom Dictionary:**

```bash
# Generate pronunciation for OOV words
mfa g2p <dictionary_name> <input_words.txt> <output_pronunciations.txt>
```

### Problem: Poor alignment quality

**Solutions:**
- Improve audio quality
- Fix transcription errors
- Use language-specific model
- Train custom acoustic model

### Problem: Slow processing

**Solutions:**
- Use multiple CPU cores: `-j 4`
- Process smaller batches
- Ensure enough RAM is available

## 📝 After Alignment

Once MFA completes, you should have:

```
output_directory/
├── audio_001.TextGrid
├── audio_002.TextGrid
└── ...
```

### Next Step: Parse TextGrid Files

Use the provided script to extract phoneme information:

```bash
python src/parse_textgrid.py
```

This extracts:
- Phoneme symbols
- Start times
- End times

And saves them as JSON for DiffSinger training.

## 🎯 Best Practices

1. **Data Quality**
   - Clean, clear audio
   - Accurate transcriptions
   - Consistent format

2. **Processing**
   - Start with a small test batch
   - Verify results before processing full dataset
   - Keep original files as backup

3. **Organization**
   - Use clear directory names
   - Document your process
   - Version control your scripts

4. **Iteration**
   - Check alignment quality manually for a few samples
   - Adjust parameters if needed
   - Re-run if quality is poor

## 📚 Additional Resources

- [MFA Official Documentation](https://montreal-forced-aligner.readthedocs.io/)
- [MFA GitHub Repository](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner)
- [Acoustic Models](https://mfa-models.readthedocs.io/en/latest/acoustic/index.html)
- [Dictionaries](https://mfa-models.readthedocs.io/en/latest/dictionary/index.html)

## 💡 Tips for Singing Voice

Singing differs from speech, so:

- **Expect some misalignments** on sustained notes
- **Vowels may be longer** than in speech models
- **Consider post-processing** to adjust boundaries
- **Test different models** to find the best fit

## 🔧 Advanced: Training Custom Model

If pre-trained models don't work well:

```bash
# Train your own acoustic model
mfa train <input_directory> <dictionary> <output_model_path>

# Example
mfa train \
    ~/data/wavs \
    english_us_arpa \
    ~/models/my_custom_model
```

**When to train custom:**
- Unique singing style
- Specific language/dialect
- Consistent dataset with one voice

---

**Next**: After alignment, proceed to parse the TextGrid files using `parse_textgrid.py`
