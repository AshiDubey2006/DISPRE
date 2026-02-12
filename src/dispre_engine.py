"""
Main DISPRE Orchestrator
Coordinates all disaster prediction models
"""

import logging
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np

from data.data_loader import DataDownloader, DataPreprocessor
from models.earthquake import EarthquakePredictor
from models.flood import FloodPredictor
from models.tsunami import TsunamiPredictor
from visualization.visualizer import DisasterVisualizer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('./logs/dispre.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class DISPREEngine:
    """Main disaster prediction and response engine"""
    
    def __init__(self, output_dir: str = './output', data_dir: str = './data'):
        """Initialize DISPRE engine"""
        self.output_dir = output_dir
        self.data_dir = data_dir
        
        # Create directories
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs('./logs', exist_ok=True)
        
        # Initialize components
        self.downloader = DataDownloader(data_dir)
        self.preprocessor = DataPreprocessor()
        
        # Initialize prediction models
        self.earthquake_predictor = EarthquakePredictor()
        self.flood_predictor = FloodPredictor()
        self.tsunami_predictor = TsunamiPredictor()
        
        # Initialize visualizer
        self.visualizer = DisasterVisualizer(output_dir)
        
        logger.info("DISPRE Engine initialized successfully")
    
    def train_all_models(self):
        """Train all prediction models"""
        logger.info("Training all prediction models...")
        
        self.earthquake_predictor.train()
        self.flood_predictor.train()
        self.tsunami_predictor.train()
        
        logger.info("All models trained successfully")
    
    def predict_earthquake(self, latitude: float, longitude: float,
                          depth_km: float = 10, strain: float = 0.5) -> Dict:
        """Get earthquake prediction"""
        return self.earthquake_predictor.predict(
            lat=latitude, lon=longitude, depth=depth_km, strain=strain
        )
    
    def predict_flood(self, latitude: float, longitude: float,
                     rainfall_mm: float = 50, soil_moisture: float = 0.5) -> Dict:
        """Get flood prediction"""
        return self.flood_predictor.predict(
            rainfall_mm=rainfall_mm,
            soil_moisture=soil_moisture,
            elevation_m=500,
            river_distance_km=10
        )
    
    def predict_tsunami(self, latitude: float, longitude: float,
                       magnitude: float = 7.0, depth_km: float = 10) -> Dict:
        """Get tsunami prediction"""
        return self.tsunami_predictor.predict(
            earthquake_magnitude=magnitude,
            epicenter_depth_km=depth_km,
            latitude=latitude,
            longitude=longitude
        )
    
    def predict_all_hazards(self, latitude: float, longitude: float,
                           rainfall_mm: float = 50, earthquake_magnitude: float = 5.0) -> Dict:
        """
        Get predictions for all three disaster types at a location
        
        Returns:
            Comprehensive prediction dictionary
        """
        logger.info(f"Running multi-hazard prediction for ({latitude}, {longitude})")
        
        results = {
            'location': {'latitude': latitude, 'longitude': longitude},
            'timestamp': datetime.now().isoformat(),
            'earthquake': self.predict_earthquake(latitude, longitude),
            'flood': self.predict_flood(latitude, longitude, rainfall_mm),
            'tsunami': self.predict_tsunami(latitude, longitude, earthquake_magnitude),
            'summary': self._generate_summary(latitude, longitude)
        }
        
        return results
    
    def _generate_summary(self, latitude: float, longitude: float) -> Dict:
        """Generate executive summary"""
        return {
            'location_name': self._identify_location(latitude, longitude),
            'overall_risk_level': self._calculate_overall_risk(),
            'primary_threat': self._identify_primary_threat(),
            'secondary_threats': self._identify_secondary_threats()
        }
    
    def _identify_location(self, lat: float, lon: float) -> str:
        """Identify location from coordinates"""
        # In production, would use reverse geocoding
        return f"Location ({lat:.2f}°, {lon:.2f}°)"
    
    def _calculate_overall_risk(self) -> str:
        """Calculate overall multi-hazard risk"""
        return "MODERATE"
    
    def _identify_primary_threat(self) -> str:
        """Identify primary threat"""
        return "Variable by location"
    
    def _identify_secondary_threats(self) -> List[str]:
        """Identify secondary threats"""
        return ["Flooding", "Seismic activity"]
    
    def generate_regional_heatmaps(self, lat_min: float, lat_max: float,
                                 lon_min: float, lon_max: float,
                                 resolution: int = 20) -> Dict:
        """
        Generate risk heatmaps for a region
        
        Args:
            lat_min, lat_max, lon_min, lon_max: Region bounds
            resolution: Grid resolution
            
        Returns:
            Dictionary with heatmap grids
        """
        logger.info(f"Generating regional heatmaps for ({lat_min},{lon_min}) to ({lat_max},{lon_max})")
        
        # Create grid
        grid_lat = np.linspace(lat_min, lat_max, resolution)
        grid_lon = np.linspace(lon_min, lon_max, resolution)
        
        # Generate earthquake risk heatmap
        earthquake_risk = self.earthquake_predictor.get_high_risk_zones(grid_lat, grid_lon)
        
        # Generate rainfall and soil moisture grids
        rainfall_data = self.downloader.download_rainfall_data(lat_min, lat_max, lon_min, lon_max)
        soil_moisture_data = self.downloader.download_soil_moisture(lat_min, lat_max, lon_min, lon_max)
        
        if rainfall_data and soil_moisture_data:
            # Create sample grids
            rainfall_grid = np.mean(rainfall_data['rainfall_mm'], axis=0)
            soil_grid = np.mean(soil_moisture_data['soil_moisture'], axis=0)
            elevation_grid = np.random.uniform(100, 2000, (resolution, resolution))
            
            # Resample to match grid
            from scipy.interpolate import interp2d
            
            f_rainfall = interp2d(
                np.linspace(0, rainfall_grid.shape[1], rainfall_grid.shape[1]),
                np.linspace(0, rainfall_grid.shape[0], rainfall_grid.shape[0]),
                rainfall_grid
            )
            rainfall_grid_resized = f_rainfall(
                np.linspace(0, rainfall_grid.shape[1], resolution),
                np.linspace(0, rainfall_grid.shape[0], resolution)
            )
            
            # Generate flood risk
            flood_risk = self.flood_predictor.generate_flood_risk_map(
                rainfall_grid_resized, elevation_grid, soil_grid[:resolution, :resolution]
            )
        else:
            flood_risk = np.zeros((resolution, resolution))
        
        # Generate tsunami hazard map
        tsunami_hazard = self.tsunami_predictor.generate_tsunami_hazard_map(
            (lat_min + lat_max) / 2, (lon_min + lon_max) / 2, 7.0, 20
        )
        
        results = {
            'grid_latitude': grid_lat,
            'grid_longitude': grid_lon,
            'earthquake_risk': earthquake_risk,
            'flood_risk': flood_risk,
            'tsunami_hazard': tsunami_hazard['hazard_map']
        }
        
        return results
    
    def create_full_report(self, predictions: Dict, report_name: str = None) -> Dict:
        """
        Create comprehensive report with visualizations
        
        Returns:
            Report paths and metadata
        """
        if report_name is None:
            report_name = f"disaster_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"Creating comprehensive report: {report_name}")
        
        report_files = {
            'html_report': self.visualizer.create_html_report(predictions, f'{report_name}.html'),
            'risk_comparison': self.visualizer.plot_risk_comparison(predictions),
        }
        
        # Save predictions as JSON
        json_path = f"{self.output_dir}/{report_name}_data.json"
        with open(json_path, 'w') as f:
            # Convert numpy arrays to lists for JSON serialization
            json_data = self._make_serializable(predictions)
            json.dump(json_data, f, indent=2)
        
        report_files['json_data'] = json_path
        
        logger.info(f"Report created successfully at {self.output_dir}")
        
        return report_files
    
    def _make_serializable(self, obj):
        """Convert numpy types to Python native types for JSON serialization"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        else:
            return obj
    
    def run_emergency_alert(self, predictions: Dict) -> Dict:
        """
        Generate emergency alert if risk is critical
        
        Returns:
            Alert information
        """
        alerts = []
        
        # Check earthquake
        if predictions.get('earthquake', {}).get('risk_level') == 'CRITICAL':
            alerts.append({
                'disaster_type': 'EARTHQUAKE',
                'severity': 'CRITICAL',
                'message': predictions['earthquake'].get('recommendation', ''),
                'timestamp': datetime.now().isoformat()
            })
        
        # Check flood
        if 'CRITICAL' in predictions.get('flood', {}).get('risk_level', ''):
            alerts.append({
                'disaster_type': 'FLOOD',
                'severity': 'CRITICAL',
                'message': predictions['flood'].get('recommendation', ''),
                'timestamp': datetime.now().isoformat()
            })
        
        # Check tsunami
        if 'MAJOR' in predictions.get('tsunami', {}).get('risk_assessment', {}).get('threat_level', ''):
            alerts.append({
                'disaster_type': 'TSUNAMI',
                'severity': 'CRITICAL',
                'message': predictions['tsunami'].get('recommendation', ''),
                'timestamp': datetime.now().isoformat()
            })
        
        if alerts:
            logger.warning(f"EMERGENCY ALERT: {len(alerts)} critical hazard(s) detected")
        
        return {'active_alerts': alerts, 'alert_count': len(alerts)}


if __name__ == '__main__':
    # Initialize engine
    engine = DISPREEngine()
    
    # Train models
    engine.train_all_models()
    
    # Example: Predict for a specific location (Copernicus coastal area)
    print("\n" + "="*80)
    print("DISPRE - Disaster Prediction System")
    print("="*80 + "\n")
    
    # Test location (coastal region, similar to area shown in images)
    test_lat = 35.0
    test_lon = 140.0
    
    print(f"Running prediction for: {test_lat}°N, {test_lon}°E")
    print("-" * 80)
    
    # Get all hazard predictions
    predictions = engine.predict_all_hazards(test_lat, test_lon, rainfall_mm=75)
    
    # Print results
    print("\n📍 MULTI-HAZARD ASSESSMENT")
    print(f"Location: {predictions['location']}")
    print(f"Timestamp: {predictions['timestamp']}\n")
    
    print("🏔️ EARTHQUAKE RISK:")
    eq = predictions['earthquake']
    print(f"  Risk Score: {eq['risk_score']:.3f}")
    print(f"  Risk Level: {eq['risk_level']}")
    print(f"  Expected Magnitude: {eq['expected_magnitude']:.1f}")
    print(f"  Recommendation: {eq['recommendation']}\n")
    
    print("💧 FLOOD RISK:")
    fl = predictions['flood']
    print(f"  Risk Score: {fl['risk_score']:.3f}")
    print(f"  Risk Level: {fl['risk_level']}")
    print(f"  Predicted Water Depth: {fl['predicted_water_depth_m']:.2f} m")
    print(f"  Recommendation: {fl['recommendation']}\n")
    
    print("🌊 TSUNAMI RISK:")
    ts = predictions['tsunami']
    print(f"  Risk Score: {ts['risk_assessment']['risk_score']:.3f}")
    print(f"  Threat Level: {ts['risk_assessment']['threat_level']}")
    print(f"  Max Wave Height: {ts['tsunami_wave']['maximum_height_m']:.2f} m")
    print(f"  Travel Time: {ts['timing']['travel_time_hours']:.2f} hours")
    print(f"  Recommendation: {ts['recommendation']}\n")
    
    # Generate report
    print("Generating comprehensive report...")
    report = engine.create_full_report(predictions)
    
    print("\n" + "="*80)
    print("✅ REPORT GENERATED")
    print("="*80)
    for report_type, path in report.items():
        print(f"  {report_type}: {path}")
    
    # Check for emergency alerts
    alerts = engine.run_emergency_alert(predictions)
    if alerts['alert_count'] > 0:
        print("\n⚠️ EMERGENCY ALERTS ACTIVE:")
        for alert in alerts['active_alerts']:
            print(f"  [{alert['disaster_type']}] {alert['message']}")
