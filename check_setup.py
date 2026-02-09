"""
Setup Verification Script
Checks dependencies and provides installation guidance
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

print("="*70)
print("BEYOND HUMAN PERCEPTION AUDIO ANALYZER")
print("Setup Verification")
print("="*70)

# Check Python version
print("\n1. Checking Python version...")
py_version = sys.version_info
print(f"   Python {py_version.major}.{py_version.minor}.{py_version.micro}")

if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
    print("   [FAIL] Python 3.8+ required")
    sys.exit(1)
else:
    print("   [OK] Python version compatible")

# Check dependencies
print("\n2. Checking dependencies...")

dependencies = {
    'numpy': 'Core numerical computing',
    'scipy': 'Scientific computing and signal processing',
    'librosa': 'Audio analysis',
    'soundfile': 'Audio file I/O',
    'matplotlib': 'Visualization',
    'yaml': 'Configuration files',
    'sounddevice': 'Real-time audio (optional)',
    'sklearn': 'Machine learning (optional)',
    'pandas': 'Data handling (optional)'
}

installed = []
missing = []

for module, description in dependencies.items():
    try:
        if module == 'yaml':
            __import__('yaml')
        elif module == 'sklearn':
            __import__('sklearn')
        else:
            __import__(module)
        installed.append(module)
        print(f"   [OK] {module:15s} - {description}")
    except ImportError:
        missing.append(module)
        print(f"   [MISSING] {module:15s} - {description}")

# Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Installed: {len(installed)}/{len(dependencies)} packages")
print(f"Missing: {len(missing)} packages")

if missing:
    print("\n" + "="*70)
    print("INSTALLATION REQUIRED")
    print("="*70)
    print("\nTo install missing dependencies, run ONE of these commands:\n")
    
    print("Option 1 - Full Installation (Recommended):")
    print("  pip install -r requirements.txt")
    
    print("\nOption 2 - Minimal Installation (Core features only):")
    print("  pip install numpy scipy matplotlib pyyaml")
    
    print("\nOption 3 - Individual packages:")
    for pkg in missing:
        if pkg == 'yaml':
            print(f"  pip install pyyaml")
        elif pkg == 'sklearn':
            print(f"  pip install scikit-learn")
        else:
            print(f"  pip install {pkg}")
    
    print("\n" + "="*70)
    print("\nAfter installation, run this script again to verify.")
    print("="*70 + "\n")
    sys.exit(1)

else:
    print("\n" + "="*70)
    print("ALL DEPENDENCIES INSTALLED!")
    print("="*70)
    print("\nYou can now run:")
    print("  1. python demo.py              - Quick demonstration")
    print("  2. python test_suite.py        - Comprehensive tests")
    print("  3. python src/analyzer.py      - Main analyzer")
    print("  4. python examples/use_cases.py - Example use cases")
    print("\n" + "="*70 + "\n")
    sys.exit(0)
