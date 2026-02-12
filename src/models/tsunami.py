"""
Tsunami Prediction Model
Predicts tsunami risk based on earthquakes, sea surface conditions, and coastal topography
"""

import logging
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple, List
from datetime import datetime, timedelta
import math

logger = logging.getLogger(__name__)


class TsunamiPredictor:
    """Tsunami prediction model"""
    
    def __init__(self):
        """Initialize tsunami predictor"""
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
        # Subduction zones with high tsunami potential
        self.tsunami_source_zones = [
            {'name': 'Cascadia', 'lat': (43, 49), 'lon': (-126, -123), 'max_mag': 9.0},
            {'name': 'Japan Trench', 'lat': (30, 45), 'lon': (140, 145), 'max_mag': 9.2},
            {'name': 'Kuril-Kamchatka', 'lat': (45, 60), 'lon': (150, 160), 'max_mag': 8.8},
            {'name': 'Indian Ocean', 'lat': (-10, 5), 'lon': (90, 100), 'max_mag': 9.0},
            {'name': 'Peru-Chile', 'lat': (-50, -10), 'lon': (-80, -70), 'max_mag': 9.5},
        ]
        
        # Vulnerable coastal areas
        self.vulnerable_coastlines = [
            {'name': 'Japanese Coast', 'lat': (30, 45), 'lon': (130, 145), 'vulnerability': 0.9},
            {'name': 'Indian Ocean Rim', 'lat': (-10, 5), 'lon': (40, 100), 'vulnerability': 0.85},
            {'name': 'Pacific Northwest Coast', 'lat': (43, 49), 'lon': (-127, -123), 'vulnerability': 0.8},
        ]
    
    def generate_synthetic_training_data(self, n_samples: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic tsunami training data"""
        logger.info(f"Generating {n_samples} synthetic tsunami training samples")
        
        X = []
        y = []
        
        for _ in range(n_samples):
            # Features: earthquake_magnitude, epicenter_depth_km, distance_to_coast_km,
            # coast_slope, ocean_depth_m, latitude, longitude, water_temp, sst_anomaly
            magnitude = np.random.uniform(4, 9)
            depth = np.random.exponential(15)
            coast_dist = np.random.exponential(100)
            coast_slope = np.random.uniform(0.001, 0.1)
            ocean_depth = np.random.exponential(3000)
            lat = np.random.uniform(-60, 60)
            lon = np.random.uniform(-180, 180)
            water_temp = np.random.normal(15, 8)
            sst_anomaly = np.random.normal(0, 1)
            
            # Tsunami wave height calculation using shallow water wave theory
            # H = A * sqrt(D) where D is ocean depth
            # Adjusted by magnitude, depth, and coastal factors
            
            mag_factor = (magnitude - 4) / 5
            depth_factor = np.exp(-depth / 50)  # Shallow earthquakes are more dangerous
            dist_factor = np.exp(-coast_dist / 200)  # Closer to coast = more risk
            slope_factor = coast_slope * 10  # Steeper slopes increase wave height
            ocean_factor = 1 / (1 + np.sqrt(ocean_depth / 1000))  # Shallower water = worse
            
            wave_height = (mag_factor * depth_factor * dist_factor * 
                          slope_factor * ocean_factor * 10)  # Normalized to meters
            
            # Risk score calculation
            zone_risk = self._get_zone_risk(lat, lon)
            vulnerability = self._get_coastal_vulnerability(lat, lon)
            
            risk = (mag_factor * 0.4 + depth_factor * 0.2 + dist_factor * 0.2 + 
                   zone_risk * 0.1 + vulnerability * 0.1)
            risk = np.clip(risk, 0, 1)
            
            X.append([magnitude, depth, coast_dist, coast_slope, ocean_depth, 
                     lat, lon, water_temp, sst_anomaly])
            y.append(risk)
        
        return np.array(X), np.array(y)
    
    def _get_zone_risk(self, lat: float, lon: float) -> float:
        """Get tsunami zone risk"""
        max_risk = 0.1
        
        for zone in self.tsunami_source_zones:
            lat_range = zone['lat']
            lon_range = zone['lon']
            
            if lat_range[0] <= lat <= lat_range[1] and lon_range[0] <= lon <= lon_range[1]:
                max_risk = max(max_risk, 0.8)
        
        return max_risk
    
    def _get_coastal_vulnerability(self, lat: float, lon: float) -> float:
        """Get coastal vulnerability index"""
        for coast in self.vulnerable_coastlines:
            lat_range = coast['lat']
            lon_range = coast['lon']
            
            if lat_range[0] <= lat <= lat_range[1] and lon_range[0] <= lon <= lon_range[1]:
                return coast['vulnerability']
        
        return 0.3  # Default lower vulnerability
    
    def train(self, X: np.ndarray = None, y: np.ndarray = None):
        """Train the tsunami prediction model"""
        if X is None or y is None:
            X, y = self.generate_synthetic_training_data()
        
        logger.info(f"Training tsunami model with {X.shape[0]} samples")
        
        self.feature_names = [
            'earthquake_magnitude', 'epicenter_depth_km', 'distance_to_coast_km',
            'coast_slope', 'ocean_depth_m', 'latitude', 'longitude',
            'water_temperature_c', 'sst_anomaly'
        ]
        
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        logger.info("Tsunami model trained successfully")
    
    def predict(self, earthquake_magnitude: float = 7.0, epicenter_depth_km: float = 10,
                distance_to_coast_km: float = 50, coast_slope: float = 0.02,
                ocean_depth_m: float = 2000, latitude: float = 0, longitude: float = 0,
                water_temp: float = 15, sst_anomaly: float = 0) -> Dict:
        """
        Predict tsunami risk for a seismic event
        
        Returns:
            Dictionary with prediction results
        """
        if not self.is_trained:
            self.train()
        
        # Prepare features
        X = np.array([[earthquake_magnitude, epicenter_depth_km, distance_to_coast_km,
                      coast_slope, ocean_depth_m, latitude, longitude, water_temp, sst_anomaly]])
        X_scaled = self.scaler.transform(X)
        
        risk_score = self.model.predict(X_scaled)[0]
        
        # Calculate tsunami wave parameters using shallow water wave theory
        # Phase speed: c = sqrt(g*h) where h is water depth
        g = 9.81  # gravity
        wave_speed = np.sqrt(g * ocean_depth_m)  # m/s
        
        # Wave height estimation using Kajiura formula
        # Simplified: H = A * sqrt(D) * magnitude_factor
        mag_factor = (earthquake_magnitude - 4) / 5
        depth_factor = np.exp(-epicenter_depth_km / 50)
        
        # Base amplitude related to moment magnitude
        moment_magnitude = earthquake_magnitude
        M0 = 10 ** (1.5 * moment_magnitude + 4.8)  # Seismic moment
        
        # Amplitude from seismic moment (simplified)
        amplitude = M0 / (2 * 1e16) * depth_factor
        
        # Wave height
        wave_height = amplitude * np.sqrt(ocean_depth_m / 1000)
        
        # Travel time to coast
        travel_time_hours = distance_to_coast_km / (wave_speed / 3.6)
        
        # Arrival time
        arrival_time = datetime.now() + timedelta(hours=travel_time_hours)
        
        # Inundation depth
        inundation_depth = wave_height * coast_slope * 10
        
        return {
            'earthquake': {
                'magnitude': earthquake_magnitude,
                'depth_km': epicenter_depth_km,
                'location': {'latitude': latitude, 'longitude': longitude}
            },
            'tsunami_wave': {
                'maximum_height_m': float(max(0, wave_height)),
                'estimated_speed_ms': float(wave_speed),
                'period_minutes': float((distance_to_coast_km * 1000 / wave_speed) / 60)
            },
            'coastal_impact': {
                'estimated_inundation_depth_m': float(max(0, inundation_depth)),
                'maximum_run_up_m': float(max(0, wave_height * 1.5 * coast_slope)),
                'affected_area_sq_km': float(self._estimate_impact_area(wave_height, inundation_depth))
            },
            'timing': {
                'travel_time_hours': float(travel_time_hours),
                'arrival_time': arrival_time.isoformat(),
                'time_to_escape_minutes': float(max(5, travel_time_hours * 60 - 30))
            },
            'risk_assessment': {
                'risk_score': float(risk_score),
                'risk_level': self._classify_tsunami_risk(risk_score, wave_height),
                'threat_level': self._determine_threat_level(wave_height, inundation_depth),
                'coastal_vulnerability': self._get_coastal_vulnerability(latitude, longitude),
                'in_major_subduction_zone': self._check_major_zone(latitude, longitude)
            },
            'recommendation': self._get_tsunami_recommendation(risk_score, wave_height, travel_time_hours),
            'timestamp': datetime.now().isoformat()
        }
    
    def _classify_tsunami_risk(self, score: float, wave_height: float) -> str:
        """Classify tsunami risk"""
        combined = score * 0.6 + np.clip(wave_height / 10, 0, 1) * 0.4
        
        if combined < 0.2:
            return 'NO TSUNAMI THREAT'
        elif combined < 0.4:
            return 'LOW'
        elif combined < 0.6:
            return 'MODERATE'
        elif combined < 0.75:
            return 'HIGH'
        else:
            return 'CRITICAL'
    
    def _determine_threat_level(self, wave_height: float, inundation: float) -> str:
        """Determine threat level based on physical parameters"""
        if wave_height < 0.5:
            return 'ADVISORY'
        elif wave_height < 1.0:
            return 'WATCH'
        elif wave_height < 2.0:
            return 'WARNING'
        else:
            return 'MAJOR WARNING'
    
    def _check_major_zone(self, lat: float, lon: float) -> bool:
        """Check if location is in major subduction zone"""
        for zone in self.tsunami_source_zones:
            lat_range = zone['lat']
            lon_range = zone['lon']
            
            if lat_range[0] <= lat <= lat_range[1] and lon_range[0] <= lon <= lon_range[1]:
                return True
        
        return False
    
    def _estimate_impact_area(self, wave_height: float, inundation: float) -> float:
        """Estimate area affected by tsunami"""
        return (wave_height * inundation) * 100  # Simplified area calculation
    
    def _get_tsunami_recommendation(self, risk_score: float, wave_height: float, travel_time: float) -> str:
        """Get tsunami-specific recommendations"""
        if wave_height < 0.5:
            return "Monitor earthquake reports. No immediate action needed."
        elif wave_height < 1.0:
            return "Tsunami Watch issued. Be prepared to move to higher ground."
        elif wave_height < 2.0:
            return "Tsunami Warning issued. Evacuate immediately to higher ground."
        else:
            if travel_time < 1:
                return "MAJOR TSUNAMI WARNING - EVACUATE IMMEDIATELY. Go to nearest high ground NOW!"
            else:
                return "MAJOR TSUNAMI WARNING - Begin immediate mass evacuation. Move to highest available ground."
    
    def predict_from_earthquake_event(self, earthquake_data: Dict) -> Dict:
        """
        Generate tsunami prediction from earthquake event data
        
        Args:
            earthquake_data: Dict with magnitude, depth, lat, lon from earthquake predictor
            
        Returns:
            Tsunami prediction
        """
        return self.predict(
            earthquake_magnitude=earthquake_data.get('magnitude', 7.0),
            epicenter_depth_km=earthquake_data.get('depth_km', 10),
            distance_to_coast_km=earthquake_data.get('distance_to_coast_km', 100),
            coast_slope=earthquake_data.get('coast_slope', 0.02),
            ocean_depth_m=earthquake_data.get('ocean_depth_m', 2000),
            latitude=earthquake_data.get('latitude', 0),
            longitude=earthquake_data.get('longitude', 0)
        )
    
    def predict_coastal_impact(self, coast_locations: List[Dict]) -> List[Dict]:
        """
        Predict tsunami impact on multiple coastal locations
        
        Args:
            coast_locations: List of coastal location dictionaries
            
        Returns:
            List of impact predictions
        """
        results = []
        
        for coast in coast_locations:
            # Distance from epicenter to coast
            distance = self._calculate_distance(
                coast.get('latitude', 0),
                coast.get('longitude', 0)
            )
            
            result = self.predict(
                earthquake_magnitude=coast.get('magnitude', 7.0),
                epicenter_depth_km=coast.get('depth_km', 10),
                distance_to_coast_km=distance,
                coast_slope=coast.get('slope', 0.02),
                ocean_depth_m=coast.get('ocean_depth_m', 2000),
                latitude=coast.get('latitude', 0),
                longitude=coast.get('longitude', 0)
            )
            results.append(result)
        
        return results
    
    def _calculate_distance(self, lat: float, lon: float) -> float:
        """Calculate distance from epicenter (simplified)"""
        # In real implementation, would use haversine formula
        return np.sqrt(lat**2 + lon**2) * 111  # Rough conversion to km
    
    def generate_tsunami_hazard_map(self, earthquake_lat: float, earthquake_lon: float,
                                  magnitude: float, depth_km: float) -> Dict:
        """
        Generate tsunami hazard map for a region affected by earthquake
        
        Returns:
            Dictionary with hazard information
        """
        # Create grid of coastal points
        coast_lats = np.linspace(max(-60, earthquake_lat - 20), 
                                 min(60, earthquake_lat + 20), 50)
        coast_lons = np.linspace(max(-180, earthquake_lon - 30), 
                                 min(180, earthquake_lon + 30), 80)
        
        hazard_map = np.zeros((len(coast_lats), len(coast_lons)))
        
        for i, lat in enumerate(coast_lats):
            for j, lon in enumerate(coast_lons):
                distance = self._calculate_distance(lat, lon)
                
                if distance < 500:  # Only consider nearby areas
                    result = self.predict(
                        earthquake_magnitude=magnitude,
                        epicenter_depth_km=depth_km,
                        distance_to_coast_km=distance,
                        latitude=lat,
                        longitude=lon
                    )
                    hazard_map[i, j] = result['tsunami_wave']['maximum_height_m']
        
        return {
            'hazard_map': hazard_map,
            'latitude_grid': coast_lats,
            'longitude_grid': coast_lons,
            'max_wave_height_m': float(np.max(hazard_map)),
            'affected_area_count': int(np.count_nonzero(hazard_map > 0.5))
        }
