# Getting Started Guide
## Beyond Human Perception Audio Analyzer

### Quick Start (5 Minutes)

This guide will get you up and running with the audio analyzer in under 5 minutes.

---

## Step 1: Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Audio interface capable of high sample rates (96kHz+ recommended)

### Install Dependencies

```bash
# Navigate to project directory
cd beyond-human-audio-analyzer

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

**Note**: If you encounter errors installing PyAudio on Windows, download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it manually.

---

## Step 2: Test Your Setup

Run the test script to verify everything is working:

```bash
python src/analyzer.py
```

This will:
- Generate a synthetic test signal with both infrasound (5 Hz) and ultrasound (25 kHz)
- Analyze the signal
- Display detected events

**Expected Output:**
```
Beyond Human Perception Audio Analyzer
======================================================
Sample Rate: 96000 Hz
Maximum Detectable Frequency: 48000 Hz
======================================================

Generating test signals...
Saved test signal to /home/claude/test_signal.wav

Analyzing test signal...

Analysis Results:
Duration: 5.00 seconds
Total events detected: 2
  - INFRASOUND: 5.00 Hz @ -6.0 dB
  - ULTRASOUND: 25000.00 Hz @ -10.5 dB
```

---

## Step 3: Analyze Your First Audio File

### Basic Analysis

```bash
python src/analyzer.py --input your_audio_file.wav --mode full
```

### Options:
- `--mode infrasound`: Only detect infrasound (<20Hz)
- `--mode ultrasound`: Only detect ultrasound (>20kHz)
- `--mode full`: Detect both (default)

---

## Step 4: Real-Time Monitoring

Monitor audio in real-time from your microphone:

```bash
python src/realtime_monitor.py
```

### First Time Setup:
1. The script will list all available audio devices
2. Note the device number for your high-quality microphone
3. Run: `python src/realtime_monitor.py --device <number>`

**Example:**
```bash
# List devices
python src/realtime_monitor.py --list-devices

# Use device #2 for monitoring
python src/realtime_monitor.py --device 2 --duration 60
```

---

## Step 5: Batch Processing

Process multiple audio files at once:

```bash
python src/batch_processor.py \
    --input-dir ./audio_files \
    --output-dir ./results \
    --mode full
```

This will:
- Process all audio files in `./audio_files`
- Generate reports in `./results` directory
- Create JSON, CSV, and text summary reports

---

## Understanding the Results

### Event Detection Output

Each detected event includes:
- **Type**: `infrasound` or `ultrasound`
- **Frequency**: The detected frequency in Hz
- **Magnitude**: Signal strength in dB
- **Timestamp**: When the event occurred (for real-time monitoring)

### Example Output:
```
INFRASOUND: 8.50 Hz @ -35.2 dB
  - Possible source: Machinery, earthquakes, weather
  
ULTRASOUND: 23,450 Hz @ -42.1 dB
  - Possible source: Bats, rodents, electronic devices
```

---

## Common Use Cases

### 1. Wildlife Monitoring
Detect bat echolocation calls or rodent communication:

```python
from src.analyzer import AudioAnalyzer

analyzer = AudioAnalyzer()
results = analyzer.analyze_full_spectrum('forest_recording.wav', mode='ultrasound')

for event in results['events']:
    if 20000 <= event['frequency_hz'] <= 50000:
        print(f"Bat call detected: {event['frequency_hz']:.0f} Hz")
```

### 2. Industrial Monitoring
Monitor machinery for abnormal infrasound vibrations:

```python
analyzer = AudioAnalyzer()
results = analyzer.analyze_full_spectrum('machine_recording.wav', mode='infrasound')

for event in results['events']:
    if event['magnitude_db'] > -30:  # High intensity
        print(f"ALERT: High intensity infrasound at {event['frequency_hz']:.2f} Hz")
```

### 3. Environmental Monitoring
Detect seismic or atmospheric events:

```bash
# Continuous monitoring for 24 hours
python src/realtime_monitor.py --duration 86400 --mode infrasound
```

---

## Configuration

Edit `config/config.yaml` to customize:

### Sample Rate
```yaml
audio:
  sample_rate: 96000  # Increase for higher ultrasound detection
```

### Detection Thresholds
```yaml
detection:
  infrasound:
    threshold_db: -40  # Lower = more sensitive
  ultrasound:
    threshold_db: -50  # Lower = more sensitive
```

### Frequency Ranges
```yaml
frequency_ranges:
  ultrasound:
    min: 20000
    max: 48000  # Limited by sample_rate/2
```

---

## Hardware Recommendations

### For Ultrasound Detection (>20kHz)
- **Budget**: MEMS microphones (e.g., ICS-43434)
- **Mid-range**: Pettersson M500 ($500-800)
- **Professional**: Wildlife Acoustics Echo Meter ($1500+)
- **Audio Interface**: Focusrite Scarlett 2i2 (192kHz capable)

### For Infrasound Detection (<20Hz)
- **Budget**: Large diaphragm condenser mic with high-pass filter disabled
- **Professional**: Seismometer or dedicated infrasound sensor
- **Audio Interface**: RME Babyface Pro (192kHz, high dynamic range)

---

## Troubleshooting

### Problem: No ultrasound detected
**Solution**: 
1. Verify microphone supports >20kHz
2. Check sample rate: `audio.sample_rate` must be at least 2x target frequency
3. Test with synthetic signal: `python src/analyzer.py`

### Problem: Too many false detections
**Solution**:
1. Increase detection threshold in `config/config.yaml`
2. Use bandpass filtering more aggressively
3. Enable ML-based detection (requires training)

### Problem: PyAudio installation fails
**Solution** (Windows):
1. Download PyAudio wheel from [Unofficial Windows Binaries](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Install: `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`

### Problem: "Sample rate not supported"
**Solution**:
1. Check audio interface specifications
2. Try lower sample rates: 48000 or 96000 Hz
3. Update audio drivers

---

## Next Steps

1. **Explore Examples**: Check `notebooks/analysis_demo.ipynb` for interactive examples
2. **Customize Detection**: Modify `config/config.yaml` for your use case
3. **Train ML Models**: See `src/ml_detector.py` for pattern recognition
4. **Integrate Vision**: Add computer vision for multi-modal analysis

---

## Additional Resources

- **Documentation**: See `README.md` for full documentation
- **Configuration Reference**: All options in `config/config.yaml`
- **API Reference**: Docstrings in source files
- **Example Scripts**: Check `examples/` directory

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review existing issues on GitHub
3. Open a new issue with:
   - Your hardware setup
   - Python version
   - Error messages
   - Sample code to reproduce

---

## Performance Tips

1. **Real-time Processing**: Use smaller buffer sizes for lower latency
2. **Batch Processing**: Use larger FFT sizes for better frequency resolution
3. **Memory**: Process long files in chunks to avoid memory issues
4. **CPU**: Enable multi-threading in configuration for faster processing

---

Happy analyzing! You're now ready to detect sounds beyond human perception. 🎵🦇📡
