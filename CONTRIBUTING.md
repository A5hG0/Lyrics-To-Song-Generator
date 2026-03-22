# Contributing to LyricsToSongGenerator

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. **Search existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, Python version, GPU, etc.)
   - Code snippets or error messages

### Submitting Code

1. **Fork the repository**
2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our coding standards
4. **Test your changes** thoroughly
5. **Commit with clear messages**:
   ```bash
   git commit -m "Add: feature description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** with a clear description

## 📝 Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Example:

```python
def extract_features(audio_path, output_dir):
    """
    Extract mel-spectrogram and F0 features from audio file.
    
    Args:
        audio_path (str): Path to input audio file
        output_dir (str): Directory to save extracted features
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Implementation here
    pass
```

### Documentation

- Update README.md if adding features
- Add comments for complex logic
- Update docstrings when modifying functions
- Create/update guides in `docs/` as needed

## 🧪 Testing

Before submitting:

1. Test with sample data
2. Verify no errors or warnings
3. Check that outputs are as expected
4. Test edge cases

## 📋 Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Documentation is updated
- [ ] Changes are tested
- [ ] Commit messages are clear
- [ ] No unnecessary files included (check .gitignore)
- [ ] No copyrighted content added

## 🎯 Areas We Need Help

- **Documentation**: Improving guides and tutorials
- **Testing**: Creating test cases and validation scripts
- **Features**: See issues labeled "enhancement"
- **Bug fixes**: See issues labeled "bug"
- **Examples**: Adding example scripts and notebooks

## ⚠️ Important Guidelines

### Copyright and Data

- **NEVER** commit copyrighted audio files
- **NEVER** commit pre-trained weights without permission
- **ALWAYS** ensure you have rights to any contributed content
- **RESPECT** licensing of external libraries

### Code Quality

- Write clean, readable code
- Add error handling
- Include logging for debugging
- Avoid hardcoded paths
- Make scripts configurable

### Community Standards

- Be respectful and constructive
- Help others when you can
- Give credit where it's due
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md)

## 🚀 Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/LyricsToSongGenerator.git
   cd LyricsToSongGenerator
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a branch for your work:
   ```bash
   git checkout -b feature/my-feature
   ```

## 📞 Questions?

- Open an issue with the "question" label
- Check existing documentation
- Review closed issues for similar questions

## 🙏 Thank You!

Every contribution, no matter how small, is valuable. I appreciate your time and effort in making this project better!

---

**Ashish Kumar (Ashish00734)**
- GitHub: [@Ashish00734](https://github.com/Ashish00734)

By contributing, you agree that your contributions will be licensed under the same license as this project (MIT License).
