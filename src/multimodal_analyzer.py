"""
Multimodal Beyond-Human Perception Analyzer
Integrates audio and vision analysis for comprehensive detection
"""

import sys
from pathlib import Path
import numpy as np
import cv2
import logging
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import AudioAnalyzer
from src.vision_analyzer import VisionAnalyzer
from src.ai_vision_detector import AIVisionDetector


class MultimodalAnalyzer:
    """Unified analyzer for audio and visual beyond-human perception."""
    
    def __init__(self, config_path: str = 'config/config.yaml'):
        self.logger = logging.getLogger(__name__)
        
        # Initialize analyzers
        self.audio_analyzer = AudioAnalyzer(config_path)
        self.vision_analyzer = VisionAnalyzer(config_path)
        self.ai_vision = AIVisionDetector()
        
        self.logger.info("Multimodal analyzer initialized")
    
    def analyze_audio_file(self, file_path: str, mode: str = 'full') -> Dict:
        """Analyze audio for beyond-human frequencies."""
        return self.audio_analyzer.analyze_full_spectrum(file_path, mode)
    
    def analyze_image_file(self, file_path: str, mode: str = 'full') -> Dict:
        """Analyze image for beyond-visible spectrum."""
        results = self.vision_analyzer.analyze_image(file_path, mode)
        
        # Add AI analysis
        image = cv2.imread(file_path)
        if image is not None:
            results['ai_analysis'] = {
                'thermal_anomalies': self.ai_vision.detect_thermal_anomalies(image),
                'invisible_light': self.ai_vision.detect_invisible_light(image),
                'motion_blur': self.ai_vision.analyze_motion_blur(image),
                'periodic_patterns': self.ai_vision.detect_periodic_patterns(image)
            }
        
        return results
    
    def analyze_video_file(self, file_path: str) -> Dict:
        """Analyze video for high-speed motion and temporal patterns."""
        results = {
            'file': Path(file_path).name,
            'type': 'video',
            'analyses': {}
        }
        
        # High-speed motion analysis
        results['analyses']['motion'] = self.vision_analyzer.detect_high_speed_motion(file_path)
        
        # Frame-by-frame AI analysis (sample frames)
        cap = cv2.VideoCapture(file_path)
        frame_analyses = []
        
        for i in range(0, 100, 10):  # Sample every 10th frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                frame_analysis = {
                    'frame': i,
                    'thermal': len(self.ai_vision.detect_thermal_anomalies(frame)),
                    'light_sources': self.ai_vision.detect_invisible_light(frame)['count']
                }
                frame_analyses.append(frame_analysis)
        
        cap.release()
        results['analyses']['frame_samples'] = frame_analyses
        
        return results
    
    def create_comprehensive_report(self, audio_file: str = None, 
                                   image_file: str = None,
                                   video_file: str = None) -> Dict:
        """Generate comprehensive multimodal analysis report."""
        report = {
            'analysis_type': 'multimodal',
            'results': {}
        }
        
        if audio_file:
            self.logger.info(f"Analyzing audio: {audio_file}")
            report['results']['audio'] = self.analyze_audio_file(audio_file)
        
        if image_file:
            self.logger.info(f"Analyzing image: {image_file}")
            report['results']['image'] = self.analyze_image_file(image_file)
        
        if video_file:
            self.logger.info(f"Analyzing video: {video_file}")
            report['results']['video'] = self.analyze_video_file(video_file)
        
        # Summary statistics
        report['summary'] = self._generate_summary(report['results'])
        
        return report
    
    def _generate_summary(self, results: Dict) -> Dict:
        """Generate summary of all detections."""
        summary = {
            'total_audio_events': 0,
            'total_visual_events': 0,
            'detection_types': []
        }
        
        if 'audio' in results:
            summary['total_audio_events'] = results['audio'].get('total_events', 0)
            if summary['total_audio_events'] > 0:
                summary['detection_types'].append('audio_beyond_human')
        
        if 'image' in results:
            for analysis_type, data in results['image'].get('analyses', {}).items():
                if isinstance(data, dict) and 'total' in data:
                    summary['total_visual_events'] += data['total']
                    summary['detection_types'].append(f'visual_{analysis_type}')
        
        return summary


def demo_multimodal():
    """Demonstration of multimodal analysis."""
    print("\n" + "="*70)
    print("MULTIMODAL BEYOND-HUMAN PERCEPTION ANALYZER")
    print("="*70)
    
    analyzer = MultimodalAnalyzer()
    
    print("\nCapabilities:")
    print("  [AUDIO]")
    print("    - Infrasound detection (<20 Hz)")
    print("    - Ultrasound detection (>20 kHz)")
    print("  [VISION]")
    print("    - Infrared detection")
    print("    - Ultraviolet detection")
    print("    - High-speed motion analysis")
    print("    - Thermal anomaly detection")
    print("    - Invisible light source detection")
    print("  [AI]")
    print("    - Pattern recognition")
    print("    - Spectral segmentation")
    print("    - Motion blur analysis")
    
    print("\n" + "="*70)
    print("Ready for multimodal analysis!")
    print("="*70 + "\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo_multimodal()
