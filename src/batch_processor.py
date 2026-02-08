"""
Batch Audio Processor
Process multiple audio files and generate comprehensive reports
"""

import os
import sys
from pathlib import Path
import json
import csv
import logging
from typing import List, Dict
from datetime import datetime
import argparse
from tqdm import tqdm

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import AudioAnalyzer


class BatchProcessor:
    """
    Batch processing system for analyzing multiple audio files.
    """
    
    def __init__(self, config_path: str = 'config/config.yaml'):
        """
        Initialize batch processor.
        
        Args:
            config_path: Path to configuration file
        """
        self.logger = logging.getLogger(__name__)
        self.analyzer = AudioAnalyzer(config_path)
        self.results = []
        
    def process_file(self, file_path: str, mode: str = 'full') -> Dict:
        """
        Process a single audio file.
        
        Args:
            file_path: Path to audio file
            mode: Analysis mode ('infrasound', 'ultrasound', 'full')
            
        Returns:
            Analysis results dictionary
        """
        try:
            self.logger.info(f"Processing: {file_path}")
            result = self.analyzer.analyze_full_spectrum(file_path, mode=mode)
            result['status'] = 'success'
            result['error'] = None
            return result
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {e}")
            return {
                'file': Path(file_path).name,
                'status': 'error',
                'error': str(e),
                'events': [],
                'total_events': 0
            }
    
    def process_directory(self, input_dir: str, 
                         output_dir: str,
                         mode: str = 'full',
                         file_extensions: List[str] = None) -> List[Dict]:
        """
        Process all audio files in a directory.
        
        Args:
            input_dir: Input directory path
            output_dir: Output directory for results
            mode: Analysis mode
            file_extensions: List of file extensions to process
            
        Returns:
            List of results for all files
        """
        if file_extensions is None:
            file_extensions = ['.wav', '.mp3', '.flac', '.ogg', '.m4a']
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Find all audio files
        input_path = Path(input_dir)
        audio_files = []
        for ext in file_extensions:
            audio_files.extend(input_path.glob(f"*{ext}"))
            audio_files.extend(input_path.glob(f"*{ext.upper()}"))
        
        if not audio_files:
            self.logger.warning(f"No audio files found in {input_dir}")
            return []
        
        self.logger.info(f"Found {len(audio_files)} audio files to process")
        
        # Process each file
        self.results = []
        for file_path in tqdm(audio_files, desc="Processing files"):
            result = self.process_file(str(file_path), mode=mode)
            self.results.append(result)
        
        # Generate reports
        self._generate_reports(output_dir)
        
        return self.results
    
    def _generate_reports(self, output_dir: str):
        """
        Generate analysis reports in multiple formats.
        
        Args:
            output_dir: Output directory for reports
        """
        output_path = Path(output_dir)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Generate JSON report
        json_file = output_path / f"analysis_report_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        self.logger.info(f"JSON report saved to: {json_file}")
        
        # Generate CSV report
        csv_file = output_path / f"analysis_report_{timestamp}.csv"
        self._generate_csv_report(csv_file)
        
        # Generate summary report
        summary_file = output_path / f"analysis_summary_{timestamp}.txt"
        self._generate_summary_report(summary_file)
    
    def _generate_csv_report(self, output_file: str):
        """
        Generate CSV report with all detected events.
        
        Args:
            output_file: Output CSV file path
        """
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'File',
                'Status',
                'Duration (s)',
                'Sample Rate',
                'Total Events',
                'Event Type',
                'Frequency (Hz)',
                'Magnitude (dB)'
            ])
            
            # Write data
            for result in self.results:
                if result['events']:
                    for event in result['events']:
                        writer.writerow([
                            result['file'],
                            result['status'],
                            result.get('duration_seconds', 'N/A'),
                            result.get('sample_rate', 'N/A'),
                            result['total_events'],
                            event['type'],
                            f"{event['frequency_hz']:.2f}",
                            f"{event['magnitude_db']:.1f}"
                        ])
                else:
                    writer.writerow([
                        result['file'],
                        result['status'],
                        result.get('duration_seconds', 'N/A'),
                        result.get('sample_rate', 'N/A'),
                        0,
                        'None',
                        'N/A',
                        'N/A'
                    ])
        
        self.logger.info(f"CSV report saved to: {output_file}")
    
    def _generate_summary_report(self, output_file: str):
        """
        Generate text summary report.
        
        Args:
            output_file: Output text file path
        """
        with open(output_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("AUDIO ANALYSIS SUMMARY REPORT\n")
            f.write("Beyond Human Perception Detection\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall statistics
            total_files = len(self.results)
            successful = sum(1 for r in self.results if r['status'] == 'success')
            failed = total_files - successful
            
            total_events = sum(r['total_events'] for r in self.results)
            infrasound_events = sum(
                len([e for e in r['events'] if e['type'] == 'infrasound'])
                for r in self.results
            )
            ultrasound_events = sum(
                len([e for e in r['events'] if e['type'] == 'ultrasound'])
                for r in self.results
            )
            
            f.write("OVERALL STATISTICS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total files processed: {total_files}\n")
            f.write(f"  Successful: {successful}\n")
            f.write(f"  Failed: {failed}\n\n")
            
            f.write(f"Total events detected: {total_events}\n")
            f.write(f"  Infrasound events (<20Hz): {infrasound_events}\n")
            f.write(f"  Ultrasound events (>20kHz): {ultrasound_events}\n\n")
            
            # Per-file results
            f.write("\nPER-FILE RESULTS\n")
            f.write("-" * 70 + "\n\n")
            
            for result in self.results:
                f.write(f"File: {result['file']}\n")
                f.write(f"  Status: {result['status']}\n")
                
                if result['status'] == 'success':
                    f.write(f"  Duration: {result.get('duration_seconds', 'N/A'):.2f} seconds\n")
                    f.write(f"  Sample Rate: {result.get('sample_rate', 'N/A')} Hz\n")
                    f.write(f"  Events detected: {result['total_events']}\n")
                    
                    if result['events']:
                        f.write("  Events:\n")
                        for event in result['events']:
                            f.write(f"    - {event['type'].upper()}: "
                                  f"{event['frequency_hz']:.2f} Hz @ "
                                  f"{event['magnitude_db']:.1f} dB\n")
                else:
                    f.write(f"  Error: {result.get('error', 'Unknown error')}\n")
                
                f.write("\n")
            
            f.write("=" * 70 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 70 + "\n")
        
        self.logger.info(f"Summary report saved to: {output_file}")
    
    def get_statistics(self) -> Dict:
        """
        Get processing statistics.
        
        Returns:
            Dictionary with statistics
        """
        if not self.results:
            return {}
        
        total_events = sum(r['total_events'] for r in self.results)
        infrasound_count = sum(
            len([e for e in r['events'] if e['type'] == 'infrasound'])
            for r in self.results
        )
        ultrasound_count = sum(
            len([e for e in r['events'] if e['type'] == 'ultrasound'])
            for r in self.results
        )
        
        return {
            'total_files': len(self.results),
            'successful_files': sum(1 for r in self.results if r['status'] == 'success'),
            'failed_files': sum(1 for r in self.results if r['status'] == 'error'),
            'total_events': total_events,
            'infrasound_events': infrasound_count,
            'ultrasound_events': ultrasound_count
        }


def main():
    """Main entry point for batch processor."""
    parser = argparse.ArgumentParser(
        description='Batch process audio files for beyond human perception detection'
    )
    parser.add_argument(
        '--input-dir',
        required=True,
        help='Input directory containing audio files'
    )
    parser.add_argument(
        '--output-dir',
        required=True,
        help='Output directory for results'
    )
    parser.add_argument(
        '--mode',
        choices=['infrasound', 'ultrasound', 'full'],
        default='full',
        help='Analysis mode (default: full)'
    )
    parser.add_argument(
        '--config',
        default='config/config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--extensions',
        nargs='+',
        default=['.wav', '.mp3', '.flac'],
        help='File extensions to process (default: .wav .mp3 .flac)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create processor
    processor = BatchProcessor(args.config)
    
    # Process directory
    print("\n" + "=" * 70)
    print("BATCH AUDIO PROCESSOR")
    print("Beyond Human Perception Detection")
    print("=" * 70)
    print(f"Input directory: {args.input_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Analysis mode: {args.mode}")
    print("=" * 70 + "\n")
    
    results = processor.process_directory(
        args.input_dir,
        args.output_dir,
        mode=args.mode,
        file_extensions=args.extensions
    )
    
    # Print statistics
    stats = processor.get_statistics()
    print("\n" + "=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)
    print(f"Files processed: {stats['total_files']}")
    print(f"  Successful: {stats['successful_files']}")
    print(f"  Failed: {stats['failed_files']}")
    print(f"\nTotal events detected: {stats['total_events']}")
    print(f"  Infrasound: {stats['infrasound_events']}")
    print(f"  Ultrasound: {stats['ultrasound_events']}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
