"""
Test Data Explorer - Analyze all images and videos
"""
import sys
from pathlib import Path
import cv2
import json
sys.path.insert(0, str(Path(__file__).parent))

from src.vision_analyzer import VisionAnalyzer
from src.ai_vision_detector import AIVisionDetector
from src.multimodal_analyzer import MultimodalAnalyzer

print("\n" + "="*70)
print("TEST DATA EXPLORER")
print("="*70)

analyzer = VisionAnalyzer()
ai = AIVisionDetector()
multi = MultimodalAnalyzer()

# Explore images
print("\n[EXPLORING IMAGES]")
test_dir = Path('data/vision_samples')
images = sorted(test_dir.glob('*.png'))

print(f"\nFound {len(images)} images\n")

detailed_results = []

for img_path in images:
    print(f"Analyzing: {img_path.name}")
    img = cv2.imread(str(img_path))
    
    # Full analysis
    result = {
        'filename': img_path.name,
        'size': f"{img.shape[1]}x{img.shape[0]}",
        'analyses': {}
    }
    
    # Spectral analysis
    spectral = analyzer.analyze_spectral_bands(img)
    result['analyses']['spectral'] = {
        'red_mean': f"{spectral['spectral_data']['red_band']['mean']:.1f}",
        'green_mean': f"{spectral['spectral_data']['green_band']['mean']:.1f}",
        'blue_mean': f"{spectral['spectral_data']['blue_band']['mean']:.1f}",
        'anomalies': spectral['anomalies']
    }
    
    # AI analysis
    blur = ai.analyze_motion_blur(img)
    result['analyses']['blur'] = {
        'is_blurred': bool(blur['is_blurred']),
        'score': f"{blur['blur_score']:.1f}"
    }
    
    patterns = ai.detect_periodic_patterns(img)
    result['analyses']['patterns'] = {
        'detected': bool(patterns['periodic_patterns_detected']),
        'count': int(patterns['pattern_count'])
    }
    
    detailed_results.append(result)
    
    print(f"  Size: {result['size']}")
    print(f"  RGB: R={result['analyses']['spectral']['red_mean']}, "
          f"G={result['analyses']['spectral']['green_mean']}, "
          f"B={result['analyses']['spectral']['blue_mean']}")
    print(f"  Blur: {result['analyses']['blur']['is_blurred']} "
          f"(score: {result['analyses']['blur']['score']})")
    print(f"  Patterns: {result['analyses']['patterns']['count']}")
    print()

# Explore videos
print("\n[EXPLORING VIDEOS]")
video_dir = Path('data/video_samples')
videos = sorted(video_dir.glob('*.mp4'))

print(f"\nFound {len(videos)} videos\n")

video_details = []

for vid_path in videos:
    print(f"Analyzing: {vid_path.name}")
    
    cap = cv2.VideoCapture(str(vid_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0
    
    # Sample first frame
    ret, first_frame = cap.read()
    cap.release()
    
    result = {
        'filename': vid_path.name,
        'resolution': f"{width}x{height}",
        'fps': f"{fps:.1f}",
        'frames': frame_count,
        'duration': f"{duration:.2f}s"
    }
    
    if ret:
        # Analyze first frame
        blur = ai.analyze_motion_blur(first_frame)
        result['first_frame_blur'] = f"{blur['blur_score']:.1f}"
    
    video_details.append(result)
    
    print(f"  Resolution: {result['resolution']}")
    print(f"  FPS: {result['fps']}")
    print(f"  Frames: {result['frames']}")
    print(f"  Duration: {result['duration']}")
    print()

# Save detailed report
print("\n[SAVING REPORT]")
report_dir = Path('results/vision_analysis')
report_dir.mkdir(parents=True, exist_ok=True)

report = {
    'summary': {
        'total_images': len(images),
        'total_videos': len(videos)
    },
    'images': detailed_results,
    'videos': video_details
}

report_file = report_dir / 'exploration_report.json'
with open(report_file, 'w') as f:
    json.dump(report, f, indent=2)

print(f"[OK] Report saved: {report_file}")

# Summary statistics
print("\n" + "="*70)
print("EXPLORATION SUMMARY")
print("="*70)

print(f"\nImages analyzed: {len(images)}")
print("\nImage categories:")
categories = {
    'astronomical': ['black_hole', 'supernova', 'spiral_galaxy', 'space_stars'],
    'thermal': ['thermal', 'building_thermal', 'wildlife_thermal', 'ir_space'],
    'uv': ['cells_uv', 'nebula_uv', 'uv_test'],
    'motion': ['bullet_motion', 'water_splash', 'motion_blur'],
    'spectral': ['spectral', 'vegetation_ndvi', 'aurora']
}

for cat, keywords in categories.items():
    count = sum(1 for img in images if any(kw in img.name for kw in keywords))
    print(f"  {cat.capitalize()}: {count}")

print(f"\nVideos analyzed: {len(videos)}")
for vid in video_details:
    print(f"  {vid['filename']}: {vid['frames']} frames @ {vid['fps']} FPS")

print("\nCapabilities tested:")
print("  [OK] Spectral band analysis")
print("  [OK] Motion blur detection")
print("  [OK] Periodic pattern detection")
print("  [OK] Video frame analysis")
print("  [OK] Multi-format support")

print("\n" + "="*70 + "\n")
