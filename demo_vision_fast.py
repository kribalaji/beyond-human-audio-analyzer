"""Fast Vision Demo"""
import sys
from pathlib import Path
import numpy as np
import cv2
sys.path.insert(0, str(Path(__file__).parent))

from src.vision_analyzer import VisionAnalyzer
from src.ai_vision_detector import AIVisionDetector

print("\n" + "="*70)
print("VISION DEMO - FAST")
print("="*70)

# Create test directory
test_dir = Path('data/vision_samples')
test_dir.mkdir(parents=True, exist_ok=True)

# 1. Create thermal image
print("\n1. Creating thermal test image...")
thermal = np.zeros((300, 400), dtype=np.uint8)
cv2.circle(thermal, (150, 150), 40, 255, -1)
cv2.circle(thermal, (280, 200), 30, 220, -1)
thermal_file = test_dir / 'thermal.png'
cv2.imwrite(str(thermal_file), thermal)
print(f"   [OK] {thermal_file}")

# 2. Analyze with vision analyzer
print("\n2. Detecting infrared hotspots...")
analyzer = VisionAnalyzer()
ir_results = analyzer.detect_infrared(thermal)
print(f"   Hotspots found: {ir_results['total']}")
for i, event in enumerate(ir_results['events'][:3]):
    print(f"     #{i+1}: Position {event['position']}, Intensity {event['intensity']:.0f}")

# 3. AI detection
print("\n3. AI thermal analysis...")
ai = AIVisionDetector()
anomalies = ai.detect_thermal_anomalies(thermal)
print(f"   Thermal anomalies: {len(anomalies)}")

# 4. False color
print("\n4. Creating false-color visualization...")
results_dir = Path('results/vision')
results_dir.mkdir(parents=True, exist_ok=True)
colored = analyzer.create_false_color_image(thermal, 'thermal')
out_file = results_dir / 'thermal_colored.png'
cv2.imwrite(str(out_file), colored)
print(f"   [OK] {out_file}")

# 5. Multimodal test
print("\n5. Testing multimodal analyzer...")
from src.multimodal_analyzer import MultimodalAnalyzer
multi = MultimodalAnalyzer()
print("   [OK] Audio + Vision ready")

print("\n" + "="*70)
print("DEMO COMPLETE!")
print("="*70)
print("\nResults:")
print(f"  - IR hotspots detected: {ir_results['total']}")
print(f"  - AI anomalies found: {len(anomalies)}")
print(f"  - Files created: 2")
print(f"  - Location: {test_dir} and {results_dir}")
print("\n" + "="*70 + "\n")
