"""
Advanced SciPy Vision Analysis
Uses SciPy for advanced signal processing on images/videos
"""

import numpy as np
import cv2
from scipy import signal, ndimage, fft
from scipy.stats import entropy
from typing import Dict, Tuple
import logging


class ScipyVisionAnalyzer:
    """Advanced vision analysis using SciPy signal processing."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def frequency_domain_analysis(self, image: np.ndarray) -> Dict:
        """2D FFT analysis to detect invisible patterns."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # 2D FFT
        f_transform = fft.fft2(gray)
        f_shift = fft.fftshift(f_transform)
        magnitude = np.abs(f_shift)
        phase = np.angle(f_shift)
        
        # Power spectrum
        power_spectrum = magnitude ** 2
        
        # Detect dominant frequencies
        threshold = np.percentile(magnitude, 99)
        peaks = magnitude > threshold
        
        return {
            'dominant_frequencies': int(np.sum(peaks)),
            'max_magnitude': float(np.max(magnitude)),
            'spectral_entropy': float(entropy(magnitude.flatten())),
            'power_spectrum_mean': float(np.mean(power_spectrum))
        }
    
    def wavelet_decomposition(self, image: np.ndarray, levels: int = 3) -> Dict:
        """Wavelet decomposition for multi-scale analysis."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Simulate wavelet decomposition using Gaussian pyramids
        pyramid = [gray]
        for i in range(levels):
            pyramid.append(cv2.pyrDown(pyramid[-1]))
        
        # Calculate energy at each level
        energies = [float(np.sum(level**2)) for level in pyramid]
        
        return {
            'levels': levels,
            'energies': energies,
            'total_energy': float(sum(energies)),
            'detail_ratio': float(energies[0] / sum(energies)) if sum(energies) > 0 else 0
        }
    
    def edge_detection_advanced(self, image: np.ndarray) -> Dict:
        """Advanced edge detection using multiple operators."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Sobel operators
        sobel_x = ndimage.sobel(gray, axis=1)
        sobel_y = ndimage.sobel(gray, axis=0)
        sobel_magnitude = np.hypot(sobel_x, sobel_y)
        
        # Prewitt operators
        prewitt_x = ndimage.prewitt(gray, axis=1)
        prewitt_y = ndimage.prewitt(gray, axis=0)
        prewitt_magnitude = np.hypot(prewitt_x, prewitt_y)
        
        # Laplacian
        laplacian = ndimage.laplace(gray)
        
        return {
            'sobel_mean': float(np.mean(sobel_magnitude)),
            'sobel_max': float(np.max(sobel_magnitude)),
            'prewitt_mean': float(np.mean(prewitt_magnitude)),
            'laplacian_variance': float(np.var(laplacian)),
            'edge_density': float(np.sum(sobel_magnitude > 50) / sobel_magnitude.size)
        }
    
    def texture_analysis(self, image: np.ndarray) -> Dict:
        """Texture analysis using statistical methods."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Local variance (texture measure)
        local_var = ndimage.generic_filter(gray, np.var, size=5)
        
        # Entropy (randomness measure)
        local_entropy = ndimage.generic_filter(gray, entropy, size=5)
        
        # Gradient magnitude
        gradient = ndimage.gaussian_gradient_magnitude(gray, sigma=2)
        
        return {
            'mean_variance': float(np.mean(local_var)),
            'mean_entropy': float(np.mean(local_entropy)),
            'texture_complexity': float(np.std(local_var)),
            'gradient_strength': float(np.mean(gradient))
        }
    
    def morphological_analysis(self, image: np.ndarray) -> Dict:
        """Morphological operations for structure detection."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Binary threshold
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Morphological operations
        kernel = np.ones((5, 5), np.uint8)
        eroded = ndimage.binary_erosion(binary, structure=kernel)
        dilated = ndimage.binary_dilation(binary, structure=kernel)
        opened = ndimage.binary_opening(binary, structure=kernel)
        closed = ndimage.binary_closing(binary, structure=kernel)
        
        return {
            'original_white_pixels': int(np.sum(binary > 0)),
            'eroded_white_pixels': int(np.sum(eroded)),
            'dilated_white_pixels': int(np.sum(dilated)),
            'structure_complexity': float(np.sum(opened) / np.sum(binary)) if np.sum(binary) > 0 else 0
        }
    
    def correlation_analysis(self, image: np.ndarray) -> Dict:
        """Auto-correlation to detect periodic structures."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Normalize
        normalized = (gray - np.mean(gray)) / np.std(gray)
        
        # Auto-correlation using FFT
        f_transform = fft.fft2(normalized)
        power_spectrum = np.abs(f_transform) ** 2
        autocorr = fft.ifft2(power_spectrum).real
        autocorr = fft.fftshift(autocorr)
        
        # Find peaks in autocorrelation
        center = np.array(autocorr.shape) // 2
        autocorr[center[0]-5:center[0]+5, center[1]-5:center[1]+5] = 0  # Remove center peak
        
        return {
            'max_correlation': float(np.max(autocorr)),
            'periodicity_score': float(np.std(autocorr)),
            'has_periodic_structure': bool(np.max(autocorr) > 0.3)
        }
    
    def spectral_filtering(self, image: np.ndarray, filter_type: str = 'highpass') -> np.ndarray:
        """Apply spectral filters to reveal hidden features."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # FFT
        f_transform = fft.fft2(gray)
        f_shift = fft.fftshift(f_transform)
        
        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2
        
        # Create filter mask
        mask = np.ones((rows, cols), np.uint8)
        r = 30
        
        if filter_type == 'highpass':
            # High-pass filter (remove low frequencies)
            mask[crow-r:crow+r, ccol-r:ccol+r] = 0
        elif filter_type == 'lowpass':
            # Low-pass filter (remove high frequencies)
            mask = np.zeros((rows, cols), np.uint8)
            mask[crow-r:crow+r, ccol-r:ccol+r] = 1
        
        # Apply filter
        f_shift_filtered = f_shift * mask
        
        # Inverse FFT
        f_ishift = fft.ifftshift(f_shift_filtered)
        img_filtered = fft.ifft2(f_ishift)
        img_filtered = np.abs(img_filtered)
        
        return img_filtered.astype(np.uint8)
    
    def phase_correlation(self, image1: np.ndarray, image2: np.ndarray) -> Dict:
        """Phase correlation for motion detection between frames."""
        if len(image1.shape) == 3:
            gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        else:
            gray1 = image1
            
        if len(image2.shape) == 3:
            gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        else:
            gray2 = image2
        
        # FFT of both images
        f1 = fft.fft2(gray1)
        f2 = fft.fft2(gray2)
        
        # Cross-power spectrum
        cross_power = (f1 * np.conj(f2)) / (np.abs(f1 * np.conj(f2)) + 1e-10)
        
        # Inverse FFT
        correlation = fft.ifft2(cross_power).real
        
        # Find peak
        y, x = np.unravel_index(np.argmax(correlation), correlation.shape)
        
        return {
            'shift_x': int(x),
            'shift_y': int(y),
            'correlation_peak': float(np.max(correlation)),
            'motion_detected': bool(np.max(correlation) > 0.5)
        }
    
    def comprehensive_analysis(self, image: np.ndarray) -> Dict:
        """Run all SciPy-based analyses."""
        return {
            'frequency_domain': self.frequency_domain_analysis(image),
            'wavelet': self.wavelet_decomposition(image),
            'edges': self.edge_detection_advanced(image),
            'texture': self.texture_analysis(image),
            'morphology': self.morphological_analysis(image),
            'correlation': self.correlation_analysis(image)
        }


if __name__ == "__main__":
    analyzer = ScipyVisionAnalyzer()
    print("SciPy Vision Analyzer initialized")
    print("Capabilities:")
    print("  - 2D FFT frequency analysis")
    print("  - Wavelet decomposition")
    print("  - Advanced edge detection")
    print("  - Texture analysis")
    print("  - Morphological operations")
    print("  - Auto-correlation")
    print("  - Spectral filtering")
    print("  - Phase correlation")
