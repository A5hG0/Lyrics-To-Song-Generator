# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-03-22 - PRODUCTION RELEASE

### Added - Complete Production Setup
- **12 actual production scripts** (not recreations)
- **Separate environment requirements** (`requirements-diffsinger.txt`, `requirements-mfa.txt`)
- **Production config files** (`acoustic_pjs_corpus.yaml`, `variance_pjs_corpus.yaml`)
- **Example .ds file** for inference testing
- **Critical transcriptions.csv guide** - Most important documentation
- **Complete DiffSinger training guide** with actual commands used
- **End-to-end workflow documentation** with time estimates
- **Config files README** with parameter explanations
- **Examples directory** with inference samples

### Documentation - Based on Real Experience
- **transcriptions_csv_guide.md** - Critical file format (most searched-for info)
- **diffsinger_training.md** - Actual production workflow
- **workflows/complete_workflow.md** - Full pipeline with diagrams
- **script_configuration.md** - How to update all hardcoded paths
- **configs/README.md** - Configuration parameter guide
- **src/README.md** - Detailed docs for all 12 scripts

### Scripts - All Production Code
1. copy-wavs.py - Dataset organization
2. spliting.py - Advanced audio slicer (207 lines)
3. Extraction_of_meta_data.py - Mel + F0 extraction
4. MIDI_Notes.py - F0 to MIDI conversion
5. Mel-Spectrogram.py - Backup version
6. parse_textgrid.py - TextGrid parser
7. ForTranscriptions.py - JSON to CSV converter
8. lab-to-csv-gen.py - HTK lab file processor
9. ds_maker.py - Create .ds files
10. ds_trimmer.py - Normalize sequences
11. matcher_for_phseq-phdur-f0seq.py - Validation
12. markers_for_audio_slicer.py - AudioSlicer integration

### Production Insights
- Audio quality requirements (studio quality from start)
- Common pitfalls documented
- Actual MFA commands with optimized parameters
- Real training times and resource requirements
- Production-tested workflow

## [1.0.0] - 2025-03-22 - Initial Release

### Added
- Initial repository structure
- Basic feature extraction script
- Basic TextGrid parsing script
- Generic documentation
- MIT License

### Issues
- Only had 2 scripts (not complete pipeline)
- Missing 10 other production scripts
- No actual config files
- No production workflow documentation
- Claimed "improved" code without seeing originals

---

## Version History Format

### [Version] - 2026-03-22

#### Added
- New features

#### Changed
- Changes in existing functionality

#### Fixed
- Bug fixes

#### Removed
- Removed features


