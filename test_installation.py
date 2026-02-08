"""
Simple test script to verify installation
"""

import sys
from pathlib import Path

print("=" * 70)
print("TESTING BEYOND HUMAN PERCEPTION AUDIO ANALYZER")
print("=" * 70)

# Test imports
print("\n1. Testing imports...")
try:
    import numpy as np
    print("   ✓ numpy")
except ImportError as e:
    print(f"   ✗ numpy: {e}")
    sys.exit(1)

try:
    import scipy
    print("   ✓ scipy")
except ImportError as e:
    print(f"   ✗ scipy: {e}")
    sys.exit(1)

try:
    import librosa
    print("   ✓ librosa")
except ImportError as e:
    print(f"   ✗ librosa: {e}")
    sys.exit(1)

try:
    import soundfile
    print("   ✓ soundfile")
except ImportError as e:
    print(f"   ✗ soundfile: {e}")
    sys.exit(1)

try:
    import matplotlib
    print("   ✓ matplotlib")
except ImportError as e:
    print(f"   ✗ matplotlib: {e}")
    sys.exit(1)

# Test project imports
print("\n2. Testing project modules...")
sys.path.insert(0, str(Path(__file__).parent))

try:
    from src.analyzer import AudioAnalyzer
    print("   ✓ analyzer module")
except ImportError as e:
    print(f"   ✗ analyzer module: {e}")
    sys.exit(1)

try:
    from src.utils import generate_test_signal
    print("   ✓ utils module")
except ImportError as e:
    print(f"   ✗ utils module: {e}")
    sys.exit(1)

# Test basic functionality
print("\n3. Testing basic functionality...")
try:
    analyzer = AudioAnalyzer()
    print(f"   ✓ Analyzer initialized (sample rate: {analyzer.sample_rate} Hz)")
except Exception as e:
    print(f"   ✗ Analyzer initialization failed: {e}")
    sys.exit(1)

try:
    test_signal = generate_test_signal(1000, 1.0, 48000)
    print(f"   ✓ Signal generation ({len(test_signal)} samples)")
except Exception as e:
    print(f"   ✗ Signal generation failed: {e}")
    sys.exit(1)

# Test FFT computation
print("\n4. Testing FFT computation...")
try:
    frequencies, magnitudes = analyzer.compute_fft(test_signal)
    print(f"   ✓ FFT computed ({len(frequencies)} frequency bins)")
except Exception as e:
    print(f"   ✗ FFT computation failed: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("ALL TESTS PASSED! ✓")
print("=" * 70)
print("\nYour installation is working correctly.")
print("You can now run the analyzer:")
print("  python src/analyzer.py")
print("\nOr try the examples:")
print("  python examples/use_cases.py")
print("=" * 70 + "\n")
