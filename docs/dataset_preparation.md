# Dataset Preparation Guide

This guide explains how to prepare a singing voice dataset for training with DiffSinger.

## 📋 Overview

A proper dataset for singing voice synthesis requires:
1. **Audio files**: Clean vocal recordings (preferably isolated vocals)
2. **Transcriptions**: Lyrics/text for each audio file
3. **Proper licensing**: Legal rights to use the audio

## ⚠️ Legal and Ethical Considerations

### Before You Start

**DO:**
- ✅ Record your own voice (with proper setup)
- ✅ Use royalty-free music with appropriate licenses
- ✅ Use publicly available datasets with permissive licenses
- ✅ Obtain written permission for copyrighted content
- ✅ Check the license terms carefully

**DON'T:**
- ❌ Use copyrighted music without permission
- ❌ Extract vocals from commercial songs without rights
- ❌ Distribute copyrighted datasets
- ❌ Train on someone's voice without their consent

### Recommended Dataset Sources

1. **Your Own Recordings**
   - Record yourself singing
   - Ensure clean, high-quality audio
   - Maintain consistent recording conditions

2. **Public Domain Music**
   - Music where copyright has expired
   - Check your jurisdiction's copyright laws

3. **Creative Commons Licensed Music**
   - Look for CC-BY or CC0 licenses
   - Always attribute as required

4. **Academic Datasets**
   - Some universities provide singing voice datasets
   - Check usage restrictions carefully

## 🎙️ Audio Requirements

### Format Specifications

- **Format**: WAV (uncompressed)
- **Sample Rate**: 44.1 kHz or 48 kHz
- **Bit Depth**: 16-bit or 24-bit
- **Channels**: Mono (single channel)
- **Duration**: 3-10 seconds per file (ideal)

### Quality Guidelines

1. **Clean Vocals**
   - Isolated vocals (no instrumental backing if possible)
   - Minimal background noise
   - No clipping or distortion
   - Consistent volume levels

2. **Recording Environment**
   - Quiet room with minimal echo
   - Use a pop filter
   - Consistent microphone distance
   - Same microphone throughout

3. **Performance Quality**
   - Clear pronunciation
   - Consistent tone and style
   - Avoid excessive vibrato (unless desired in output)
   - Natural breathing patterns

## 📝 Creating Transcriptions

### File Naming Convention

```
audio_001.wav  →  audio_001.txt
audio_002.wav  →  audio_002.txt
```

### Transcription Format

Each text file should contain:
- The exact lyrics sung in the audio
- Use standard spelling (not phonetic)
- Include punctuation
- One line per audio file

Example:
```
Twinkle twinkle little star, how I wonder what you are.
```

### Transcription Tips

1. **Accuracy is crucial**
   - Match exactly what is sung
   - Include all words, even repeated ones
   - Handle hums/vocalizations: use "mm" or "ah"

2. **Language Considerations**
   - Use consistent language encoding (UTF-8)
   - For non-English: ensure proper character support
   - Maintain consistent capitalization

## 📁 Dataset Directory Structure

### Recommended Structure

```
your_dataset/
├── wavs/                    # All audio files
│   ├── song_001.wav
│   ├── song_002.wav
│   └── ...
├── transcripts/             # All transcription files
│   ├── song_001.txt
│   ├── song_002.txt
│   └── ...
└── metadata.csv            # Optional: metadata file
```

### Alternative Structure (MFA-ready)

```
your_dataset/
├── song_001.wav
├── song_001.txt
├── song_002.wav
├── song_002.txt
└── ...
```

## 🔧 Preprocessing Steps

### 1. Vocal Isolation (if needed)

If your audio has instrumental backing:

**Tools:**
- Spleeter (Open source)
- Ultimate Vocal Remover (UVR)
- iZotope RX (Professional)
- Demucs (AI-based)

**Command example (Spleeter):**
```bash
spleeter separate -p spleeter:2stems -o output/ your_song.mp3
```

### 2. Audio Normalization

Ensure consistent volume across all files:

```python
import librosa
import soundfile as sf
import numpy as np

# Load audio
audio, sr = librosa.load('input.wav', sr=44100)

# Normalize to -20 dB
target_dB = -20.0
current_dB = 20 * np.log10(np.sqrt(np.mean(audio**2)))
gain = 10**((target_dB - current_dB) / 20)
audio_normalized = audio * gain

# Save
sf.write('output.wav', audio_normalized, sr)
```

### 3. Format Conversion

Convert all files to the required format:

```bash
# Using ffmpeg
ffmpeg -i input.mp3 -ar 44100 -ac 1 -sample_fmt s16 output.wav
```

### 4. Quality Check

Before proceeding, verify:
- [ ] All files are in WAV format
- [ ] Sample rate is consistent (44.1 kHz)
- [ ] All files are mono
- [ ] No clipping or distortion
- [ ] Each audio file has a matching transcript
- [ ] File names match exactly (except extension)

## 📊 Dataset Size Recommendations

### Minimum Requirements
- **Files**: 100-200 audio clips
- **Duration**: 10-20 minutes total
- **Variety**: Different phonemes and musical contexts

### Recommended
- **Files**: 500-1000 audio clips
- **Duration**: 1-2 hours total
- **Variety**: Wide range of pitches, dynamics, and expressions

### Professional Quality
- **Files**: 2000+ audio clips
- **Duration**: 3-5+ hours total
- **Variety**: Comprehensive coverage of vocal range and styles

## 🎵 Content Diversity

Ensure your dataset includes:

1. **Phonetic Coverage**
   - All vowels (A, E, I, O, U)
   - All consonants
   - Common phoneme combinations
   - Diphthongs and blends

2. **Pitch Range**
   - Low notes
   - Mid range
   - High notes
   - Transitions between registers

3. **Dynamics**
   - Soft singing (piano)
   - Normal volume (mezzo)
   - Loud singing (forte)

4. **Articulation**
   - Legato (smooth)
   - Staccato (short)
   - Normal articulation

## 🔍 Quality Control Checklist

Before using your dataset:

- [ ] All files load without errors
- [ ] Audio quality is consistent
- [ ] Transcriptions are accurate
- [ ] No duplicate files
- [ ] File naming is consistent
- [ ] Total dataset size is adequate
- [ ] You have legal rights to all content
- [ ] Backup of original files exists

## 📚 Example Datasets (Reference Only)

These are examples of publicly available singing datasets (check licenses):

1. **NUS-48E Sung and Spoken Lyrics Corpus**
   - English singing
   - Research purposes
   - Check current license

2. **DAMP (Digital Archive of Mobile Performances)**
   - User-contributed singing
   - Check usage terms

3. **Kakao Singing Voice Dataset**
   - Korean singing
   - Research license

**Always verify licenses before use!**

## 🚀 Next Steps

After preparing your dataset:

1. Run feature extraction (`Extraction_of_meta_data.py`)
2. Perform forced alignment with MFA
3. Parse TextGrid files (`parse_textgrid.py`)
4. Begin training

## 💡 Tips and Best Practices

1. **Start Small**: Test with a small dataset first
2. **Consistency**: Keep recording conditions identical
3. **Backup**: Always keep original recordings
4. **Documentation**: Note any issues or special cases
5. **Incremental**: Can always add more data later

## ⚠️ Common Pitfalls to Avoid

- ❌ Inconsistent audio quality
- ❌ Background noise
- ❌ Incorrect transcriptions
- ❌ Mixed languages without proper handling
- ❌ Copyrighted content without permission
- ❌ Too short audio clips (<2 seconds)
- ❌ Too long audio clips (>15 seconds)

## 📞 Need Help?

If you're stuck:
1. Check MFA documentation for alignment issues
2. Verify audio format compatibility
3. Review transcription accuracy
4. Test with a small subset first

---

**Remember**: Quality over quantity. A smaller, high-quality dataset will outperform a large, noisy one.
