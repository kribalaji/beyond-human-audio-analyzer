"""
Signal Processing Utilities
DSP functions for audio analysis
"""

import numpy as np
from scipy import signal
from typing import Tuple


def bandpass_filter(audio: np.ndarray, lowcut: float, highcut: float, 
                   sample_rate: int, order: int = 5) -> np.ndarray:
    """Apply bandpass filter."""
    nyquist = sample_rate / 2
    low = lowcut / nyquist
    high = highcut / nyquist
    low = max(0.0001, min(low, 0.9999))
    high = max(low + 0.0001, min(high, 0.9999))
    sos = signal.butter(order, [low, high], btype='band', output='sos')
    return signal.sosfilt(sos, audio)


def compute_stft(audio: np.ndarray, sample_rate: int, 
                fft_size: int = 2048, hop_length: int = 512) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute Short-Time Fourier Transform."""
    f, t, Zxx = signal.stft(audio, sample_rate, nperseg=fft_size, noverlap=fft_size-hop_length)
    return f, t, np.abs(Zxx)
