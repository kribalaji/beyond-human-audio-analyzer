# Beyond Human Perception Audio Analyzer

A comprehensive Python toolkit for analyzing and detecting sounds beyond human hearing range (infrasound <20Hz and ultrasound >20kHz), with optional visual analysis integration.

## Features

- **Infrasound Detection** (<20Hz): Detect earthquakes, weather patterns, industrial machinery
- **Ultrasound Detection** (>20kHz): Detect bat calls, rodent communication, electronic devices
- **Real-time Analysis**: Live audio stream processing
- **Spectral Analysis**: FFT-based frequency decomposition
- **Pattern Recognition**: ML-based anomaly detection
- **Visualization**: Spectrograms, waveforms, and frequency plots
- **Audio Recording**: Capture and save detected events
- **Export Capabilities**: CSV, JSON, and audio file exports

## Requirements

### Hardware
- **Microphone**: Must support extended frequency range
  - For ultrasound: 40kHz+ capable microphone
  - For infrasound: Low-frequency microphone or seismometer
- **Audio Interface**: High sample rate support (96kHz - 192kHz recommended)

### Software
- Python 3.8+
- See `requirements.txt` for dependencies

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd beyond-human-audio-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Basic Audio Analysis
```bash
python src/analyzer.py --input audio_sample.wav --mode full
```

### 2. Real-time Monitoring
```bash
python src/realtime_monitor.py --infrasound --ultrasound
```

### 3. Batch Processing
```bash
python src/batch_processor.py --input-dir ./audio_files --output-dir ./results
```

## Project Structure

```
beyond-human-audio-analyzer/
├── src/
│   ├── analyzer.py           # Main analysis engine
│   ├── realtime_monitor.py   # Real-time audio monitoring
│   ├── batch_processor.py    # Batch file processing
│   ├── signal_processing.py  # DSP utilities
│   ├── visualizer.py         # Visualization tools
│   ├── ml_detector.py        # Machine learning detection
│   └── utils.py              # Helper functions
├── config/
│   └── config.yaml           # Configuration settings
├── data/
│   ├── samples/              # Sample audio files
│   └── models/               # Trained ML models
├── tests/
│   └── test_*.py             # Unit tests
├── notebooks/
│   └── analysis_demo.ipynb   # Jupyter demo
├── requirements.txt
└── README.md
```

## Configuration

Edit `config/config.yaml` to customize:
- Frequency ranges
- Detection thresholds
- Sample rates
- Filter parameters
- Output formats

## Usage Examples

### Detect Infrasound Events
```python
from src.analyzer import AudioAnalyzer

analyzer = AudioAnalyzer(sample_rate=48000)
results = analyzer.detect_infrasound('recording.wav', threshold=-40)
print(f"Found {len(results)} infrasound events")
```

### Ultrasound Analysis
```python
analyzer = AudioAnalyzer(sample_rate=192000)
ultrasound_data = analyzer.detect_ultrasound('bat_recording.wav')
analyzer.visualize_spectrogram(ultrasound_data, freq_range=(20000, 100000))
```

### Real-time Monitoring
```python
from src.realtime_monitor import RealtimeMonitor

monitor = RealtimeMonitor(sample_rate=96000)
monitor.start(
    callback=lambda event: print(f"Detected: {event['type']} at {event['frequency']}Hz"),
    duration=60  # Monitor for 60 seconds
)
```

## Technical Details

### Signal Processing Pipeline
1. **Preprocessing**: DC offset removal, normalization
2. **Filtering**: Bandpass filters for target frequency ranges
3. **Analysis**: FFT, STFT, wavelet transforms
4. **Detection**: Threshold-based and ML-based detection
5. **Post-processing**: Event classification and characterization

### Frequency Ranges
- **Infrasound**: 0.01 Hz - 20 Hz
- **Human Audible**: 20 Hz - 20,000 Hz (for reference)
- **Ultrasound**: 20,000 Hz - 100,000 Hz (depending on hardware)

## Performance Considerations

- **Sample Rate**: Higher rates (192kHz) needed for ultrasound
- **Buffer Size**: Balance between latency and accuracy
- **CPU Usage**: Real-time processing can be intensive
- **Memory**: Large audio files require sufficient RAM

## Troubleshooting

### No ultrasound detected
- Verify microphone supports >20kHz
- Check sample rate is sufficient (2x highest frequency)
- Ensure audio interface supports high sample rates

### High false positive rate
- Adjust detection thresholds in config
- Apply stricter filters
- Use ML-based detection for better accuracy

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## License

MIT License - See LICENSE file for details

## Citation

If you use this project in research, please cite:
```
Beyond Human Perception Audio Analyzer (2026)
https://github.com/yourusername/beyond-human-audio-analyzer
```

## References

- Infrasound detection: https://www.iris.edu/hq/indiepub/infrasound
- Ultrasound analysis: https://www.batdetective.org/
- Signal processing: https://www.dspguide.com/

## Contact

For questions or support, please open an issue on GitHub.
