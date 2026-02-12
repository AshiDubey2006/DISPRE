"""
Earthquake Prediction Model
Predicts earthquake risk based on seismic and climate data
"""

import logging
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple, List
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class EarthquakePredictor:
    """Earthquake prediction model"""
    
    def __init__(self):
        """Initialize earthquake predictor"""
        self.model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
        # Tectonic zones (lat, lon, depth_range_km)
        self.tectonic_zones = {
            'ring_of_fire': {
                'regions': [
                    {'name': 'Pacific Northwest', 'lat': (45, 50), 'lon': (-125, -120), 'risk': 0.8},
                    {'name': 'California', 'lat': (32, 42), 'lon': (-125, -114), 'risk': 0.85},
                    {'name': 'Mexico', 'lat': (14, 20), 'lon': (-105, -95), 'risk': 0.75},
                    {'name': 'Japan', 'lat': (30, 45), 'lon': (130, 145), 'risk': 0.9},
                    {'name': 'Philippines', 'lat': (5, 20), 'lon': (120, 135), 'risk': 0.8},
                ]
            },
            'alpine_belt': {
                'regions': [
                    {'name': 'Mediterranean', 'lat': (30, 45), 'lon': (-10, 45), 'risk': 0.7},
                    {'name': 'India-Himalayas', 'lat': (24, 35), 'lon': (68, 95), 'risk': 0.75},
                    {'name': 'Central Asia', 'lat': (35, 50), 'lon': (65, 100), 'risk': 0.7},
                ]
            }
        }
    
    def generate_synthetic_training_data(self, n_samples: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic earthquake training data"""
        logger.info(f"Generating {n_samples} synthetic earthquake training samples")
        
        X = []
        y = []
        
        for _ in range(n_samples):
            # Features: latitude, longitude, depth, days_since_last_quake, 
            # crustal_strain, tectonic_plate_motion, temperature, pressure
            lat = np.random.uniform(-60, 60)
            lon = np.random.uniform(-180, 180)
            depth = np.random.exponential(15)
            days_since = np.random.exponential(30)
            strain = np.random.uniform(0, 1)
            plate_motion = np.random.uniform(0, 10)  # cm/year
            temp = np.random.normal(25, 10)
            pressure = np.random.uniform(800, 1013)
            
            # Create risk score based on features
            tectonic_risk = self._calculate_tectonic_risk(lat, lon)
            strain_factor = strain * 0.3
            depth_factor = (1 - np.exp(-depth/50)) * 0.2
            plate_factor = (plate_motion / 10) * 0.3
            
            risk = tectonic_risk * 0.2 + strain_factor + depth_factor + plate_factor
            risk = np.clip(risk, 0, 1)
            
            X.append([lat, lon, depth, days_since, strain, plate_motion, temp, pressure])
            y.append(risk)
        
        return np.array(X), np.array(y)
    
    def _calculate_tectonic_risk(self, lat: float, lon: float) -> float:
        """Calculate base tectonic risk for a location"""
        max_risk = 0.1
        
        for zone_type, zone_data in self.tectonic_zones.items():
            for region in zone_data['regions']:
                lat_range = region['lat']
                lon_range = region['lon']
                
                if lat_range[0] <= lat <= lat_range[1] and lon_range[0] <= lon <= lon_range[1]:
                    max_risk = max(max_risk, region['risk'])
        
        return max_risk
    
    def train(self, X: np.ndarray = None, y: np.ndarray = None):
        """Train the earthquake prediction model"""
        if X is None or y is None:
            X, y = self.generate_synthetic_training_data()
        
        logger.info(f"Training earthquake model with {X.shape[0]} samples")
        
        self.feature_names = [
            'latitude', 'longitude', 'depth_km', 'days_since_last_quake',
            'crustal_strain', 'plate_motion_cm_yr', 'temperature_c', 'pressure_mb'
        ]
        
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        logger.info("Earthquake model trained successfully")
    
    def predict(self, lat: float, lon: float, depth: float = 10, 
                days_since_quake: float = 30, strain: float = 0.5,
                plate_motion: float = 5, temp: float = 25, pressure: float = 1013) -> Dict:
        """
        Predict earthquake risk for a location
        
        Returns:
            Dictionary with prediction results
        """
        if not self.is_trained:
            self.train()
        
        # Prepare features
        X = np.array([[lat, lon, depth, days_since_quake, strain, plate_motion, temp, pressure]])
        X_scaled = self.scaler.transform(X)
        
        risk_score = self.model.predict(X_scaled)[0]
        
        # Calculate predicted magnitude distribution
        depth_factor = np.clip(depth / 50, 0, 1)
        strain_factor = strain
        mag_base = 4.5 + depth_factor * 2 + strain_factor * 2
        
        return {
            'location': {'latitude': lat, 'longitude': lon},
            'depth_km': depth,
            'risk_score': float(risk_score),
            'risk_level': self._classify_risk(risk_score),
            'predicted_magnitude_range': (
                max(2.0, mag_base - 1.5),
                min(9.0, mag_base + 1.5)
            ),
            'expected_magnitude': float(mag_base),
            'probability_magnitude_gt_5': float(strain_factor * 0.8),
            'probability_magnitude_gt_7': float(strain_factor * 0.3),
            'tectonic_zone': self._identify_tectonic_zone(lat, lon),
            'recommendation': self._get_recommendation(risk_score),
            'timestamp': datetime.now().isoformat()
        }
    
    def _classify_risk(self, score: float) -> str:
        """Classify risk level"""
        if score < 0.2:
            return 'LOW'
        elif score < 0.4:
            return 'MODERATE'
        elif score < 0.6:
            return 'ELEVATED'
        elif score < 0.8:
            return 'HIGH'
        else:
            return 'CRITICAL'
    
    def _identify_tectonic_zone(self, lat: float, lon: float) -> str:
        """Identify which tectonic zone a location is in"""
        for zone_type, zone_data in self.tectonic_zones.items():
            for region in zone_data['regions']:
                lat_range = region['lat']
                lon_range = region['lon']
                
                if lat_range[0] <= lat <= lat_range[1] and lon_range[0] <= lon <= lon_range[1]:
                    return f"{region['name']} ({zone_type})"
        
        return "Non-active zone"
    
    def _get_recommendation(self, risk_score: float) -> str:
        """Get recommendations based on risk score"""
        if risk_score < 0.2:
            return "Continue routine monitoring"
        elif risk_score < 0.4:
            return "Increase monitoring frequency"
        elif risk_score < 0.6:
            return "Enhanced monitoring and public awareness"
        elif risk_score < 0.8:
            return "High alert status - prepare emergency response"
        else:
            return "CRITICAL - Activate emergency protocols immediately"
    
    def predict_batch(self, locations: List[Dict]) -> List[Dict]:
        """Predict for multiple locations"""
        results = []
        
        for loc in locations:
            result = self.predict(
                lat=loc.get('latitude', 0),
                lon=loc.get('longitude', 0),
                depth=loc.get('depth_km', 10),
                days_since_quake=loc.get('days_since_quake', 30),
                strain=loc.get('strain', 0.5),
                plate_motion=loc.get('plate_motion', 5),
                temp=loc.get('temperature', 25),
                pressure=loc.get('pressure', 1013)
            )
            results.append(result)
        
        return results
    
    def get_high_risk_zones(self, grid_lat: np.ndarray, grid_lon: np.ndarray) -> np.ndarray:
        """
        Generate risk heatmap for a region
        
        Args:
            grid_lat: 1D latitude array
            grid_lon: 1D longitude array
            
        Returns:
            2D risk score array
        """
        if not self.is_trained:
            self.train()
        
        risk_grid = np.zeros((len(grid_lat), len(grid_lon)))
        
        for i, lat in enumerate(grid_lat):
            for j, lon in enumerate(grid_lon):
                X = np.array([[lat, lon, 15, 30, 0.5, 5, 25, 1013]])
                X_scaled = self.scaler.transform(X)
                risk_grid[i, j] = self.model.predict(X_scaled)[0]
        
        return risk_grid
