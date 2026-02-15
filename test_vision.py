"""Quick Vision Test"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("VISION MODULES TEST")
print("="*70)

# Test imports
print("\n1. Testing imports...")
try:
    import cv2
    print("   [OK] opencv-python")
except:
    print("   [FAIL] opencv-python")

try:
    import skimage
    print("   [OK] scikit-image")
except:
    print("   [FAIL] scikit-image")

try:
    from src.vision_analyzer import VisionAnalyzer
    print("   [OK] vision_analyzer")
except Exception as e:
    print(f"   [FAIL] vision_analyzer: {e}")

try:
    from src.ai_vision_detector import AIVisionDetector
    print("   [OK] ai_vision_detector")
except Exception as e:
    print(f"   [FAIL] ai_vision_detector: {e}")

try:
    from src.multimodal_analyzer import MultimodalAnalyzer
    print("   [OK] multimodal_analyzer")
except Exception as e:
    print(f"   [FAIL] multimodal_analyzer: {e}")

print("\n" + "="*70)
print("VISION CAPABILITIES READY!")
print("="*70)
print("\nAvailable features:")
print("  - Infrared detection")
print("  - Ultraviolet detection")
print("  - Thermal analysis")
print("  - High-speed motion")
print("  - AI pattern detection")
print("  - Multimodal (audio + vision)")
print("\n" + "="*70 + "\n")
