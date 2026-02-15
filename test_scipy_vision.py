"""Quick SciPy Vision Test"""
import sys
from pathlib import Path
import cv2
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))

from src.scipy_vision_analyzer import ScipyVisionAnalyzer

print("\n" + "="*70)
print("SCIPY VISION - QUICK TEST")
print("="*70)

analyzer = ScipyVisionAnalyzer()

# Create simple test image
print("\n1. Creating test image...")
test_img = np.zeros((200, 200), dtype=np.uint8)
cv2.circle(test_img, (100, 100), 50, 255, -1)
print("   [OK] Test image created")

# Quick analysis
print("\n2. Running SciPy analysis...")
results = analyzer.comprehensive_analysis(test_img)

print("\n3. Results:")
print(f"   Frequency domain: {results['frequency_domain']['dominant_frequencies']} peaks")
print(f"   Wavelet levels: {results['wavelet']['levels']}")
print(f"   Edge density: {results['edges']['edge_density']:.3f}")
print(f"   Texture complexity: {results['texture']['texture_complexity']:.1f}")
print(f"   Periodic structure: {results['correlation']['has_periodic_structure']}")

# Spectral filter
print("\n4. Applying spectral filter...")
filtered = analyzer.spectral_filtering(test_img, 'highpass')
print(f"   [OK] Filtered image shape: {filtered.shape}")

print("\n" + "="*70)
print("SCIPY CAPABILITIES READY!")
print("="*70)
print("\nAvailable methods:")
print("  - frequency_domain_analysis() - 2D FFT")
print("  - wavelet_decomposition() - Multi-scale")
print("  - edge_detection_advanced() - Sobel/Prewitt/Laplacian")
print("  - texture_analysis() - Statistical")
print("  - morphological_analysis() - Structure detection")
print("  - correlation_analysis() - Periodicity")
print("  - spectral_filtering() - Highpass/Lowpass")
print("  - phase_correlation() - Motion detection")
print("\n" + "="*70 + "\n")
