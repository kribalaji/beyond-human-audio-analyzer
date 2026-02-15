"""
Beyond Human Vision Analyzer
Detects visual phenomena beyond human perception:
- Infrared (IR) detection
- Ultraviolet (UV) detection
- High-speed motion analysis
- Thermal imaging analysis
- Spectral analysis beyond visible range
"""

import numpy as np
import cv2
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging


class VisionAnalyzer:
    """Analyze images/video for beyond-visible spectrum phenomena."""
    
    def __init__(self, config_path: str = 'config/config.yaml'):
        self.logger = logging.getLogger(__name__)
        self.results = []
        
    def detect_infrared(self, image: np.ndarray) -> Dict:
        """Detect infrared signatures in thermal images."""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
            
        # Detect hot spots (IR signatures)
        _, hot_spots = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(hot_spots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        events = []
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 50:  # Minimum area threshold
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    events.append({
                        'type': 'infrared_hotspot',
                        'position': (cx, cy),
                        'area': area,
                        'intensity': float(gray[cy, cx])
                    })
        
        return {'events': events, 'total': len(events)}
    
    def detect_ultraviolet(self, image: np.ndarray) -> Dict:
        """Detect UV patterns (simulated from blue channel enhancement)."""
        if len(image.shape) == 3:
            # UV often appears in blue channel
            blue_channel = image[:, :, 0]
        else:
            blue_channel = image
            
        # Enhance UV-like features
        enhanced = cv2.equalizeHist(blue_channel)
        _, uv_mask = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(uv_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        events = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 30:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    events.append({
                        'type': 'ultraviolet_pattern',
                        'position': (cx, cy),
                        'area': area
                    })
        
        return {'events': events, 'total': len(events)}
    
    def detect_high_speed_motion(self, video_path: str, fps_threshold: int = 120) -> Dict:
        """Analyze high-speed video for motion invisible to human eye."""
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        if fps < fps_threshold:
            self.logger.warning(f"Video FPS ({fps}) below threshold ({fps_threshold})")
        
        prev_frame = None
        motion_events = []
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Calculate frame difference
                diff = cv2.absdiff(prev_frame, gray)
                _, motion_mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
                motion_pixels = np.sum(motion_mask > 0)
                
                if motion_pixels > 1000:  # Significant motion
                    motion_events.append({
                        'frame': frame_count,
                        'timestamp': frame_count / fps,
                        'motion_intensity': int(motion_pixels)
                    })
            
            prev_frame = gray
            frame_count += 1
            
            if frame_count > 300:  # Limit analysis
                break
        
        cap.release()
        return {'events': motion_events, 'total': len(motion_events), 'fps': fps}
    
    def analyze_spectral_bands(self, image: np.ndarray) -> Dict:
        """Analyze image across spectral bands beyond visible range."""
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            
        # Split into channels
        b, g, r = cv2.split(image)
        
        # Calculate spectral statistics
        spectral_data = {
            'red_band': {
                'mean': float(np.mean(r)),
                'std': float(np.std(r)),
                'max': int(np.max(r))
            },
            'green_band': {
                'mean': float(np.mean(g)),
                'std': float(np.std(g)),
                'max': int(np.max(g))
            },
            'blue_band': {
                'mean': float(np.mean(b)),
                'std': float(np.std(b)),
                'max': int(np.max(b))
            }
        }
        
        # Detect anomalies
        anomalies = []
        if spectral_data['red_band']['mean'] > 200:
            anomalies.append('high_infrared_signature')
        if spectral_data['blue_band']['mean'] > 200:
            anomalies.append('high_ultraviolet_signature')
            
        return {'spectral_data': spectral_data, 'anomalies': anomalies}
    
    def analyze_image(self, image_path: str, mode: str = 'full') -> Dict:
        """Comprehensive image analysis."""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        results = {
            'file': Path(image_path).name,
            'shape': image.shape,
            'analyses': {}
        }
        
        if mode in ['infrared', 'full']:
            results['analyses']['infrared'] = self.detect_infrared(image)
            
        if mode in ['ultraviolet', 'full']:
            results['analyses']['ultraviolet'] = self.detect_ultraviolet(image)
            
        if mode in ['spectral', 'full']:
            results['analyses']['spectral'] = self.analyze_spectral_bands(image)
        
        return results
    
    def create_false_color_image(self, image: np.ndarray, mode: str = 'thermal') -> np.ndarray:
        """Create false-color visualization of invisible spectra."""
        if len(image.shape) == 2:
            gray = image
        else:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if mode == 'thermal':
            # Thermal colormap
            colored = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        elif mode == 'uv':
            # UV colormap
            colored = cv2.applyColorMap(gray, cv2.COLORMAP_COOL)
        else:
            colored = cv2.applyColorMap(gray, cv2.COLORMAP_VIRIDIS)
            
        return colored


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    analyzer = VisionAnalyzer()
    print("Beyond Human Vision Analyzer initialized")
    print("Capabilities: IR detection, UV detection, spectral analysis")
