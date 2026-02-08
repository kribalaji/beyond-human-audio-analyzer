"""
Real-time Audio Monitoring for Beyond Human Perception Detection
Continuous monitoring and alert system for infrasound and ultrasound
"""

import numpy as np
import sounddevice as sd
import queue
import threading
import logging
from typing import Optional, Callable, Dict, List
from datetime import datetime
import yaml
from scipy import signal
import time


class RealtimeMonitor:
    """
    Real-time audio monitoring system for detecting sounds beyond human hearing range.
    """
    
    def __init__(self, config_path: str = 'config/config.yaml'):
        """
        Initialize the real-time monitor.
        
        Args:
            config_path: Path to configuration YAML file
        """
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        
        self.sample_rate = self.config['audio']['sample_rate']
        self.buffer_size = self.config['audio']['buffer_size']
        self.channels = self.config['audio']['channels']
        
        self.audio_queue = queue.Queue()
        self.is_monitoring = False
        self.monitor_thread = None
        
        self.event_callbacks = []
        self.detected_events = []
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Return default configuration."""
        return {
            'audio': {
                'sample_rate': 96000,
                'buffer_size': 2048,
                'channels': 1
            },
            'frequency_ranges': {
                'infrasound': {'min': 0.01, 'max': 20},
                'ultrasound': {'min': 20000, 'max': 48000}
            },
            'detection': {
                'infrasound': {'threshold_db': -40},
                'ultrasound': {'threshold_db': -50}
            },
            'realtime': {
                'display_interval': 0.1,
                'alerts_enabled': True
            }
        }
    
    def list_audio_devices(self):
        """List available audio input devices."""
        print("\nAvailable Audio Devices:")
        print("=" * 60)
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                print(f"[{i}] {device['name']}")
                print(f"    Channels: {device['max_input_channels']}, "
                      f"Sample Rate: {device['default_samplerate']} Hz")
        print("=" * 60)
    
    def _audio_callback(self, indata, frames, time_info, status):
        """
        Callback function for audio stream.
        
        Args:
            indata: Input audio data
            frames: Number of frames
            time_info: Timing information
            status: Status flags
        """
        if status:
            self.logger.warning(f"Audio callback status: {status}")
        
        # Add audio data to queue for processing
        self.audio_queue.put(indata.copy())
    
    def _process_audio_buffer(self, audio_buffer: np.ndarray) -> List[Dict]:
        """
        Process audio buffer and detect events.
        
        Args:
            audio_buffer: Audio data buffer
            
        Returns:
            List of detected events
        """
        events = []
        
        # Flatten if multi-channel
        if audio_buffer.ndim > 1:
            audio_buffer = audio_buffer.mean(axis=1)
        
        # Compute FFT
        N = len(audio_buffer)
        fft_vals = np.fft.fft(audio_buffer)
        fft_freq = np.fft.fftfreq(N, 1/self.sample_rate)
        
        # Take positive frequencies
        positive_freq_idx = fft_freq > 0
        frequencies = fft_freq[positive_freq_idx]
        magnitudes = np.abs(fft_vals[positive_freq_idx])
        magnitudes_db = 20 * np.log10(magnitudes + 1e-10)
        
        # Check infrasound range
        infra_config = self.config['frequency_ranges']['infrasound']
        infra_threshold = self.config['detection']['infrasound']['threshold_db']
        
        infra_mask = (frequencies >= infra_config['min']) & (frequencies <= infra_config['max'])
        if np.any(infra_mask):
            infra_magnitudes = magnitudes_db[infra_mask]
            infra_frequencies = frequencies[infra_mask]
            
            max_idx = np.argmax(infra_magnitudes)
            if infra_magnitudes[max_idx] > infra_threshold:
                event = {
                    'type': 'infrasound',
                    'frequency_hz': infra_frequencies[max_idx],
                    'magnitude_db': infra_magnitudes[max_idx],
                    'timestamp': datetime.now()
                }
                events.append(event)
        
        # Check ultrasound range
        ultra_config = self.config['frequency_ranges']['ultrasound']
        ultra_threshold = self.config['detection']['ultrasound']['threshold_db']
        
        ultra_mask = (frequencies >= ultra_config['min']) & (frequencies <= ultra_config['max'])
        if np.any(ultra_mask):
            ultra_magnitudes = magnitudes_db[ultra_mask]
            ultra_frequencies = frequencies[ultra_mask]
            
            max_idx = np.argmax(ultra_magnitudes)
            if ultra_magnitudes[max_idx] > ultra_threshold:
                event = {
                    'type': 'ultrasound',
                    'frequency_hz': ultra_frequencies[max_idx],
                    'magnitude_db': ultra_magnitudes[max_idx],
                    'timestamp': datetime.now()
                }
                events.append(event)
        
        return events
    
    def _monitor_loop(self):
        """Main monitoring loop running in separate thread."""
        self.logger.info("Monitoring loop started")
        
        accumulated_audio = np.array([])
        process_interval = self.config['realtime']['display_interval']
        samples_per_interval = int(self.sample_rate * process_interval)
        
        while self.is_monitoring:
            try:
                # Get audio data from queue (with timeout)
                audio_chunk = self.audio_queue.get(timeout=1.0)
                
                # Accumulate audio
                accumulated_audio = np.concatenate([accumulated_audio, audio_chunk.flatten()])
                
                # Process when we have enough samples
                if len(accumulated_audio) >= samples_per_interval:
                    # Process the audio buffer
                    events = self._process_audio_buffer(accumulated_audio[:samples_per_interval])
                    
                    # Handle detected events
                    if events:
                        for event in events:
                            self.detected_events.append(event)
                            
                            # Call registered callbacks
                            for callback in self.event_callbacks:
                                try:
                                    callback(event)
                                except Exception as e:
                                    self.logger.error(f"Error in event callback: {e}")
                            
                            # Console output
                            timestamp_str = event['timestamp'].strftime('%H:%M:%S.%f')[:-3]
                            print(f"[{timestamp_str}] {event['type'].upper()}: "
                                  f"{event['frequency_hz']:.2f} Hz @ {event['magnitude_db']:.1f} dB")
                    
                    # Remove processed samples
                    accumulated_audio = accumulated_audio[samples_per_interval:]
                
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
        
        self.logger.info("Monitoring loop stopped")
    
    def register_callback(self, callback: Callable[[Dict], None]):
        """
        Register a callback function to be called when events are detected.
        
        Args:
            callback: Function that takes event dictionary as parameter
        """
        self.event_callbacks.append(callback)
        self.logger.info(f"Registered callback: {callback.__name__}")
    
    def start(self, device: Optional[int] = None, 
             duration: Optional[float] = None,
             callback: Optional[Callable[[Dict], None]] = None):
        """
        Start real-time monitoring.
        
        Args:
            device: Audio device index (None for default)
            duration: Monitoring duration in seconds (None for indefinite)
            callback: Optional callback function for detected events
        """
        if self.is_monitoring:
            self.logger.warning("Monitoring already active")
            return
        
        if callback:
            self.register_callback(callback)
        
        self.is_monitoring = True
        self.detected_events = []
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # Start audio stream
        try:
            self.logger.info(f"Starting audio stream (sample rate: {self.sample_rate} Hz)")
            
            with sd.InputStream(
                device=device,
                channels=self.channels,
                samplerate=self.sample_rate,
                blocksize=self.buffer_size,
                callback=self._audio_callback
            ):
                print("\n" + "=" * 60)
                print("REAL-TIME MONITORING ACTIVE")
                print("=" * 60)
                print(f"Sample Rate: {self.sample_rate} Hz")
                print(f"Nyquist Frequency: {self.sample_rate / 2} Hz")
                print(f"Monitoring: Infrasound (<20Hz) and Ultrasound (>20kHz)")
                print("Press Ctrl+C to stop")
                print("=" * 60 + "\n")
                
                if duration:
                    print(f"Monitoring for {duration} seconds...")
                    time.sleep(duration)
                else:
                    print("Monitoring indefinitely...")
                    while self.is_monitoring:
                        time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n\nMonitoring interrupted by user")
        except Exception as e:
            self.logger.error(f"Error in audio stream: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop real-time monitoring."""
        if not self.is_monitoring:
            return
        
        self.logger.info("Stopping monitoring...")
        self.is_monitoring = False
        
        # Wait for monitoring thread to finish
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2.0)
        
        print("\n" + "=" * 60)
        print("MONITORING STOPPED")
        print("=" * 60)
        print(f"Total events detected: {len(self.detected_events)}")
        
        # Summary statistics
        if self.detected_events:
            infrasound_events = [e for e in self.detected_events if e['type'] == 'infrasound']
            ultrasound_events = [e for e in self.detected_events if e['type'] == 'ultrasound']
            
            print(f"  Infrasound events: {len(infrasound_events)}")
            print(f"  Ultrasound events: {len(ultrasound_events)}")
        
        print("=" * 60 + "\n")
    
    def get_detected_events(self) -> List[Dict]:
        """
        Get list of all detected events.
        
        Returns:
            List of event dictionaries
        """
        return self.detected_events.copy()
    
    def clear_events(self):
        """Clear the detected events list."""
        self.detected_events.clear()
        self.logger.info("Cleared detected events")


def example_callback(event: Dict):
    """Example callback function for handling detected events."""
    if event['magnitude_db'] > -30:
        print(f"  >>> HIGH INTENSITY EVENT: {event['frequency_hz']:.2f} Hz")


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create monitor
    monitor = RealtimeMonitor()
    
    # List available devices
    monitor.list_audio_devices()
    
    # Register callback
    monitor.register_callback(example_callback)
    
    # Start monitoring
    print("\nStarting real-time monitoring...")
    print("Note: Ensure your audio interface supports high sample rates!")
    
    try:
        monitor.start(duration=30)  # Monitor for 30 seconds
    except KeyboardInterrupt:
        print("\nExiting...")
    
    # Get summary
    events = monitor.get_detected_events()
    if events:
        print(f"\nSummary: Detected {len(events)} total events")
