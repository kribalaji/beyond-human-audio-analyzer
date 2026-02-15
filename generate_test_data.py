"""
Comprehensive Test Data Generator
Creates diverse images and videos for vision analysis
"""
import sys
from pathlib import Path
import numpy as np
import cv2
sys.path.insert(0, str(Path(__file__).parent))

from src.vision_analyzer import VisionAnalyzer
from src.ai_vision_detector import AIVisionDetector

print("\n" + "="*70)
print("COMPREHENSIVE TEST DATA GENERATOR")
print("="*70)

test_dir = Path('data/vision_samples')
test_dir.mkdir(parents=True, exist_ok=True)
video_dir = Path('data/video_samples')
video_dir.mkdir(parents=True, exist_ok=True)

# ============================================================================
# PART 1: DIVERSE IMAGE GENERATION
# ============================================================================

print("\n[PART 1: GENERATING TEST IMAGES]")

# 1. Astronomical Images
print("\n1. Astronomical images...")

# Black hole simulation
black_hole = np.zeros((600, 600, 3), dtype=np.uint8)
center = (300, 300)
for r in range(250, 50, -5):
    color = int(255 * (250-r)/200)
    cv2.circle(black_hole, center, r, (color//3, color//2, color), 2)
cv2.imwrite(str(test_dir / 'black_hole.png'), black_hole)
print("   [OK] black_hole.png")

# Supernova
supernova = np.zeros((500, 500, 3), dtype=np.uint8)
cv2.circle(supernova, (250, 250), 100, (255, 200, 100), -1)
cv2.circle(supernova, (250, 250), 150, (255, 150, 50), 20)
cv2.circle(supernova, (250, 250), 200, (200, 100, 50), 10)
supernova = cv2.GaussianBlur(supernova, (21, 21), 0)
cv2.imwrite(str(test_dir / 'supernova.png'), supernova)
print("   [OK] supernova.png")

# 2. Microscopic/UV Images
print("\n2. Microscopic/UV images...")

# Cell structure (UV fluorescence)
cells = np.zeros((600, 800, 3), dtype=np.uint8)
for _ in range(15):
    x, y = np.random.randint(50, 750), np.random.randint(50, 550)
    size = np.random.randint(30, 60)
    cv2.circle(cells, (x, y), size, (255, 100, 200), -1)
    cv2.circle(cells, (x, y), size//2, (200, 150, 255), -1)
cells = cv2.GaussianBlur(cells, (5, 5), 0)
cv2.imwrite(str(test_dir / 'cells_uv.png'), cells)
print("   [OK] cells_uv.png")

# 3. Thermal/IR Images
print("\n3. Thermal/IR images...")

# Building thermal scan
building = np.zeros((600, 800), dtype=np.uint8)
building[100:500, 100:700] = 80  # Building base
building[150:250, 200:300] = 200  # Hot window
building[150:250, 450:550] = 210  # Hot window
building[350:450, 300:400] = 180  # Door
cv2.imwrite(str(test_dir / 'building_thermal.png'), building)
print("   [OK] building_thermal.png")

# Wildlife thermal
wildlife = np.zeros((500, 700), dtype=np.uint8)
wildlife[:, :] = 50  # Cold background
# Animal heat signatures
cv2.ellipse(wildlife, (200, 250), (60, 40), 0, 0, 360, 220, -1)  # Animal 1
cv2.ellipse(wildlife, (500, 300), (50, 35), 0, 0, 360, 210, -1)  # Animal 2
cv2.imwrite(str(test_dir / 'wildlife_thermal.png'), wildlife)
print("   [OK] wildlife_thermal.png")

# 4. High-Speed/Motion Images
print("\n4. High-speed motion images...")

# Bullet trajectory
bullet = np.zeros((400, 800, 3), dtype=np.uint8)
for i in range(0, 800, 50):
    cv2.circle(bullet, (i, 200), 10, (255, 255, 255), -1)
kernel = np.zeros((1, 50))
kernel[0, :] = 1/50
bullet = cv2.filter2D(bullet, -1, kernel)
cv2.imwrite(str(test_dir / 'bullet_motion.png'), bullet)
print("   [OK] bullet_motion.png")

# Water droplet splash
splash = np.zeros((600, 600, 3), dtype=np.uint8)
cv2.circle(splash, (300, 300), 50, (200, 200, 255), -1)
for i in range(5):
    angle = i * 72
    x = int(300 + 150 * np.cos(np.radians(angle)))
    y = int(300 + 150 * np.sin(np.radians(angle)))
    cv2.line(splash, (300, 300), (x, y), (150, 150, 255), 3)
cv2.imwrite(str(test_dir / 'water_splash.png'), splash)
print("   [OK] water_splash.png")

# 5. Spectral/Multispectral
print("\n5. Spectral analysis images...")

# Vegetation index (NDVI simulation)
ndvi = np.zeros((500, 500, 3), dtype=np.uint8)
ndvi[0:250, :] = [50, 150, 50]   # Healthy vegetation
ndvi[250:500, :] = [150, 100, 50] # Stressed vegetation
cv2.imwrite(str(test_dir / 'vegetation_ndvi.png'), ndvi)
print("   [OK] vegetation_ndvi.png")

# 6. Atmospheric/Weather
print("\n6. Atmospheric images...")

# Aurora borealis
aurora = np.zeros((600, 800, 3), dtype=np.uint8)
for i in range(600):
    intensity = int(128 + 127 * np.sin(i * 0.02))
    aurora[i, :] = [0, intensity, intensity//2]
aurora = cv2.GaussianBlur(aurora, (51, 51), 0)
cv2.imwrite(str(test_dir / 'aurora.png'), aurora)
print("   [OK] aurora.png")

# ============================================================================
# PART 2: VIDEO GENERATION
# ============================================================================

print("\n[PART 2: GENERATING TEST VIDEOS]")

# Video 1: Rotating thermal object
print("\n1. Creating thermal rotation video...")
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video1 = cv2.VideoWriter(str(video_dir / 'thermal_rotation.mp4'), fourcc, 30, (400, 400), False)

for angle in range(0, 360, 3):
    frame = np.zeros((400, 400), dtype=np.uint8)
    center = (200, 200)
    axes = (80, 40)
    cv2.ellipse(frame, center, axes, angle, 0, 360, 255, -1)
    video1.write(frame)
video1.release()
print("   [OK] thermal_rotation.mp4 (120 frames)")

# Video 2: Moving objects (high-speed simulation)
print("\n2. Creating high-speed motion video...")
video2 = cv2.VideoWriter(str(video_dir / 'highspeed_motion.mp4'), fourcc, 60, (640, 480), True)

for i in range(180):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    x = int(50 + i * 3)
    y = int(240 + 100 * np.sin(i * 0.1))
    cv2.circle(frame, (x, y), 20, (255, 255, 255), -1)
    video2.write(frame)
video2.release()
print("   [OK] highspeed_motion.mp4 (180 frames)")

# Video 3: Pulsating light source
print("\n3. Creating pulsating light video...")
video3 = cv2.VideoWriter(str(video_dir / 'pulsating_light.mp4'), fourcc, 30, (500, 500), True)

for i in range(90):
    frame = np.zeros((500, 500, 3), dtype=np.uint8)
    radius = int(50 + 30 * np.sin(i * 0.2))
    intensity = int(200 + 55 * np.sin(i * 0.2))
    cv2.circle(frame, (250, 250), radius, (intensity, intensity, intensity), -1)
    video3.write(frame)
video3.release()
print("   [OK] pulsating_light.mp4 (90 frames)")

# Video 4: Thermal gradient animation
print("\n4. Creating thermal gradient video...")
video4 = cv2.VideoWriter(str(video_dir / 'thermal_gradient.mp4'), fourcc, 30, (600, 400), False)

for i in range(120):
    frame = np.zeros((400, 600), dtype=np.uint8)
    for y in range(400):
        intensity = int((y + i) % 256)
        frame[y, :] = intensity
    video4.write(frame)
video4.release()
print("   [OK] thermal_gradient.mp4 (120 frames)")

# ============================================================================
# PART 3: ANALYZE ALL TEST DATA
# ============================================================================

print("\n[PART 3: ANALYZING TEST DATA]")

analyzer = VisionAnalyzer()
ai = AIVisionDetector()
results_dir = Path('results/vision_analysis')
results_dir.mkdir(parents=True, exist_ok=True)

# Analyze images
print("\nAnalyzing images...")
image_files = list(test_dir.glob('*.png'))
analysis_results = []

for img_file in image_files:
    img = cv2.imread(str(img_file))
    if img is None:
        continue
    
    result = {
        'file': img_file.name,
        'ir_hotspots': 0,
        'uv_patterns': 0,
        'thermal_anomalies': 0,
        'light_sources': 0
    }
    
    # IR detection
    if len(img.shape) == 2:
        ir = analyzer.detect_infrared(img)
        result['ir_hotspots'] = ir['total']
        thermal = ai.detect_thermal_anomalies(img)
        result['thermal_anomalies'] = len(thermal)
    
    # UV detection
    uv = analyzer.detect_ultraviolet(img)
    result['uv_patterns'] = uv['total']
    
    # Light sources
    lights = ai.detect_invisible_light(img)
    result['light_sources'] = lights['count']
    
    analysis_results.append(result)
    print(f"   {img_file.name}: IR={result['ir_hotspots']}, UV={result['uv_patterns']}, "
          f"Thermal={result['thermal_anomalies']}, Lights={result['light_sources']}")

# Analyze videos
print("\nAnalyzing videos...")
video_files = list(video_dir.glob('*.mp4'))
video_results = []

for vid_file in video_files:
    motion = analyzer.detect_high_speed_motion(str(vid_file), fps_threshold=30)
    result = {
        'file': vid_file.name,
        'fps': motion['fps'],
        'motion_events': motion['total']
    }
    video_results.append(result)
    print(f"   {vid_file.name}: FPS={result['fps']:.1f}, Motion events={result['motion_events']}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*70)
print("GENERATION & ANALYSIS COMPLETE")
print("="*70)

print(f"\nImages created: {len(image_files)}")
print("Categories:")
print("  - Astronomical: 2 (black hole, supernova)")
print("  - Microscopic/UV: 1 (cells)")
print("  - Thermal/IR: 2 (building, wildlife)")
print("  - High-speed: 2 (bullet, splash)")
print("  - Spectral: 1 (vegetation)")
print("  - Atmospheric: 1 (aurora)")

print(f"\nVideos created: {len(video_files)}")
print("  - thermal_rotation.mp4 (120 frames)")
print("  - highspeed_motion.mp4 (180 frames)")
print("  - pulsating_light.mp4 (90 frames)")
print("  - thermal_gradient.mp4 (120 frames)")

print("\nTotal detections:")
total_ir = sum(r['ir_hotspots'] for r in analysis_results)
total_uv = sum(r['uv_patterns'] for r in analysis_results)
total_thermal = sum(r['thermal_anomalies'] for r in analysis_results)
total_lights = sum(r['light_sources'] for r in analysis_results)
total_motion = sum(r['motion_events'] for r in video_results)

print(f"  IR hotspots: {total_ir}")
print(f"  UV patterns: {total_uv}")
print(f"  Thermal anomalies: {total_thermal}")
print(f"  Light sources: {total_lights}")
print(f"  Motion events: {total_motion}")

print("\nLocations:")
print(f"  Images: {test_dir}")
print(f"  Videos: {video_dir}")
print(f"  Results: {results_dir}")

print("\n" + "="*70 + "\n")
