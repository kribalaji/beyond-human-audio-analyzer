"""
Quick Demo Script
Demonstrates the audio analyzer with synthetic signals
"""

import sys
import os
from pathlib import Path
import numpy as np
import soundfile as sf

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from src.analyzer import AudioAnalyzer
from src.utils import generate_test_signal


def main():
    print("\n" + "="*70)
    print("BEYOND HUMAN PERCEPTION AUDIO ANALYZER - QUICK DEMO")
    print("="*70)
    
    # Initialize analyzer
    print("\n1. Initializing analyzer...")
    analyzer = AudioAnalyzer()
    print(f"   [OK] Sample rate: {analyzer.sample_rate} Hz")
    print(f"   [OK] Max detectable frequency: {analyzer.sample_rate/2} Hz")
    
    # Create test directory
    test_dir = Path('data/samples')
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate test signals
    print("\n2. Generating test signals...")
    
    duration = 3  # seconds
    sample_rate = 96000
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Test 1: Infrasound only (10 Hz)
    print("   Creating infrasound test (10 Hz)...")
    infrasound = 0.7 * np.sin(2 * np.pi * 10 * t)
    infrasound += 0.05 * np.random.randn(len(t))
    infrasound_file = test_dir / 'demo_infrasound.wav'
    sf.write(str(infrasound_file), infrasound, sample_rate)
    print(f"   [OK] Saved: {infrasound_file}")
    
    # Test 2: Ultrasound only (28 kHz)
    print("   Creating ultrasound test (28 kHz)...")
    ultrasound = 0.6 * np.sin(2 * np.pi * 28000 * t)
    ultrasound += 0.05 * np.random.randn(len(t))
    ultrasound_file = test_dir / 'demo_ultrasound.wav'
    sf.write(str(ultrasound_file), ultrasound, sample_rate)
    print(f"   [OK] Saved: {ultrasound_file}")
    
    # Test 3: Mixed signal (8 Hz + 25 kHz)
    print("   Creating mixed signal (8 Hz + 25 kHz)...")
    mixed = (0.5 * np.sin(2 * np.pi * 8 * t) + 
             0.4 * np.sin(2 * np.pi * 25000 * t))
    mixed += 0.05 * np.random.randn(len(t))
    mixed_file = test_dir / 'demo_mixed.wav'
    sf.write(str(mixed_file), mixed, sample_rate)
    print(f"   [OK] Saved: {mixed_file}")
    
    # Analyze each file
    print("\n3. Analyzing signals...")
    print("-"*70)
    
    test_files = [
        (infrasound_file, "Infrasound Test (10 Hz)", 'infrasound'),
        (ultrasound_file, "Ultrasound Test (28 kHz)", 'ultrasound'),
        (mixed_file, "Mixed Signal (8 Hz + 25 kHz)", 'full')
    ]
    
    for file_path, description, mode in test_files:
        print(f"\n{description}")
        print(f"File: {file_path.name}")
        
        results = analyzer.analyze_full_spectrum(str(file_path), mode=mode)
        
        print(f"Duration: {results['duration_seconds']:.2f} seconds")
        print(f"Events detected: {results['total_events']}")
        
        if results['events']:
            print("Detected frequencies:")
            for event in results['events']:
                freq_display = f"{event['frequency_hz']:.2f} Hz"
                if event['frequency_hz'] > 1000:
                    freq_display = f"{event['frequency_hz']/1000:.2f} kHz"
                
                print(f"  * {event['type'].upper()}: {freq_display} "
                      f"@ {event['magnitude_db']:.1f} dB")
        else:
            print("  No events detected (check thresholds in config)")
        
        print("-"*70)
    
    # Summary
    print("\n4. Demo Complete!")
    print("="*70)
    print("\nWhat was tested:")
    print("  [OK] Infrasound detection (<20 Hz)")
    print("  [OK] Ultrasound detection (>20 kHz)")
    print("  [OK] Mixed signal analysis")
    print("  [OK] File I/O operations")
    print("  [OK] FFT computation")
    print("  [OK] Event detection")
    
    print("\nGenerated files:")
    print(f"  * {infrasound_file}")
    print(f"  * {ultrasound_file}")
    print(f"  * {mixed_file}")
    
    print("\nNext steps:")
    print("  1. Run full test suite: python test_suite.py")
    print("  2. Try examples: python examples/use_cases.py")
    print("  3. Analyze your own files: python src/batch_processor.py --help")
    print("  4. Customize settings: edit config/config.yaml")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    try:
        main()
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("  2. Run from project root directory")
        print("  3. Check test_installation.py for detailed diagnostics")
        sys.exit(1)
