"""
Example Scripts for Common Use Cases
Demonstrates practical applications of the Beyond Human Perception Audio Analyzer
"""

import sys
from pathlib import Path
import numpy as np
import soundfile as sf

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import AudioAnalyzer
from src.realtime_monitor import RealtimeMonitor
from src.utils import generate_test_signal, save_audio


def example_1_bat_detection():
    """
    Example 1: Detect bat echolocation calls
    Bats typically use frequencies between 20-100 kHz
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 1: BAT ECHOLOCATION DETECTION")
    print("=" * 70)
    
    analyzer = AudioAnalyzer()
    
    # Generate synthetic bat call (simplified)
    # Real bat calls are more complex with frequency modulation
    duration = 0.5  # 500ms
    sample_rate = 192000  # High sample rate for ultrasound
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Simulate FM bat call (chirp from 80kHz to 40kHz)
    f0 = 80000  # Starting frequency
    f1 = 40000  # Ending frequency
    chirp = np.sin(2 * np.pi * (f0 * t + (f1 - f0) / (2 * duration) * t**2))
    
    # Add some noise
    noise = 0.1 * np.random.randn(len(t))
    bat_signal = 0.8 * chirp + noise
    
    # Save and analyze
    test_file = '/home/claude/data/samples/bat_call_synthetic.wav'
    save_audio(bat_signal, sample_rate, test_file)
    
    print(f"\nGenerated synthetic bat call: {test_file}")
    print("Analyzing for ultrasound...")
    
    analyzer.sample_rate = sample_rate
    results = analyzer.analyze_full_spectrum(test_file, mode='ultrasound')
    
    print(f"\nResults:")
    print(f"Total ultrasound events: {results['total_events']}")
    
    for event in results['events']:
        print(f"  - {event['frequency_hz']/1000:.1f} kHz @ {event['magnitude_db']:.1f} dB")
    
    # Visualize
    audio, sr = analyzer.load_audio(test_file, target_sr=sample_rate)
    analyzer.visualize_spectrogram(
        audio,
        title="Bat Echolocation Call - Spectrogram",
        freq_range=(20000, 100000),
        save_path='/home/claude/data/samples/bat_spectrogram.png'
    )


def example_2_machinery_monitoring():
    """
    Example 2: Monitor industrial machinery for infrasound
    Low-frequency vibrations can indicate wear or malfunction
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: INDUSTRIAL MACHINERY MONITORING")
    print("=" * 70)
    
    analyzer = AudioAnalyzer()
    
    # Generate synthetic machinery signal
    duration = 10  # 10 seconds
    sample_rate = 48000
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Normal operation: steady 12 Hz vibration
    normal_freq = 12
    normal_signal = 0.3 * np.sin(2 * np.pi * normal_freq * t)
    
    # Add abnormal 3 Hz vibration (simulating bearing wear)
    abnormal_freq = 3
    abnormal_signal = 0.5 * np.sin(2 * np.pi * abnormal_freq * t)
    
    # Combine
    machinery_signal = normal_signal + abnormal_signal + 0.05 * np.random.randn(len(t))
    
    # Save and analyze
    test_file = '/home/claude/data/samples/machinery_vibration.wav'
    save_audio(machinery_signal, sample_rate, test_file)
    
    print(f"\nGenerated machinery signal: {test_file}")
    print("Analyzing for infrasound...")
    
    results = analyzer.analyze_full_spectrum(test_file, mode='infrasound')
    
    print(f"\nResults:")
    print(f"Total infrasound events: {results['total_events']}")
    
    # Check for abnormal frequencies
    for event in results['events']:
        freq = event['frequency_hz']
        mag = event['magnitude_db']
        
        if freq < 5:
            status = "⚠️  WARNING: Abnormal low-frequency vibration"
        else:
            status = "✓ Normal operation frequency"
        
        print(f"  - {freq:.2f} Hz @ {mag:.1f} dB - {status}")


def example_3_rodent_detection():
    """
    Example 3: Detect rodent ultrasonic vocalizations
    Mice and rats communicate in 20-90 kHz range
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: RODENT VOCALIZATION DETECTION")
    print("=" * 70)
    
    analyzer = AudioAnalyzer()
    
    # Generate synthetic rodent vocalization
    duration = 0.3  # 300ms
    sample_rate = 192000
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Typical mouse call around 50-70 kHz
    rodent_freq = 60000
    rodent_call = 0.6 * np.sin(2 * np.pi * rodent_freq * t)
    
    # Add frequency modulation (mice calls are often modulated)
    modulation = 0.1 * np.sin(2 * np.pi * 500 * t)
    rodent_call = rodent_call * (1 + modulation)
    
    # Add noise
    noise = 0.15 * np.random.randn(len(t))
    rodent_signal = rodent_call + noise
    
    # Save and analyze
    test_file = '/home/claude/data/samples/rodent_vocalization.wav'
    save_audio(rodent_signal, sample_rate, test_file)
    
    print(f"\nGenerated rodent vocalization: {test_file}")
    print("Analyzing for ultrasound...")
    
    analyzer.sample_rate = sample_rate
    results = analyzer.analyze_full_spectrum(test_file, mode='ultrasound')
    
    print(f"\nResults:")
    print(f"Total ultrasound events: {results['total_events']}")
    
    for event in results['events']:
        freq_khz = event['frequency_hz'] / 1000
        
        # Classify based on frequency
        if 50 <= freq_khz <= 70:
            species = "Possible mouse vocalization"
        elif 20 <= freq_khz <= 40:
            species = "Possible rat vocalization"
        else:
            species = "Unknown ultrasound source"
        
        print(f"  - {freq_khz:.1f} kHz @ {event['magnitude_db']:.1f} dB")
        print(f"    Classification: {species}")


def example_4_realtime_callback():
    """
    Example 4: Real-time monitoring with custom callback
    Demonstrates alert system for high-intensity events
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: REAL-TIME MONITORING WITH ALERTS")
    print("=" * 70)
    
    # Track detected events
    event_log = []
    
    def alert_callback(event):
        """Custom callback for high-priority events"""
        event_log.append(event)
        
        # Alert on high-intensity events
        if event['magnitude_db'] > -30:
            print(f"\n🚨 HIGH INTENSITY ALERT:")
            print(f"   Type: {event['type'].upper()}")
            print(f"   Frequency: {event['frequency_hz']:.2f} Hz")
            print(f"   Magnitude: {event['magnitude_db']:.1f} dB")
            print(f"   Time: {event['timestamp'].strftime('%H:%M:%S')}")
    
    print("\nThis example requires a working microphone.")
    print("To run this example, uncomment the code below and ensure")
    print("your audio interface is properly configured.\n")
    
    # Uncomment to run with actual hardware:
    """
    monitor = RealtimeMonitor()
    monitor.register_callback(alert_callback)
    
    print("Starting real-time monitoring for 30 seconds...")
    print("Make some high-frequency sounds (keys jingling, etc.)")
    
    try:
        monitor.start(duration=30)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your audio interface supports high sample rates")
    
    # Print summary
    print(f"\nDetected {len(event_log)} events total")
    """


def example_5_batch_analysis():
    """
    Example 5: Batch process multiple files
    Useful for analyzing recordings from field deployments
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 5: BATCH PROCESSING")
    print("=" * 70)
    
    from src.batch_processor import BatchProcessor
    
    # Create some test files first
    analyzer = AudioAnalyzer()
    sample_dir = Path('/home/claude/data/samples')
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nGenerating test audio files...")
    
    # Generate 3 test files with different characteristics
    test_files = [
        ('infrasound_test.wav', 5, 'infrasound'),
        ('ultrasound_test.wav', 25000, 'ultrasound'),
        ('mixed_test.wav', None, 'both')
    ]
    
    for filename, freq, signal_type in test_files:
        duration = 2
        sample_rate = 96000
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        if signal_type == 'both':
            # Mixed signal
            signal = (0.4 * np.sin(2 * np.pi * 8 * t) + 
                     0.3 * np.sin(2 * np.pi * 30000 * t))
        else:
            signal = 0.5 * np.sin(2 * np.pi * freq * t)
        
        signal += 0.05 * np.random.randn(len(t))
        
        filepath = sample_dir / filename
        save_audio(signal, sample_rate, str(filepath))
        print(f"  Created: {filename}")
    
    # Process batch
    print("\nProcessing batch...")
    processor = BatchProcessor()
    
    results_dir = '/home/claude/data/samples/batch_results'
    processor.process_directory(
        str(sample_dir),
        results_dir,
        mode='full'
    )
    
    # Display statistics
    stats = processor.get_statistics()
    print("\nBatch Processing Results:")
    print(f"  Files processed: {stats['total_files']}")
    print(f"  Total events: {stats['total_events']}")
    print(f"  Infrasound events: {stats['infrasound_events']}")
    print(f"  Ultrasound events: {stats['ultrasound_events']}")
    print(f"\nReports saved to: {results_dir}")


def main():
    """Run all examples"""
    print("\n")
    print("=" * 70)
    print("BEYOND HUMAN PERCEPTION AUDIO ANALYZER")
    print("Example Use Cases")
    print("=" * 70)
    
    examples = [
        ("Bat Detection", example_1_bat_detection),
        ("Machinery Monitoring", example_2_machinery_monitoring),
        ("Rodent Detection", example_3_rodent_detection),
        ("Real-time Alerts", example_4_realtime_callback),
        ("Batch Processing", example_5_batch_analysis)
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nSelect example (1-5) or 'all' to run all examples:")
    choice = input("> ").strip().lower()
    
    if choice == 'all':
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"\nError in {name}: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        idx = int(choice) - 1
        try:
            examples[idx][1]()
        except Exception as e:
            print(f"\nError: {e}")
    else:
        print("Invalid choice")
    
    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
