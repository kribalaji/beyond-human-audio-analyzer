"""
SciPy Vision Analysis Demo
Advanced signal processing on images
"""
import sys
from pathlib import Path
import cv2
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))

from src.scipy_vision_analyzer import ScipyVisionAnalyzer

print("\n" + "="*70)
print("SCIPY VISION ANALYSIS DEMO")
print("="*70)

analyzer = ScipyVisionAnalyzer()
test_dir = Path('data/vision_samples')
results_dir = Path('results/scipy_vision')
results_dir.mkdir(parents=True, exist_ok=True)

# Select diverse test images
test_images = [
    'spiral_galaxy.png',
    'building_thermal.png',
    'cells_uv.png',
    'supernova.png'
]

print("\n[ANALYZING TEST IMAGES WITH SCIPY]\n")

for img_name in test_images:
    img_path = test_dir / img_name
    if not img_path.exists():
        continue
    
    print(f"Analyzing: {img_name}")
    img = cv2.imread(str(img_path))
    
    # Comprehensive analysis
    results = analyzer.comprehensive_analysis(img)
    
    print(f"  Frequency Domain:")
    print(f"    Dominant frequencies: {results['frequency_domain']['dominant_frequencies']}")
    print(f"    Spectral entropy: {results['frequency_domain']['spectral_entropy']:.2f}")
    
    print(f"  Wavelet Analysis:")
    print(f"    Levels: {results['wavelet']['levels']}")
    print(f"    Detail ratio: {results['wavelet']['detail_ratio']:.3f}")
    
    print(f"  Edge Detection:")
    print(f"    Sobel mean: {results['edges']['sobel_mean']:.1f}")
    print(f"    Edge density: {results['edges']['edge_density']:.3f}")
    
    print(f"  Texture:")
    print(f"    Complexity: {results['texture']['texture_complexity']:.1f}")
    print(f"    Gradient strength: {results['texture']['gradient_strength']:.1f}")
    
    print(f"  Correlation:")
    print(f"    Periodic structure: {results['correlation']['has_periodic_structure']}")
    print(f"    Periodicity score: {results['correlation']['periodicity_score']:.3f}")
    
    # Apply spectral filters
    highpass = analyzer.spectral_filtering(img, 'highpass')
    lowpass = analyzer.spectral_filtering(img, 'lowpass')
    
    # Save filtered images
    cv2.imwrite(str(results_dir / f'{img_name[:-4]}_highpass.png'), highpass)
    cv2.imwrite(str(results_dir / f'{img_name[:-4]}_lowpass.png'), lowpass)
    print(f"  [OK] Saved filtered images")
    print()

# Video analysis - phase correlation
print("\n[VIDEO ANALYSIS - PHASE CORRELATION]\n")

video_dir = Path('data/video_samples')
video_file = video_dir / 'highspeed_motion.mp4'

if video_file.exists():
    print(f"Analyzing: {video_file.name}")
    cap = cv2.VideoCapture(str(video_file))
    
    ret, prev_frame = cap.read()
    frame_count = 0
    motion_detections = []
    
    while ret and frame_count < 50:  # Analyze first 50 frames
        ret, curr_frame = cap.read()
        if not ret:
            break
        
        # Phase correlation between consecutive frames
        phase_corr = analyzer.phase_correlation(prev_frame, curr_frame)
        
        if phase_corr['motion_detected']:
            motion_detections.append({
                'frame': frame_count,
                'shift_x': phase_corr['shift_x'],
                'shift_y': phase_corr['shift_y'],
                'correlation': phase_corr['correlation_peak']
            })
        
        prev_frame = curr_frame
        frame_count += 1
    
    cap.release()
    
    print(f"  Frames analyzed: {frame_count}")
    print(f"  Motion detected: {len(motion_detections)} frames")
    if motion_detections:
        avg_shift_x = np.mean([m['shift_x'] for m in motion_detections])
        avg_shift_y = np.mean([m['shift_y'] for m in motion_detections])
        print(f"  Average motion: X={avg_shift_x:.1f}, Y={avg_shift_y:.1f} pixels")

print("\n" + "="*70)
print("SCIPY ANALYSIS COMPLETE")
print("="*70)

print("\nCapabilities Demonstrated:")
print("  [OK] 2D FFT frequency analysis")
print("  [OK] Wavelet decomposition")
print("  [OK] Advanced edge detection (Sobel, Prewitt, Laplacian)")
print("  [OK] Texture analysis")
print("  [OK] Morphological operations")
print("  [OK] Auto-correlation (periodicity detection)")
print("  [OK] Spectral filtering (highpass/lowpass)")
print("  [OK] Phase correlation (motion detection)")

print(f"\nFiltered images saved: {results_dir}")
print("  - *_highpass.png (high-frequency features)")
print("  - *_lowpass.png (low-frequency features)")

print("\n" + "="*70 + "\n")
