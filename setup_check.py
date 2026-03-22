#!/usr/bin/env python3
"""
Setup verification script for LyricsToSongGenerator
Checks if all dependencies are installed and paths are configured correctly.
"""

import sys
import os

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"  ✗ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies...")
    
    dependencies = [
        ('torch', 'PyTorch'),
        ('torchaudio', 'torchaudio'),
        ('librosa', 'librosa'),
        ('numpy', 'numpy'),
        ('textgrid', 'textgrid'),
    ]
    
    all_installed = True
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - Not installed")
            all_installed = False
    
    return all_installed

def check_optional_dependencies():
    """Check optional packages."""
    print("\nChecking optional dependencies...")
    
    optional = [
        ('matplotlib', 'matplotlib'),
        ('pandas', 'pandas'),
        ('yaml', 'PyYAML'),
    ]
    
    for module, name in optional:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ○ {name} - Optional, not installed")

def check_mfa():
    """Check if Montreal Forced Aligner is installed."""
    print("\nChecking Montreal Forced Aligner...")
    
    import subprocess
    try:
        result = subprocess.run(
            ['mfa', 'version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"  ✓ MFA installed: {result.stdout.strip()}")
            return True
        else:
            print("  ✗ MFA command failed")
            return False
    except FileNotFoundError:
        print("  ✗ MFA not found in PATH")
        print("     Install with: conda install -c conda-forge montreal-forced-aligner")
        return False
    except subprocess.TimeoutExpired:
        print("  ✗ MFA command timed out")
        return False

def check_directory_structure():
    """Verify project directory structure."""
    print("\nChecking directory structure...")
    
    required_dirs = [
        'src',
        'docs',
        'configs',
        'examples',
    ]
    
    required_files = [
        'README.md',
        'requirements.txt',
        'LICENSE',
        'src/Extraction_of_meta_data.py',
        'src/parse_textgrid.py',
    ]
    
    all_present = True
    
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ {directory}/ - Missing")
            all_present = False
    
    for filepath in required_files:
        if os.path.isfile(filepath):
            print(f"  ✓ {filepath}")
        else:
            print(f"  ✗ {filepath} - Missing")
            all_present = False
    
    return all_present

def check_gpu():
    """Check if GPU is available."""
    print("\nChecking GPU availability...")
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            print(f"  ✓ GPU available: {gpu_name}")
            print(f"  ✓ Number of GPUs: {gpu_count}")
            return True
        else:
            print("  ○ No GPU detected (CPU training will be slower)")
            return False
    except ImportError:
        print("  ✗ Cannot check GPU (PyTorch not installed)")
        return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("""
1. Prepare your dataset:
   - See docs/dataset_preparation.md
   
2. Update paths in scripts:
   - src/Extraction_of_meta_data.py
   - src/parse_textgrid.py
   
3. Run MFA alignment:
   - See docs/mfa_setup.md
   
4. Extract features:
   - python src/Extraction_of_meta_data.py
   
5. Parse TextGrids:
   - python src/parse_textgrid.py
   
6. Start training:
   - See docs/training_guide.md

For detailed instructions, see USAGE.md
""")

def main():
    """Run all checks."""
    print("="*60)
    print("LyricsToSongGenerator - Setup Verification")
    print("="*60)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_directory_structure(),
    ]
    
    # Optional checks
    check_optional_dependencies()
    check_mfa()
    check_gpu()
    
    print("\n" + "="*60)
    if all(checks):
        print("✓ All required checks passed!")
        print_next_steps()
    else:
        print("✗ Some required checks failed.")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
        print("\nFor MFA installation:")
        print("  conda install -c conda-forge montreal-forced-aligner")
    print("="*60)

if __name__ == "__main__":
    main()
