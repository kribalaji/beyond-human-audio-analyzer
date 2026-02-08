"""
Utility Functions for Audio Analysis
Helper functions for signal processing, file operations, and data export
"""

import numpy as np
from scipy import signal
import soundfile as sf
import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging


def db_to_linear(db_value: float) -> float:
    """
    Convert decibels to linear scale.
    
    Args:
        db_value: Value in decibels
        
    Returns:
        Linear scale value
    """
    return 10 ** (db_value / 20)


def linear_to_db(linear_value: float) -> float:
    """
    Convert linear scale to decibels.
    
    Args:
        linear_value: Linear scale value
        
    Returns:
        Value in decibels
    """
    return 20 * np.log10(max(linear_value, 1e-10))


def calculate_snr(signal_audio: np.ndarray, noise_audio: np.ndarray) -> float:
    """
    Calculate Signal-to-Noise Ratio.
    
    Args:
        signal_audio: Signal portion of audio
        noise_audio: Noise portion of audio
        
    Returns:
        SNR in dB
    """
    signal_power = np.mean(signal_audio ** 2)
    noise_power = np.mean(noise_audio ** 2)
    
    if noise_power == 0:
        return float('inf')
    
    snr = 10 * np.log10(signal_power / noise_power)
    return snr


def calculate_thd(audio: np.ndarray, sample_rate: int, 
                 fundamental_freq: float, num_harmonics: int = 5) -> float:
    """
    Calculate Total Harmonic Distortion.
    
    Args:
        audio: Input audio signal
        sample_rate: Sample rate in Hz
        fundamental_freq: Fundamental frequency in Hz
        num_harmonics: Number of harmonics to consider
        
    Returns:
        THD as percentage
    """
    # Compute FFT
    fft_vals = np.fft.fft(audio)
    fft_freq = np.fft.fftfreq(len(audio), 1/sample_rate)
    
    positive_freq_idx = fft_freq > 0
    frequencies = fft_freq[positive_freq_idx]
    magnitudes = np.abs(fft_vals[positive_freq_idx])
    
    # Find fundamental
    fund_idx = np.argmin(np.abs(frequencies - fundamental_freq))
    fundamental_magnitude = magnitudes[fund_idx]
    
    # Calculate harmonic magnitudes
    harmonic_power = 0
    for n in range(2, num_harmonics + 2):
        harmonic_freq = n * fundamental_freq
        harmonic_idx = np.argmin(np.abs(frequencies - harmonic_freq))
        harmonic_power += magnitudes[harmonic_idx] ** 2
    
    # Calculate THD
    if fundamental_magnitude == 0:
        return 0
    
    thd = np.sqrt(harmonic_power) / fundamental_magnitude * 100
    return thd


def resample_audio(audio: np.ndarray, orig_sr: int, 
                  target_sr: int) -> np.ndarray:
    """
    Resample audio to different sample rate.
    
    Args:
        audio: Input audio
        orig_sr: Original sample rate
        target_sr: Target sample rate
        
    Returns:
        Resampled audio
    """
    if orig_sr == target_sr:
        return audio
    
    # Calculate resampling ratio
    ratio = target_sr / orig_sr
    
    # Use scipy's resample
    num_samples = int(len(audio) * ratio)
    resampled = signal.resample(audio, num_samples)
    
    return resampled


def apply_window(audio: np.ndarray, window_type: str = 'hann') -> np.ndarray:
    """
    Apply window function to audio.
    
    Args:
        audio: Input audio
        window_type: Type of window ('hann', 'hamming', 'blackman', etc.)
        
    Returns:
        Windowed audio
    """
    window = signal.get_window(window_type, len(audio))
    return audio * window


def normalize_audio(audio: np.ndarray, target_db: float = -20) -> np.ndarray:
    """
    Normalize audio to target dB level.
    
    Args:
        audio: Input audio
        target_db: Target peak level in dB
        
    Returns:
        Normalized audio
    """
    # Calculate current peak
    peak = np.max(np.abs(audio))
    
    if peak == 0:
        return audio
    
    # Current level in dB
    current_db = linear_to_db(peak)
    
    # Calculate gain needed
    gain_db = target_db - current_db
    gain_linear = db_to_linear(gain_db)
    
    # Apply gain
    normalized = audio * gain_linear
    
    return normalized


def save_audio(audio: np.ndarray, sample_rate: int, 
              file_path: str, bit_depth: int = 24):
    """
    Save audio to file.
    
    Args:
        audio: Audio data
        sample_rate: Sample rate in Hz
        file_path: Output file path
        bit_depth: Bit depth (16 or 24)
    """
    # Determine subtype based on bit depth
    subtype_map = {
        16: 'PCM_16',
        24: 'PCM_24',
        32: 'PCM_32'
    }
    subtype = subtype_map.get(bit_depth, 'PCM_24')
    
    # Ensure audio is in valid range
    audio = np.clip(audio, -1.0, 1.0)
    
    sf.write(file_path, audio, sample_rate, subtype=subtype)


def export_events_to_json(events: List[Dict], output_file: str):
    """
    Export detected events to JSON file.
    
    Args:
        events: List of event dictionaries
        output_file: Output JSON file path
    """
    with open(output_file, 'w') as f:
        json.dump(events, f, indent=2, default=str)


def export_events_to_csv(events: List[Dict], output_file: str):
    """
    Export detected events to CSV file.
    
    Args:
        events: List of event dictionaries
        output_file: Output CSV file path
    """
    if not events:
        return
    
    # Get all unique keys from events
    fieldnames = set()
    for event in events:
        fieldnames.update(event.keys())
    
    fieldnames = sorted(fieldnames)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(events)


def create_frequency_bins(min_freq: float, max_freq: float, 
                         num_bins: int) -> np.ndarray:
    """
    Create logarithmically spaced frequency bins.
    
    Args:
        min_freq: Minimum frequency in Hz
        max_freq: Maximum frequency in Hz
        num_bins: Number of bins
        
    Returns:
        Array of frequency bin edges
    """
    return np.logspace(np.log10(min_freq), np.log10(max_freq), num_bins + 1)


def extract_audio_segment(audio: np.ndarray, sample_rate: int,
                         start_time: float, end_time: float) -> np.ndarray:
    """
    Extract segment of audio between start and end times.
    
    Args:
        audio: Input audio
        sample_rate: Sample rate in Hz
        start_time: Start time in seconds
        end_time: End time in seconds
        
    Returns:
        Audio segment
    """
    start_sample = int(start_time * sample_rate)
    end_sample = int(end_time * sample_rate)
    
    # Ensure indices are valid
    start_sample = max(0, start_sample)
    end_sample = min(len(audio), end_sample)
    
    return audio[start_sample:end_sample]


def calculate_zero_crossing_rate(audio: np.ndarray, 
                                frame_length: int = 2048,
                                hop_length: int = 512) -> np.ndarray:
    """
    Calculate zero-crossing rate of audio signal.
    
    Args:
        audio: Input audio
        frame_length: Length of analysis frame
        hop_length: Hop size between frames
        
    Returns:
        Array of zero-crossing rates per frame
    """
    zcr = []
    
    for i in range(0, len(audio) - frame_length, hop_length):
        frame = audio[i:i + frame_length]
        
        # Count zero crossings
        zero_crossings = np.sum(np.abs(np.diff(np.sign(frame)))) / 2
        
        # Normalize by frame length
        zcr.append(zero_crossings / frame_length)
    
    return np.array(zcr)


def apply_noise_gate(audio: np.ndarray, threshold_db: float = -40,
                    attack_samples: int = 10, 
                    release_samples: int = 100) -> np.ndarray:
    """
    Apply noise gate to suppress low-level noise.
    
    Args:
        audio: Input audio
        threshold_db: Gate threshold in dB
        attack_samples: Attack time in samples
        release_samples: Release time in samples
        
    Returns:
        Gated audio
    """
    threshold_linear = db_to_linear(threshold_db)
    
    # Calculate envelope
    envelope = np.abs(audio)
    
    # Create gate control signal
    gate = np.zeros_like(audio)
    gate_state = 0
    
    for i in range(len(audio)):
        if envelope[i] > threshold_linear:
            # Attack
            gate_state = min(1.0, gate_state + 1.0 / attack_samples)
        else:
            # Release
            gate_state = max(0.0, gate_state - 1.0 / release_samples)
        
        gate[i] = gate_state
    
    # Apply gate
    gated = audio * gate
    
    return gated


def generate_test_signal(frequency: float, duration: float, 
                        sample_rate: int, amplitude: float = 0.5) -> np.ndarray:
    """
    Generate test sinusoidal signal.
    
    Args:
        frequency: Frequency in Hz
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
        amplitude: Signal amplitude (0 to 1)
        
    Returns:
        Test signal array
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    signal_audio = amplitude * np.sin(2 * np.pi * frequency * t)
    
    return signal_audio


def estimate_frequency_content(audio: np.ndarray, sample_rate: int,
                              frequency_ranges: Dict[str, Tuple[float, float]]) -> Dict[str, float]:
    """
    Estimate energy content in different frequency ranges.
    
    Args:
        audio: Input audio
        sample_rate: Sample rate in Hz
        frequency_ranges: Dictionary of range names to (min, max) frequency tuples
        
    Returns:
        Dictionary of range names to energy percentages
    """
    # Compute FFT
    fft_vals = np.fft.fft(audio)
    fft_freq = np.fft.fftfreq(len(audio), 1/sample_rate)
    
    positive_freq_idx = fft_freq > 0
    frequencies = fft_freq[positive_freq_idx]
    magnitudes = np.abs(fft_vals[positive_freq_idx]) ** 2
    
    total_energy = np.sum(magnitudes)
    
    energy_distribution = {}
    
    for range_name, (min_freq, max_freq) in frequency_ranges.items():
        mask = (frequencies >= min_freq) & (frequencies <= max_freq)
        range_energy = np.sum(magnitudes[mask])
        
        if total_energy > 0:
            percentage = (range_energy / total_energy) * 100
        else:
            percentage = 0
        
        energy_distribution[range_name] = percentage
    
    return energy_distribution


def setup_logger(name: str, log_file: Optional[str] = None, 
                level: int = logging.INFO) -> logging.Logger:
    """
    Setup logger with file and console handlers.
    
    Args:
        name: Logger name
        log_file: Optional log file path
        level: Logging level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


if __name__ == "__main__":
    # Test utility functions
    print("Testing utility functions...")
    
    # Test signal generation
    test_signal = generate_test_signal(440, 1.0, 48000)
    print(f"Generated test signal: {len(test_signal)} samples")
    
    # Test dB conversion
    db_val = linear_to_db(0.5)
    linear_val = db_to_linear(db_val)
    print(f"dB conversion: 0.5 -> {db_val:.2f} dB -> {linear_val:.4f}")
    
    # Test frequency content estimation
    ranges = {
        'infrasound': (0, 20),
        'audible': (20, 20000),
        'ultrasound': (20000, 24000)
    }
    distribution = estimate_frequency_content(test_signal, 48000, ranges)
    print(f"Frequency distribution: {distribution}")
    
    print("All tests completed successfully!")
