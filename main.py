#!/usr/bin/env python
"""
DISPRE Main Application
Should run this file to execute the disaster prediction system
"""

import sys
import os
import json
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dispre_engine import DISPREEngine
import logging

logger = logging.getLogger(__name__)


def main():
    """Main application entry point"""
    
    print("\n" + "="*90)
    print("  DISPRE - Disaster Prediction and Response Engine v1.0")
    print("  Advanced Hazard Assessment for Earthquake, Flood, and Tsunami")
    print("="*90 + "\n")
    
    # Initialize engine
    print("🚀 Initializing DISPRE Engine...")
    engine = DISPREEngine(output_dir='./output', data_dir='./data')
    print("   ✓ Engine initialized\n")
    
    # Train models
    print("🤖 Training prediction models...")
    engine.train_all_models()
    print("   ✓ All models trained\n")
    
    # Define test locations
    test_locations = [
        {
            'name': 'Pacific Ring of Fire (Japan)',
            'latitude': 35.0,
            'longitude': 140.0,
            'rainfall': 75,
            'magnitude': 7.5
        },
        {
            'name': 'Coastal California',
            'latitude': 36.5,
            'longitude': -120.5,
            'rainfall': 50,
            'magnitude': 6.8
        },
        {
            'name': 'Indian Ocean Region',
            'latitude': -8.5,
            'longitude': 95.0,
            'rainfall': 100,
            'magnitude': 7.0
        },
        {
            'name': 'Himalayan Region',
            'latitude': 28.5,
            'longitude': 84.0,
            'rainfall': 120,
            'magnitude': 6.5
        }
    ]
    
    all_predictions = {}
    
    # Run predictions for all test locations
    print("📊 Running multi-hazard predictions...\n")
    
    for loc in test_locations:
        print(f"  • Analyzing: {loc['name']}")
        print(f"    Coordinates: {loc['latitude']}°, {loc['longitude']}°")
        
        try:
            predictions = engine.predict_all_hazards(
                latitude=loc['latitude'],
                longitude=loc['longitude'],
                rainfall_mm=loc['rainfall'],
                earthquake_magnitude=loc['magnitude'] - 1.5  # Calibrate
            )
            
            all_predictions[loc['name']] = predictions
            
            # Print risk summary
            eq_risk = predictions['earthquake']['risk_level']
            fl_risk = predictions['flood']['risk_level']
            ts_threat = predictions['tsunami']['risk_assessment']['threat_level']
            
            print(f"    Risk Assessment:")
            print(f"      - Earthquake: {eq_risk}")
            print(f"      - Flood: {fl_risk}")
            print(f"      - Tsunami: {ts_threat}")
            
            # Check for critical alerts
            alerts = engine.run_emergency_alert(predictions)
            if alerts['alert_count'] > 0:
                print(f"    ⚠️ CRITICAL ALERTS: {alerts['alert_count']}")
            
            print()
            
        except Exception as e:
            logger.error(f"Error processing {loc['name']}: {e}")
            print(f"    ❌ Error: {str(e)}\n")
    
    # Generate detailed report for primary location
    print("📄 Generating comprehensive report...")
    primary_location = test_locations[0]
    primary_predictions = all_predictions[primary_location['name']]
    
    report_files = engine.create_full_report(
        primary_predictions,
        report_name=f"dispre_report_{primary_location['name'].replace(' ', '_')}"
    )
    
    print("\n✅ DISPRE Execution Complete!\n")
    print("="*90)
    print("Generated Files:")
    for file_type, filepath in report_files.items():
        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath) / 1024  # KB
            print(f"  ✓ {file_type:.<30} {filepath} ({file_size:.1f} KB)")
        else:
            print(f"  ✗ {file_type:.<30} {filepath} (NOT FOUND)")
    
    print("="*90 + "\n")
    
    # Summary statistics
    print("📈 Summary Statistics:")
    print(f"  • Total locations analyzed: {len(all_predictions)}")
    
    critical_count = sum(
        1 for pred in all_predictions.values()
        if any(
            'CRITICAL' in str(pred.get(disaster, {}).get('risk_level', ''))
            or 'CRITICAL' in str(pred.get('tsunami', {}).get('risk_assessment', {}).get('risk_level', ''))
            for disaster in ['earthquake', 'flood']
        )
    )
    
    print(f"  • Critical risk locations: {critical_count}")
    print(f"  • Output directory: ./output")
    print(f"  • Log file: ./logs/dispre.log")
    
    print("\n💡 Next Steps:")
    print("  1. Review the HTML report in ./output/ directory")
    print("  2. Check risk comparison charts")
    print("  3. Examine JSON data for further analysis")
    print("  4. Contact local disaster management for critical alerts")
    
    print("\n" + "="*90 + "\n")


if __name__ == '__main__':
    main()

