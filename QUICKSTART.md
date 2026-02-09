# Quick Start Guide

## Installation & Testing

### Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run Installation Test

```bash
python test_installation.py
```

This will verify that all dependencies are installed correctly.

### Step 3: Run Comprehensive Test Suite

```bash
python test_suite.py
```

This runs 10 comprehensive tests covering all major functionality:
- Import verification
- Analyzer initialization
- Signal generation
- FFT computation
- Infrasound detection
- Ultrasound detection
- Full spectrum analysis
- Utility functions
- File I/O operations
- Batch processing

## Quick Usage Examples

### Example 1: Analyze a Single Audio File

```python
from src.analyzer import AudioAnalyzer

analyzer = AudioAnalyzer()
results = analyzer.analyze_full_spectrum('your_audio.wav', mode='full')

print(f"Detected {results['total_events']} events")
for event in results['events']:
    print(f"{event['type']}: {event['frequency_hz']:.2f} Hz")
```

### Example 2: Generate and Analyze Test Signal

```bash
python src/analyzer.py
```

This will:
- Generate a test signal with infrasound (5 Hz) and ultrasound (25 kHz)
- Save it to `data/samples/test_signal.wav`
- Analyze and display detected events

### Example 3: Batch Process Multiple Files

```bash
python src/batch_processor.py --input-dir data/samples --output-dir results --mode full
```

### Example 4: Real-time Monitoring (requires microphone)

```bash
python src/realtime_monitor.py
```

Note: Requires a microphone that supports high sample rates (96kHz+)

### Example 5: Run Use Case Examples

```bash
python examples/use_cases.py
```

This provides interactive examples for:
1. Bat detection
2. Machinery monitoring
3. Rodent detection
4. Real-time alerts
5. Batch processing

## Project Structure

```
beyond-human-audio-analyzer/
├── src/
│   ├── analyzer.py           # Main analysis engine
│   ├── realtime_monitor.py   # Real-time monitoring
│   ├── batch_processor.py    # Batch file processing
│   ├── signal_processing.py  # DSP utilities
│   ├── visualizer.py         # Visualization tools
│   ├── ml_detector.py        # ML detection
│   └── utils.py              # Helper functions
├── config/
│   └── config.yaml           # Configuration settings
├── data/
│   ├── samples/              # Sample audio files
│   └── models/               # ML models
├── results/                  # Analysis results
├── logs/                     # Log files
├── examples/
│   └── use_cases.py          # Example scripts
├── test_installation.py      # Installation test
├── test_suite.py             # Comprehensive tests
└── requirements.txt          # Dependencies
```

## Configuration

Edit `config/config.yaml` to customize:
- Sample rates
- Detection thresholds
- Frequency ranges
- Filter parameters
- Output formats

## Troubleshooting

### Issue: "No module named 'src'"
**Solution**: Run scripts from the project root directory

### Issue: "Config file not found"
**Solution**: Ensure you're in the project root directory where `config/` exists

### Issue: High sample rate not supported
**Solution**: 
- Check your audio interface capabilities
- Lower the sample_rate in `config/config.yaml`
- For ultrasound detection, you need hardware that supports >96kHz

### Issue: No events detected
**Solution**:
- Lower detection thresholds in `config/config.yaml`
- Verify your audio file contains the target frequencies
- Check that sample rate is sufficient (2x highest frequency)

## Next Steps

1. ✅ Run `test_suite.py` to verify everything works
2. 📊 Try the examples in `examples/use_cases.py`
3. 🎵 Analyze your own audio files
4. ⚙️ Customize `config/config.yaml` for your needs
5. 📖 Read the full README.md for detailed documentation

## Support

For issues or questions:
- Check the troubleshooting section above
- Review the comprehensive README.md
- Examine the example scripts in `examples/`
