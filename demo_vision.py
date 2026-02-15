"""
Vision Analysis Demo
Demonstrates beyond-human vision detection capabilities
"""

import sys
from pathlib import Path
import numpy as np
import cv2

sys.path.insert(0, str(Path(__file__).parent))

from src.vision_analyzer import VisionAnalyzer
from src.ai_vision_detector import AIVisionDetector
from src.multimodal_analyzer import MultimodalAnalyzer


def create_test_images():
    """Generate test images simulating IR/UV phenomena."""
    print("\nGenerating test images...")
    
    test_dir = Path('data/vision_samples')
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Simulated thermal/IR image
    thermal = np.zeros((480, 640), dtype=np.uint8)
    # Add hot spots
    cv2.circle(thermal, (200, 200), 50, 255, -1)
    cv2.circle(thermal, (400, 300), 30, 220, -1)
    cv2.circle(thermal, (500, 150), 40, 240, -1)
    # Add gradient (temperature field)
    for i in range(480):
        thermal[i, :] += int(i * 0.1)
    thermal_file = test_dir / 'thermal_test.png'
    cv2.imwrite(str(thermal_file), thermal)
    print(f"  [OK] Created: {thermal_file}")
    
    # 2. Simulated UV image
    uv = np.zeros((480, 640, 3), dtype=np.uint8)
    # UV patterns (high blue channel)
    cv2.rectangle(uv, (100, 100), (300, 300), (255, 100, 50), -1)
    cv2.circle(uv, (450, 200), 80, (240, 120, 60), -1)
    uv_file = test_dir / 'uv_test.png'
    cv2.imwrite(str(uv_file), uv)
    print(f"  [OK] Created: {uv_file}")
    
    # 3. High-contrast spectral image
    spectral = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    # Add structured patterns
    spectral[100:200, 100:300] = [255, 0, 0]  # Red region
    spectral[250:350, 350:500] = [0, 0, 255]  # Blue region
    spectral_file = test_dir / 'spectral_test.png'
    cv2.imwrite(str(spectral_file), spectral)
    print(f"  [OK] Created: {spectral_file}")
    
    return thermal_file, uv_file, spectral_file


def demo_vision_analysis():
    """Run vision analysis demo."""
    print("\n" + "="*70)
    print("BEYOND HUMAN VISION ANALYZER - DEMO")
    print("="*70)
    
    # Create test images
    thermal_file, uv_file, spectral_file = create_test_images()
    
    # Initialize analyzers
    print("\n1. Initializing analyzers...")
    vision = VisionAnalyzer()
    ai_vision = AIVisionDetector()
    print("  [OK] Vision analyzers ready")
    
    # Test 1: Thermal/IR analysis
    print("\n2. Analyzing thermal image...")
    print(f"   File: {thermal_file.name}")
    thermal_img = cv2.imread(str(thermal_file), cv2.IMREAD_GRAYSCALE)
    ir_results = vision.detect_infrared(thermal_img)
    print(f"   Infrared hotspots detected: {ir_results['total']}")
    for i, event in enumerate(ir_results['events'][:3]):
        print(f"     - Hotspot {i+1}: Position {event['position']}, "
              f"Intensity {event['intensity']:.1f}")
    
    # AI thermal analysis
    thermal_anomalies = ai_vision.detect_thermal_anomalies(thermal_img)
    print(f"   AI thermal anomalies: {len(thermal_anomalies)}")
    
    # Test 2: UV analysis
    print("\n3. Analyzing UV image...")
    print(f"   File: {uv_file.name}")
    uv_img = cv2.imread(str(uv_file))
    uv_results = vision.detect_ultraviolet(uv_img)
    print(f"   UV patterns detected: {uv_results['total']}")
    
    # Test 3: Spectral analysis
    print("\n4. Analyzing spectral bands...")
    print(f"   File: {spectral_file.name}")
    spectral_img = cv2.imread(str(spectral_file))
    spectral_results = vision.analyze_spectral_bands(spectral_img)
    print(f"   Spectral bands analyzed:")
    for band, data in spectral_results['spectral_data'].items():
        print(f"     - {band}: mean={data['mean']:.1f}, max={data['max']}")
    if spectral_results['anomalies']:
        print(f"   Anomalies: {', '.join(spectral_results['anomalies'])}")
    
    # Test 4: AI pattern detection
    print("\n5. AI pattern detection...")
    patterns = ai_vision.detect_periodic_patterns(spectral_img)
    print(f"   Periodic patterns: {patterns['periodic_patterns_detected']}")
    print(f"   Pattern count: {patterns['pattern_count']}")
    
    # Test 5: False color visualization
    print("\n6. Creating false-color visualizations...")
    results_dir = Path('results/vision')
    results_dir.mkdir(parents=True, exist_ok=True)
    
    thermal_colored = vision.create_false_color_image(thermal_img, 'thermal')
    thermal_out = results_dir / 'thermal_false_color.png'
    cv2.imwrite(str(thermal_out), thermal_colored)
    print(f"   [OK] Saved: {thermal_out}")
    
    uv_colored = vision.create_false_color_image(uv_img, 'uv')
    uv_out = results_dir / 'uv_false_color.png'
    cv2.imwrite(str(uv_out), uv_colored)
    print(f"   [OK] Saved: {uv_out}")
    
    # Summary
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nCapabilities tested:")
    print("  [OK] Infrared/thermal detection")
    print("  [OK] Ultraviolet pattern detection")
    print("  [OK] Spectral band analysis")
    print("  [OK] AI thermal anomaly detection")
    print("  [OK] Periodic pattern detection")
    print("  [OK] False-color visualization")
    
    print("\nGenerated files:")
    print(f"  - data/vision_samples/ (3 test images)")
    print(f"  - results/vision/ (2 false-color images)")
    
    print("\n" + "="*70 + "\n")


def demo_multimodal():
    """Demo multimodal analysis."""
    print("\n" + "="*70)
    print("MULTIMODAL ANALYSIS DEMO")
    print("="*70)
    
    analyzer = MultimodalAnalyzer()
    
    # Check for existing test files
    audio_file = Path('data/samples/demo_mixed.wav')
    image_file = Path('data/vision_samples/thermal_test.png')
    
    if audio_file.exists() and image_file.exists():
        print("\nRunning multimodal analysis...")
        report = analyzer.create_comprehensive_report(
            audio_file=str(audio_file),
            image_file=str(image_file)
        )
        
        print("\nMultimodal Analysis Results:")
        print(f"  Audio events: {report['summary']['total_audio_events']}")
        print(f"  Visual events: {report['summary']['total_visual_events']}")
        print(f"  Detection types: {len(report['summary']['detection_types'])}")
        
        print("\n" + "="*70 + "\n")
    else:
        print("\n[INFO] Run audio demo first: python demo.py")
        print("[INFO] Then run this vision demo to enable multimodal analysis")
        print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.WARNING)
    
    try:
        demo_vision_analysis()
        demo_multimodal()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nMake sure OpenCV is installed:")
        print("  pip install opencv-python")
        sys.exit(1)
