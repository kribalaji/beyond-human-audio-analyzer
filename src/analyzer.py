"""
Main Audio Analyzer for Beyond Human Perception Detection
Handles infrasound (<20Hz) and ultrasound (>20kHz) analysis
"""

import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from pathlib import Path
import yaml
import logging
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class AudioAnalyzer:
    """
    Comprehensive audio analyzer for detecting sounds beyond human hearing range.
    """
    
    def __init__(self, config_path: str = 'config/config.yaml'):
        """
        Initialize the analyzer with configuration.
        
        Args:
            config_path: Path to configuration YAML file
        """
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        self.sample_rate = self.config['audio']['sample_rate']
        self.results = []
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Return default configuration."""
        return {
            'audio': {'sample_rate': 96000, 'channels': 1},
            'frequency_ranges': {
                'infrasound': {'min': 0.01, 'max': 20},
                'ultrasound': {'min': 20000, 'max': 48000}
            },
            'detection': {
                'infrasound': {'threshold_db': -40, 'min_duration': 0.5},
                'ultrasound': {'threshold_db': -50, 'min_duration': 0.05}
            },
            'signal_processing': {
                'fft_size': 4096,
                'hop_length': 1024,
                'window': 'hann'
            }
        }
    
    def load_audio(self, file_path: str, target_sr: Optional[int] = None) -> Tuple[np.ndarray, int]:
        """
        Load audio file and resample if necessary.
        
        Args:
            file_path: Path to audio file
            target_sr: Target sample rate (uses config if None)
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        if target_sr is None:
            target_sr = self.sample_rate
            
        try:
            audio, sr = librosa.load(file_path, sr=target_sr, mono=True)
            self.logger.info(f"Loaded audio: {file_path} (duration: {len(audio)/sr:.2f}s)")
            return audio, sr
        except Exception as e:
            self.logger.error(f"Error loading audio file: {e}")
            raise
    
    def preprocess(self, audio: np.ndarray) -> np.ndarray:
        """
        Preprocess audio signal.
        
        Args:
            audio: Input audio array
            
        Returns:
            Preprocessed audio array
        """
        # Remove DC offset
        audio = audio - np.mean(audio)
        
        # Normalize
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio))
        
        return audio
    
    def apply_bandpass_filter(self, audio: np.ndarray, lowcut: float, 
                             highcut: float, order: int = 5) -> np.ndarray:
        """
        Apply bandpass filter to isolate frequency range.
        
        Args:
            audio: Input audio
            lowcut: Low frequency cutoff (Hz)
            highcut: High frequency cutoff (Hz)
            order: Filter order
            
        Returns:
            Filtered audio
        """
        nyquist = self.sample_rate / 2
        low = lowcut / nyquist
        high = highcut / nyquist
        
        # Ensure frequencies are valid
        low = max(0.0001, min(low, 0.9999))
        high = max(low + 0.0001, min(high, 0.9999))
        
        sos = signal.butter(order, [low, high], btype='band', output='sos')
        filtered = signal.sosfilt(sos, audio)
        
        return filtered
    
    def compute_fft(self, audio: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute FFT of audio signal.
        
        Args:
            audio: Input audio
            
        Returns:
            Tuple of (frequencies, magnitudes in dB)
        """
        N = len(audio)
        fft_vals = fft(audio)
        fft_freq = fftfreq(N, 1/self.sample_rate)
        
        # Take positive frequencies only
        positive_freq_idx = fft_freq > 0
        frequencies = fft_freq[positive_freq_idx]
        magnitudes = np.abs(fft_vals[positive_freq_idx])
        
        # Convert to dB
        magnitudes_db = 20 * np.log10(magnitudes + 1e-10)
        
        return frequencies, magnitudes_db
    
    def compute_spectrogram(self, audio: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute spectrogram using STFT.
        
        Args:
            audio: Input audio
            
        Returns:
            Tuple of (frequencies, times, spectrogram)
        """
        fft_size = self.config['signal_processing']['fft_size']
        hop_length = self.config['signal_processing']['hop_length']
        
        stft = librosa.stft(audio, n_fft=fft_size, hop_length=hop_length)
        spectrogram_db = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
        
        frequencies = librosa.fft_frequencies(sr=self.sample_rate, n_fft=fft_size)
        times = librosa.frames_to_time(np.arange(spectrogram_db.shape[1]), 
                                        sr=self.sample_rate, 
                                        hop_length=hop_length)
        
        return frequencies, times, spectrogram_db
    
    def detect_infrasound(self, audio: np.ndarray, 
                         file_name: str = "unknown") -> List[Dict]:
        """
        Detect infrasound events (<20Hz).
        
        Args:
            audio: Input audio
            file_name: Name of source file
            
        Returns:
            List of detected events
        """
        freq_config = self.config['frequency_ranges']['infrasound']
        det_config = self.config['detection']['infrasound']
        
        # Filter for infrasound range
        filtered = self.apply_bandpass_filter(
            audio, 
            freq_config['min'], 
            freq_config['max']
        )
        
        # Compute spectrum
        frequencies, magnitudes_db = self.compute_fft(filtered)
        
        # Find peaks above threshold
        threshold = det_config['threshold_db']
        infrasound_mask = frequencies < freq_config['max']
        
        peaks, properties = signal.find_peaks(
            magnitudes_db[infrasound_mask],
            height=threshold,
            distance=int(self.sample_rate * det_config['min_duration'])
        )
        
        events = []
        for i, peak_idx in enumerate(peaks):
            event = {
                'type': 'infrasound',
                'frequency_hz': frequencies[infrasound_mask][peak_idx],
                'magnitude_db': properties['peak_heights'][i],
                'file': file_name,
                'timestamp': None  # Would need time-series analysis for accurate timing
            }
            events.append(event)
            self.logger.info(f"Infrasound detected: {event['frequency_hz']:.2f} Hz at {event['magnitude_db']:.1f} dB")
        
        return events
    
    def detect_ultrasound(self, audio: np.ndarray, 
                         file_name: str = "unknown") -> List[Dict]:
        """
        Detect ultrasound events (>20kHz).
        
        Args:
            audio: Input audio
            file_name: Name of source file
            
        Returns:
            List of detected events
        """
        freq_config = self.config['frequency_ranges']['ultrasound']
        det_config = self.config['detection']['ultrasound']
        
        # Filter for ultrasound range
        filtered = self.apply_bandpass_filter(
            audio, 
            freq_config['min'], 
            min(freq_config['max'], self.sample_rate / 2 - 1000)
        )
        
        # Compute spectrum
        frequencies, magnitudes_db = self.compute_fft(filtered)
        
        # Find peaks above threshold
        threshold = det_config['threshold_db']
        ultrasound_mask = (frequencies >= freq_config['min']) & (frequencies <= freq_config['max'])
        
        peaks, properties = signal.find_peaks(
            magnitudes_db[ultrasound_mask],
            height=threshold,
            distance=int(self.sample_rate * det_config['min_duration'])
        )
        
        events = []
        for i, peak_idx in enumerate(peaks):
            event = {
                'type': 'ultrasound',
                'frequency_hz': frequencies[ultrasound_mask][peak_idx],
                'magnitude_db': properties['peak_heights'][i],
                'file': file_name,
                'timestamp': None
            }
            events.append(event)
            self.logger.info(f"Ultrasound detected: {event['frequency_hz']:.2f} Hz at {event['magnitude_db']:.1f} dB")
        
        return events
    
    def analyze_full_spectrum(self, file_path: str, mode: str = 'full') -> Dict:
        """
        Perform complete analysis on audio file.
        
        Args:
            file_path: Path to audio file
            mode: Analysis mode ('infrasound', 'ultrasound', or 'full')
            
        Returns:
            Dictionary with analysis results
        """
        # Load audio
        audio, sr = self.load_audio(file_path)
        
        # Preprocess
        audio = self.preprocess(audio)
        
        results = {
            'file': Path(file_path).name,
            'duration_seconds': len(audio) / sr,
            'sample_rate': sr,
            'events': []
        }
        
        # Detect based on mode
        if mode in ['infrasound', 'full']:
            infrasound_events = self.detect_infrasound(audio, Path(file_path).name)
            results['events'].extend(infrasound_events)
        
        if mode in ['ultrasound', 'full']:
            ultrasound_events = self.detect_ultrasound(audio, Path(file_path).name)
            results['events'].extend(ultrasound_events)
        
        results['total_events'] = len(results['events'])
        
        return results
    
    def visualize_spectrum(self, audio: np.ndarray, 
                          title: str = "Frequency Spectrum",
                          freq_range: Optional[Tuple[float, float]] = None,
                          save_path: Optional[str] = None):
        """
        Visualize frequency spectrum.
        
        Args:
            audio: Input audio
            title: Plot title
            freq_range: Tuple of (min_freq, max_freq) to display
            save_path: Path to save figure
        """
        frequencies, magnitudes_db = self.compute_fft(audio)
        
        plt.figure(figsize=(12, 6))
        plt.plot(frequencies, magnitudes_db, linewidth=0.5)
        
        if freq_range:
            plt.xlim(freq_range)
            mask = (frequencies >= freq_range[0]) & (frequencies <= freq_range[1])
            plt.ylim([magnitudes_db[mask].min() - 10, magnitudes_db[mask].max() + 10])
        
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude (dB)')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            self.logger.info(f"Saved spectrum plot to {save_path}")
        
        plt.show()
    
    def visualize_spectrogram(self, audio: np.ndarray,
                            title: str = "Spectrogram",
                            freq_range: Optional[Tuple[float, float]] = None,
                            save_path: Optional[str] = None):
        """
        Visualize spectrogram.
        
        Args:
            audio: Input audio
            title: Plot title
            freq_range: Tuple of (min_freq, max_freq) to display
            save_path: Path to save figure
        """
        frequencies, times, spectrogram_db = self.compute_spectrogram(audio)
        
        plt.figure(figsize=(14, 8))
        plt.pcolormesh(times, frequencies, spectrogram_db, 
                      shading='gouraud', cmap='viridis')
        
        if freq_range:
            plt.ylim(freq_range)
        
        plt.colorbar(label='Magnitude (dB)')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title(title)
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            self.logger.info(f"Saved spectrogram to {save_path}")
        
        plt.show()


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO, 
                       format='%(asctime)s - %(levelname)s - %(message)s')
    
    analyzer = AudioAnalyzer()
    
    print("Beyond Human Perception Audio Analyzer")
    print("=" * 50)
    print(f"Sample Rate: {analyzer.sample_rate} Hz")
    print(f"Maximum Detectable Frequency: {analyzer.sample_rate / 2} Hz")
    print("=" * 50)
    
    # Example: Generate synthetic test signals
    print("\nGenerating test signals...")
    
    duration = 5  # seconds
    t = np.linspace(0, duration, int(analyzer.sample_rate * duration))
    
    # Infrasound signal (5 Hz)
    infrasound_signal = 0.5 * np.sin(2 * np.pi * 5 * t)
    
    # Ultrasound signal (25 kHz)
    ultrasound_signal = 0.3 * np.sin(2 * np.pi * 25000 * t)
    
    # Combined signal
    combined_signal = infrasound_signal + ultrasound_signal + 0.05 * np.random.randn(len(t))
    
    # Save test signal
    test_dir = Path('data/samples')
    test_dir.mkdir(parents=True, exist_ok=True)
    test_file = test_dir / 'test_signal.wav'
    sf.write(str(test_file), combined_signal, analyzer.sample_rate)
    print(f"Saved test signal to {test_file}")
    
    # Analyze
    print("\nAnalyzing test signal...")
    results = analyzer.analyze_full_spectrum(str(test_file), mode='full')
    
    print(f"\nAnalysis Results:")
    print(f"Duration: {results['duration_seconds']:.2f} seconds")
    print(f"Total events detected: {results['total_events']}")
    
    for event in results['events']:
        print(f"  - {event['type'].upper()}: {event['frequency_hz']:.2f} Hz @ {event['magnitude_db']:.1f} dB")
