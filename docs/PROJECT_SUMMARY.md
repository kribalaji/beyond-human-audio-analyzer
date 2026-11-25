# Beyond Human Perception Audio Analyzer
## Project Summary & Technical Overview

### Executive Summary

This is a comprehensive Python-based audio analysis system designed to detect and analyze sounds beyond human hearing capabilities. The system focuses on two primary frequency ranges:
- **Infrasound**: < 20 Hz (earthquakes, weather, machinery)
- **Ultrasound**: > 20 kHz (bats, rodents, electronic devices)

---

## Key Features

### 1. Core Analysis Capabilities
- Real-time audio monitoring with configurable sample rates up to 192 kHz
- FFT-based frequency spectrum analysis
- Spectrogram generation with STFT (Short-Time Fourier Transform)
- Bandpass filtering for frequency range isolation
- Peak detection with configurable thresholds
- Signal-to-Noise Ratio (SNR) calculation
- Total Harmonic Distortion (THD) measurement

### 2. Detection Modes
- **Infrasound Mode**: Specialized for <20 Hz detection
- **Ultrasound Mode**: Specialized for >20 kHz detection
- **Full Spectrum Mode**: Simultaneous detection across all ranges

### 3. Processing Options
- Single file analysis
- Batch processing for multiple files
- Real-time monitoring with callback system
- Event-triggered recording

### 4. Output Formats
- JSON reports with detailed event data
- CSV exports for spreadsheet analysis
- Text summary reports
- High-quality visualizations (spectrograms, waveforms)
- Audio file exports of detected events

---

## Technical Architecture

### Project Structure
```
beyond-human-audio-analyzer/
├── src/
│   ├── analyzer.py          # Core analysis engine (650+ lines)
│   ├── realtime_monitor.py  # Real-time monitoring (450+ lines)
│   ├── batch_processor.py   # Batch processing (400+ lines)
│   └── utils.py             # Utility functions (500+ lines)
├── config/
│   └── config.yaml          # Configuration settings
├── data/
│   ├── samples/             # Sample audio files
│   └── models/              # ML models (optional)
├── examples/
│   └── use_cases.py         # Practical examples (500+ lines)
├── requirements.txt         # Python dependencies
├── README.md                # Full documentation
├── GETTING_STARTED.md       # Quick start guide
└── test_installation.py     # Installation verification
```

### Core Components

#### 1. AudioAnalyzer (analyzer.py)
The main analysis engine with methods for:
- Audio loading and preprocessing
- FFT and spectrogram computation
- Bandpass filtering
- Event detection (infrasound/ultrasound)
- Visualization generation

**Key Methods:**
- `load_audio()`: Load and resample audio files
- `preprocess()`: DC removal and normalization
- `compute_fft()`: Fast Fourier Transform
- `detect_infrasound()`: Detect <20 Hz events
- `detect_ultrasound()`: Detect >20 kHz events
- `visualize_spectrum()`: Generate frequency plots
- `visualize_spectrogram()`: Generate time-frequency plots

#### 2. RealtimeMonitor (realtime_monitor.py)
Real-time audio stream processing with:
- Audio callback system
- Event queue management
- Custom callback registration
- Threading for non-blocking operation

**Key Methods:**
- `start()`: Begin monitoring
- `stop()`: Stop monitoring
- `register_callback()`: Add event handlers
- `list_audio_devices()`: Show available hardware

#### 3. BatchProcessor (batch_processor.py)
Bulk file processing with:
- Directory scanning
- Progress tracking
- Multi-format report generation
- Error handling and logging

**Key Methods:**
- `process_directory()`: Process all files in folder
- `process_file()`: Single file analysis
- `get_statistics()`: Summary statistics

#### 4. Utils (utils.py)
Helper functions including:
- Signal generation
- Audio format conversion
- dB/linear conversions
- SNR/THD calculations
- Noise gating
- Audio segmentation

---

## Technical Specifications

### Signal Processing

#### Sampling Requirements
- **Nyquist Theorem**: Sample rate must be ≥ 2× highest frequency
- **Infrasound**: 48 kHz sample rate sufficient
- **Ultrasound**: 96-192 kHz recommended
- **Bit Depth**: 24-bit for high dynamic range

#### FFT Parameters
- **Default FFT Size**: 4096 samples
- **Hop Length**: 1024 samples
- **Window Function**: Hann window (default)
- **Frequency Resolution**: sample_rate / fft_size Hz

#### Filtering
- **Type**: Butterworth bandpass filter
- **Order**: 5 (default, configurable)
- **Implementation**: SOS (Second-Order Sections) for stability

### Detection Algorithms

#### Peak Detection
```python
# Finds peaks in frequency spectrum above threshold
peaks, properties = signal.find_peaks(
    magnitudes_db,
    height=threshold_db,
    distance=min_duration * sample_rate
)
```

#### Threshold Settings
- **Infrasound**: -40 dB (default)
- **Ultrasound**: -50 dB (default)
- **Adjustable via config**: Lower = more sensitive

---

## Use Cases & Applications

### 1. Wildlife Monitoring
**Target Species:**
- Bats (20-100 kHz echolocation)
- Rodents (20-90 kHz vocalizations)
- Insects (various ultrasonic ranges)

**Applications:**
- Population surveys
- Species identification
- Behavioral studies
- Habitat assessment

### 2. Industrial & Machinery
**Detection:**
- Bearing wear (low-frequency vibrations)
- Motor imbalance (harmonic patterns)
- Pneumatic leaks (ultrasonic)
- Structural stress (infrasound)

**Applications:**
- Predictive maintenance
- Quality control
- Safety monitoring
- Energy efficiency

### 3. Environmental Monitoring
**Phenomena:**
- Seismic activity (infrasound)
- Atmospheric events (infrasound)
- Weather patterns (low frequencies)
- Human-made noise pollution

**Applications:**
- Earthquake early warning
- Storm tracking
- Aviation safety
- Urban planning

### 4. Building & Infrastructure
**Detection:**
- Structural resonances
- Plumbing leaks (ultrasonic)
- HVAC issues
- Electrical arcing (ultrasonic)

**Applications:**
- Building diagnostics
- Leak detection
- Energy audits
- Safety inspections

---

## Performance Characteristics

### Processing Speed
- **Real-time**: Capable at ≤96 kHz sample rate on modern hardware
- **Batch Processing**: ~1-2× real-time on average (varies with file size)
- **Memory Usage**: ~50-200 MB depending on buffer sizes

### Accuracy
- **Frequency Resolution**: ±(sample_rate / fft_size) Hz
- **Detection Range**: 0.01 Hz to (sample_rate/2) Hz
- **Dynamic Range**: 24-bit = 144 dB theoretical

### Limitations
- Hardware-dependent frequency limits
- Nyquist frequency = sample_rate / 2
- Cannot detect below microphone's frequency response
- Real-time processing latency depends on buffer size

---

## Hardware Requirements

### Minimum
- CPU: Dual-core 2.0+ GHz
- RAM: 4 GB
- Storage: 1 GB for software + data storage
- Audio: Any USB microphone

### Recommended (Professional Use)
- CPU: Quad-core 3.0+ GHz
- RAM: 8+ GB
- Storage: SSD with 50+ GB
- Audio Interface: 192 kHz capable (RME, Focusrite, MOTU)
- Microphone: Frequency-extended (e.g., Pettersson, Wildlife Acoustics)

### For Ultrasound
- Microphone with >40 kHz response
- Audio interface with 96-192 kHz support
- Low-noise preamp

### For Infrasound
- Large diaphragm or specialized sensor
- Seismometer for <1 Hz
- Vibration isolation recommended

---

## Software Dependencies

### Core Libraries
```
numpy (1.24+)       - Numerical computing
scipy (1.10+)       - Signal processing
librosa (0.10+)     - Audio analysis
soundfile (0.12+)   - Audio I/O
matplotlib (3.7+)   - Visualization
```

### Additional
```
PyAudio (0.2.13+)   - Real-time audio
PyYAML (6.0+)       - Configuration
pandas (2.0+)       - Data handling
scikit-learn (1.3+) - Machine learning (optional)
```

---

## Configuration Options

### Sample Rates
```yaml
audio:
  sample_rate: 96000  # 48000, 96000, 192000
```

### Detection Thresholds
```yaml
detection:
  infrasound:
    threshold_db: -40   # Lower = more sensitive
    min_duration: 0.5   # seconds
  ultrasound:
    threshold_db: -50
    min_duration: 0.05
```

### Signal Processing
```yaml
signal_processing:
  fft_size: 4096      # 1024, 2048, 4096, 8192
  hop_length: 1024
  window: 'hann'      # hann, hamming, blackman
```

---

## Future Enhancements

### Planned Features
1. **Machine Learning Integration**
   - Pattern recognition
   - Species classification
   - Anomaly detection
   - Transfer learning support

2. **Multi-channel Analysis**
   - Spatial localization
   - Beamforming
   - Noise cancellation

3. **Computer Vision Integration**
   - Synchronized video analysis
   - Multi-modal event correlation
   - Automated species identification

4. **Cloud Integration**
   - Remote monitoring
   - Data synchronization
   - Collaborative analysis

5. **Mobile Support**
   - iOS/Android apps
   - Field deployment
   - GPS integration

---

## Research Applications

### Academic Research
- Bioacoustics studies
- Environmental monitoring
- Material science
- Earthquake research

### Industry
- Predictive maintenance
- Quality assurance
- Non-destructive testing
- Energy sector monitoring

### Conservation
- Wildlife population studies
- Habitat assessment
- Impact evaluation
- Long-term monitoring

---

## Performance Optimization Tips

### For Real-time Processing
1. Use smaller buffer sizes (1024-2048)
2. Disable visualization during monitoring
3. Use efficient FFT sizes (powers of 2)
4. Consider GPU acceleration for ML models

### For Batch Processing
1. Use larger FFT sizes for better resolution
2. Process files in parallel
3. Use SSD for faster file I/O
4. Enable multi-threading

### For Long Recordings
1. Process in chunks
2. Use streaming processing
3. Implement intelligent storage (save only events)
4. Use compression for storage

---

## Troubleshooting Guide

### Common Issues

**Issue**: No events detected
- Check microphone frequency response
- Verify sample rate is sufficient
- Lower detection thresholds
- Test with synthetic signals

**Issue**: Too many false detections
- Increase threshold values
- Apply stricter filtering
- Check for environmental noise
- Use noise gate

**Issue**: Poor frequency resolution
- Increase FFT size
- Use longer analysis windows
- Check sample rate
- Verify audio quality

**Issue**: Real-time latency
- Decrease buffer size
- Optimize processing pipeline
- Use faster hardware
- Reduce FFT size

---

## Legal & Ethical Considerations

### Privacy
- Ultrasound can penetrate walls
- May capture unintended conversations
- Follow local recording laws
- Obtain necessary permissions

### Safety
- High-intensity ultrasound can affect animals
- Follow wildlife research ethics
- Minimize environmental impact
- Respect protected species

### Data
- Securely store recordings
- Follow data protection regulations
- Anonymize when possible
- Respect intellectual property

---

## Conclusion

The Beyond Human Perception Audio Analyzer provides a comprehensive, professional-grade solution for detecting and analyzing sounds outside human hearing range. With its flexible architecture, extensive configuration options, and robust processing capabilities, it serves researchers, engineers, and conservation professionals across multiple domains.

The system's modular design allows for easy extension and customization, while its performance optimizations ensure it can handle real-world deployment scenarios. Whether used for wildlife monitoring, industrial diagnostics, or environmental research, this tool provides the foundation for understanding the hidden acoustic world around us.

---

**Project Statistics:**
- Total Lines of Code: ~2,000+
- Documentation: ~1,500 lines
- Test Coverage: Core functions
- Platform Support: Windows, macOS, Linux
- License: MIT

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Maintained By**: [Your Organization]
