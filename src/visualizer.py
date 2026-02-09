"""
Visualization Tools
Functions for plotting spectrograms and waveforms
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_spectrogram(frequencies: np.ndarray, times: np.ndarray, 
                    spectrogram: np.ndarray, title: str = "Spectrogram"):
    """Plot spectrogram."""
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(times, frequencies, spectrogram, shading='gouraud', cmap='viridis')
    plt.colorbar(label='Magnitude (dB)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title(title)
    plt.tight_layout()
    return plt.gcf()


def plot_waveform(audio: np.ndarray, sample_rate: int, title: str = "Waveform"):
    """Plot audio waveform."""
    plt.figure(figsize=(12, 4))
    time = np.arange(len(audio)) / sample_rate
    plt.plot(time, audio, linewidth=0.5)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt.gcf()
