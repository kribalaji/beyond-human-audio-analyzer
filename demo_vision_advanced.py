"""
Advanced Vision Demo - Space Images, Blur Detection, Complex Scenarios
"""
import sys
from pathlib import Path
import numpy as np
import cv2
sys.path.insert(0, str(Path(__file__).parent))

from src.vision_analyzer import VisionAnalyzer
from src.ai_vision_detector import AIVisionDetector
from src.multimodal_analyzer import MultimodalAnalyzer

print("\n" + "="*70)
print("ADVANCED VISION DEMO - SPACE & COMPLEX SCENARIOS")
print("="*70)

test_dir = Path('data/vision_samples')
test_dir.mkdir(parents=True, exist_ok=True)
results_dir = Path('results/vision')
results_dir.mkdir(parents=True, exist_ok=True)

analyzer = VisionAnalyzer()
ai = AIVisionDetector()

# 1. SPACE IMAGE - Stars and galaxies
print("\n1. Creating space image (stars/galaxies)...")
space = np.zeros((600, 800, 3), dtype=np.uint8)
# Add stars (bright points)
for _ in range(200):
    x, y = np.random.randint(0, 800), np.random.randint(0, 600)
    brightness = np.random.randint(150, 255)
    cv2.circle(space, (x, y), 1, (brightness, brightness, brightness), -1)
# Add galaxies (bright regions)
cv2.circle(space, (200, 150), 60, (180, 160, 140), -1)
cv2.circle(space, (600, 400), 80, (200, 180, 160), -1)
cv2.ellipse(space, (400, 300), (100, 40), 45, 0, 360, (190, 170, 150), -1)
space_file = test_dir / 'space_stars.png'
cv2.imwrite(str(space_file), space)
print(f"   [OK] {space_file}")

# Analyze space image
print("   Analyzing space image...")
light_sources = ai.detect_invisible_light(space)
print(f"   Light sources detected: {light_sources['count']}")
patterns = ai.detect_periodic_patterns(space)
print(f"   Periodic patterns: {patterns['periodic_patterns_detected']}")

# 2. NEBULA-LIKE IMAGE (UV/IR simulation)
print("\n2. Creating nebula image (UV/IR simulation)...")
nebula = np.zeros((600, 800, 3), dtype=np.uint8)
# Create colorful nebula effect
for i in range(600):
    for j in range(800):
        r = np.sqrt((i-300)**2 + (j-400)**2)
        if r < 250:
            intensity = int(255 * (1 - r/250))
            nebula[i, j] = [intensity//3, intensity//2, intensity]  # Blue-purple
nebula_file = test_dir / 'nebula_uv.png'
cv2.imwrite(str(nebula_file), nebula)
print(f"   [OK] {nebula_file}")

# Analyze nebula
uv_results = analyzer.detect_ultraviolet(nebula)
spectral = analyzer.analyze_spectral_bands(nebula)
print(f"   UV patterns: {uv_results['total']}")
print(f"   Spectral anomalies: {len(spectral['anomalies'])}")

# 3. MOTION BLUR IMAGE
print("\n3. Creating motion blur image...")
sharp = np.zeros((400, 600, 3), dtype=np.uint8)
cv2.rectangle(sharp, (100, 150), (200, 250), (255, 255, 255), -1)
cv2.circle(sharp, (400, 200), 50, (200, 200, 200), -1)
# Apply motion blur
kernel_size = 30
kernel = np.zeros((kernel_size, kernel_size))
kernel[int((kernel_size-1)/2), :] = np.ones(kernel_size)
kernel = kernel / kernel_size
blurred = cv2.filter2D(sharp, -1, kernel)
blur_file = test_dir / 'motion_blur.png'
cv2.imwrite(str(blur_file), blurred)
print(f"   [OK] {blur_file}")

# Analyze blur
blur_analysis = ai.analyze_motion_blur(blurred)
print(f"   Blur detected: {blur_analysis['is_blurred']}")
print(f"   Blur score: {blur_analysis['blur_score']:.1f}")
print(f"   Motion magnitude: {blur_analysis['motion_magnitude']:.1f}")

# 4. INFRARED SPACE (Hot celestial objects)
print("\n4. Creating IR space image (hot objects)...")
ir_space = np.zeros((500, 700), dtype=np.uint8)
# Hot stars
cv2.circle(ir_space, (150, 150), 30, 255, -1)
cv2.circle(ir_space, (400, 250), 40, 240, -1)
cv2.circle(ir_space, (550, 350), 25, 230, -1)
# Thermal gradient (space dust)
for i in range(500):
    ir_space[i, :] += int(i * 0.05)
ir_space_file = test_dir / 'ir_space.png'
cv2.imwrite(str(ir_space_file), ir_space)
print(f"   [OK] {ir_space_file}")

# Analyze IR space
ir_results = analyzer.detect_infrared(ir_space)
thermal_anomalies = ai.detect_thermal_anomalies(ir_space)
print(f"   IR hotspots: {ir_results['total']}")
print(f"   Thermal anomalies: {len(thermal_anomalies)}")

# 5. SPECTRAL SEGMENTATION TEST
print("\n5. Creating multi-spectral image...")
spectral_img = np.zeros((400, 600, 3), dtype=np.uint8)
spectral_img[0:200, 0:200] = [255, 0, 0]      # Red region
spectral_img[0:200, 200:400] = [0, 255, 0]    # Green region
spectral_img[0:200, 400:600] = [0, 0, 255]    # Blue region
spectral_img[200:400, 0:300] = [255, 255, 0]  # Yellow region
spectral_img[200:400, 300:600] = [255, 0, 255] # Magenta region
spectral_file = test_dir / 'spectral_bands.png'
cv2.imwrite(str(spectral_file), spectral_img)
print(f"   [OK] {spectral_file}")

# Segment spectral regions
segments = ai.segment_spectral_regions(spectral_img)
segmented_file = results_dir / 'spectral_segmented.png'
cv2.imwrite(str(segmented_file), segments['segmented_image'])
print(f"   Spectral regions: {segments['num_regions']}")
print(f"   [OK] Segmented: {segmented_file}")

# 6. GALAXY WITH PERIODIC PATTERNS
print("\n6. Creating galaxy with periodic structure...")
galaxy = np.zeros((600, 600), dtype=np.uint8)
center = (300, 300)
# Spiral arms with periodic pattern
for angle in range(0, 360, 2):
    for r in range(50, 250, 5):
        theta = np.radians(angle + r/5)
        x = int(center[0] + r * np.cos(theta))
        y = int(center[1] + r * np.sin(theta))
        if 0 <= x < 600 and 0 <= y < 600:
            galaxy[y, x] = 200
# Blur to make it look like galaxy
galaxy = cv2.GaussianBlur(galaxy, (15, 15), 0)
galaxy_file = test_dir / 'spiral_galaxy.png'
cv2.imwrite(str(galaxy_file), galaxy)
print(f"   [OK] {galaxy_file}")

# Detect patterns
galaxy_patterns = ai.detect_periodic_patterns(galaxy)
print(f"   Periodic patterns: {galaxy_patterns['periodic_patterns_detected']}")
print(f"   Pattern count: {galaxy_patterns['pattern_count']}")

# 7. CREATE FALSE-COLOR VISUALIZATIONS
print("\n7. Creating false-color visualizations...")
# Thermal colormap for IR space
ir_colored = analyzer.create_false_color_image(ir_space, 'thermal')
cv2.imwrite(str(results_dir / 'ir_space_colored.png'), ir_colored)
print(f"   [OK] IR false-color")

# UV colormap for nebula
nebula_gray = cv2.cvtColor(nebula, cv2.COLOR_BGR2GRAY)
uv_colored = analyzer.create_false_color_image(nebula_gray, 'uv')
cv2.imwrite(str(results_dir / 'nebula_uv_colored.png'), uv_colored)
print(f"   [OK] UV false-color")

# 8. SUMMARY STATISTICS
print("\n" + "="*70)
print("ANALYSIS SUMMARY")
print("="*70)

all_files = list(test_dir.glob('*.png'))
print(f"\nTest images created: {len(all_files)}")
for f in all_files:
    print(f"  - {f.name}")

result_files = list(results_dir.glob('*.png'))
print(f"\nResult images created: {len(result_files)}")
for f in result_files:
    print(f"  - {f.name}")

print("\nDetection Results:")
print(f"  Space light sources: {light_sources['count']}")
print(f"  UV patterns: {uv_results['total']}")
print(f"  IR hotspots: {ir_results['total']}")
print(f"  Thermal anomalies: {len(thermal_anomalies)}")
print(f"  Motion blur detected: {blur_analysis['is_blurred']}")
print(f"  Spectral regions: {segments['num_regions']}")
print(f"  Galaxy patterns: {galaxy_patterns['pattern_count']}")

print("\n" + "="*70)
print("ADVANCED DEMO COMPLETE!")
print("="*70)
print("\nCapabilities Demonstrated:")
print("  [OK] Space image analysis (stars, galaxies)")
print("  [OK] Nebula UV/IR detection")
print("  [OK] Motion blur analysis")
print("  [OK] Infrared space objects")
print("  [OK] Spectral segmentation")
print("  [OK] Periodic pattern detection")
print("  [OK] False-color visualization")
print("\n" + "="*70 + "\n")
