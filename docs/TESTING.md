# Testing & Validation Guide

## Overview

This document provides a complete guide to testing and validating the Beyond Human Perception Audio Analyzer.

## Test Files Created

### 1. `test_installation.py`
**Purpose**: Quick verification that all dependencies are installed
**Run**: `python test_installation.py`
**Tests**:
- Core library imports (numpy, scipy, librosa, etc.)
- Project module imports
- Basic analyzer initialization
- Signal generation
- FFT computation

**Expected Output**: All checks should pass with ✓ marks

### 2. `test_suite.py`
**Purpose**: Comprehensive testing of all functionality
**Run**: `python test_suite.py`
**Tests** (10 total):
1. Basic imports verification
2. Analyzer initialization
3. Signal generation
4. FFT computation and peak detection
5. Infrasound detection (<20 Hz)
6. Ultrasound detection (>20 kHz)
7. Full spectrum analysis
8. Utility functions (dB conversion, normalization, etc.)
9. File I/O operations (save/load audio, export events)
10. Batch processing

**Expected Output**: 10/10 tests passed (100%)

### 3. `demo.py`
**Purpose**: Quick demonstration with synthetic signals
**Run**: `python demo.py`
**Demonstrates**:
- Infrasound detection (10 Hz signal)
- Ultrasound detection (28 kHz signal)
- Mixed signal analysis (8 Hz + 25 kHz)
- File generation and analysis workflow

**Expected Output**: 3 test files created and analyzed successfully

## Testing Workflow

### Quick Test (2 minutes)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run installation test
python test_installation.py

# 3. Run quick demo
python demo.py
```

### Full Test (5 minutes)
```bash
# 1. Run comprehensive test suite
python test_suite.py

# 2. Try example use cases
python examples/use_cases.py
# Select option 1-5 or 'all'

# 3. Test batch processing
python src/batch_processor.py --input-dir data/samples --output-dir results --mode full
```

### Manual Testing
```bash
# 1. Generate test signal
python src/analyzer.py

# 2. Analyze specific file
python -c "from src.analyzer import AudioAnalyzer; a = AudioAnalyzer(); print(a.analyze_full_spectrum('data/samples/test_signal.wav'))"

# 3. Real-time monitoring (requires microphone)
python src/realtime_monitor.py
```

## Validation Checklist

### ✅ Core Functionality
- [ ] Analyzer initializes without errors
- [ ] FFT computation works correctly
- [ ] Infrasound detection (<20 Hz) works
- [ ] Ultrasound detection (>20 kHz) works
- [ ] Full spectrum analysis combines both
- [ ] Peak frequency detection is accurate

### ✅ File Operations
- [ ] Audio files can be loaded
- [ ] Audio files can be saved
- [ ] Events export to JSON
- [ ] Events export to CSV
- [ ] Batch processing works
- [ ] Reports are generated

### ✅ Signal Processing
- [ ] Bandpass filtering works
- [ ] Preprocessing (DC removal, normalization) works
- [ ] Spectrogram computation works
- [ ] FFT produces correct frequencies

### ✅ Utilities
- [ ] dB conversions are accurate
- [ ] Signal generation works
- [ ] Frequency content estimation works
- [ ] Audio normalization works

## Expected Results

### Test Signal Analysis
When analyzing the generated test signals, you should see:

**Infrasound (10 Hz)**:
- Type: INFRASOUND
- Frequency: ~10 Hz (±2 Hz)
- Magnitude: > -40 dB

**Ultrasound (28 kHz)**:
- Type: ULTRASOUND
- Frequency: ~28,000 Hz (±500 Hz)
- Magnitude: > -50 dB

**Mixed Signal**:
- 2 events detected
- One infrasound (~8 Hz)
- One ultrasound (~25,000 Hz)

## Performance Benchmarks

### Processing Speed
- Single file (3 seconds): < 1 second
- Batch (10 files): < 10 seconds
- Real-time: < 100ms latency

### Accuracy
- Frequency detection: ±1% of actual frequency
- Peak detection: > 95% for signals > threshold
- False positive rate: < 5% with default settings

## Troubleshooting Test Failures

### Test 1-3 Fail (Import/Initialization)
**Problem**: Dependencies not installed
**Solution**: 
```bash
pip install -r requirements.txt
```

### Test 4 Fails (FFT)
**Problem**: Numerical computation issue
**Solution**: Check numpy/scipy versions, reinstall if needed

### Test 5-6 Fail (Detection)
**Problem**: Thresholds too high or signal too weak
**Solution**: Lower thresholds in `config/config.yaml`

### Test 7 Fails (Full Analysis)
**Problem**: File I/O or path issues
**Solution**: Ensure `data/samples/` directory exists

### Test 9 Fails (File Operations)
**Problem**: Permission or path issues
**Solution**: Check write permissions for `data/` and `results/` directories

### Test 10 Fails (Batch Processing)
**Problem**: Missing files or directory issues
**Solution**: Ensure test files are created in `data/samples/batch_test/`

## Success Criteria

The system is considered fully functional when:

1. ✅ All 10 tests in `test_suite.py` pass
2. ✅ `demo.py` runs without errors
3. ✅ Test signals are correctly analyzed
4. ✅ Files are created in `data/samples/`
5. ✅ Results are exported to `results/`
6. ✅ No critical errors in logs

## Files Generated During Testing

After running all tests, you should have:

```
data/samples/
├── test_signal.wav          (from analyzer.py)
├── test_infrasound.wav      (from test_suite.py)
├── test_ultrasound.wav      (from test_suite.py)
├── test_mixed.wav           (from test_suite.py)
├── test_io.wav              (from test_suite.py)
├── demo_infrasound.wav      (from demo.py)
├── demo_ultrasound.wav      (from demo.py)
├── demo_mixed.wav           (from demo.py)
└── batch_test/              (from test_suite.py)
    ├── test_batch_1.wav
    ├── test_batch_2.wav
    └── test_batch_3.wav

results/
├── test_events.json         (from test_suite.py)
├── test_events.csv          (from test_suite.py)
└── batch_test/              (from test_suite.py)
    ├── analysis_report_*.json
    ├── analysis_report_*.csv
    └── analysis_summary_*.txt
```

## Continuous Testing

For ongoing development:

```bash
# Run quick validation
python test_installation.py && python demo.py

# Run full test suite
python test_suite.py

# Test specific functionality
python -m pytest tests/ -v  # If pytest tests are added
```

## Next Steps After Successful Testing

1. ✅ Analyze real audio files
2. ✅ Customize configuration for your use case
3. ✅ Integrate into your workflow
4. ✅ Deploy for production use
5. ✅ Monitor and log results

## Support

If tests fail consistently:
1. Check Python version (3.8+ required)
2. Verify all dependencies installed
3. Review error messages carefully
4. Check file permissions
5. Ensure sufficient disk space
6. Review `logs/analyzer.log` for details

## Conclusion

This testing framework ensures the audio analyzer works correctly across all major functionality. All tests should pass before using the system for production analysis.
