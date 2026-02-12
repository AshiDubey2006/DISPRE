"""
Flood Prediction Model
Predicts flood risk based on rainfall, soil moisture, topography, and river data
"""

import logging
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple, List
from datetime import datetime

logger = logging.getLogger(__name__)


class FloodPredictor:
    """Flood prediction model"""
    
    def __init__(self):
        """Initialize flood predictor"""
        self.model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        
        # River basins and flood-prone areas
        self.flood_prone_areas = [
            {'name': 'Ganga Basin', 'lat': (22, 32), 'lon': (72, 88), 'base_risk': 0.7},
            {'name': 'Brahmaputra', 'lat': (24, 30), 'lon': (88, 95), 'base_risk': 0.75},
            {'name': 'Amazon Basin', 'lat': (-10, 5), 'lon': (-75, -50), 'base_risk': 0.7},
            {'name': 'Mississippi', 'lat': (28, 45), 'lon': (-100, -85), 'base_risk': 0.6},
            {'name': 'Yangtze', 'lat': (28, 35), 'lon': (108, 120), 'base_risk': 0.65},
        ]
    
    def generate_synthetic_training_data(self, n_samples: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic flood training data"""
        logger.info(f"Generating {n_samples} synthetic flood training samples")
        
        X = []
        y = []
        
        for _ in range(n_samples):
            # Features: rainfall_mm, soil_moisture, elevation_m, slope_deg, 
            # river_distance_km, urbanization_factor, dam_capacity_ratio, antecedent_moisture
            rainfall = np.random.gamma(shape=2, scale=5)
            soil_moisture = np.random.uniform(0, 1)
            elevation = np.random.exponential(500)
            slope = np.random.exponential(5)
            river_dist = np.random.exponential(10)
            urbanization = np.random.uniform(0, 1)
            dam_ratio = np.random.uniform(0, 1)
            antecedent = np.random.uniform(0, 1)
            
            # Calculate flood risk
            rainfall_factor = np.clip(rainfall / 100, 0, 1)
            moisture_factor = soil_moisture * 0.3
            elevation_factor = np.clip(1 - elevation/2000, 0, 1) * 0.2
            slope_factor = np.clip(1 - slope/30, 0, 1) * 0.2
            proximity_factor = np.clip(1 - river_dist/50, 0, 1) * 0.3
            urban_factor = urbanization * 0.15
            dam_factor = (1 - dam_ratio) * 0.1
            
            risk = (rainfall_factor * 0.4 + moisture_factor + elevation_factor + 
                   slope_factor + proximity_factor + urban_factor + dam_factor + antecedent * 0.1)
            
            risk = np.clip(risk, 0, 1)
            
            X.append([rainfall, soil_moisture, elevation, slope, river_dist, 
                     urbanization, dam_ratio, antecedent])
            y.append(risk)
        
        return np.array(X), np.array(y)
    
    def train(self, X: np.ndarray = None, y: np.ndarray = None):
        """Train the flood prediction model"""
        if X is None or y is None:
            X, y = self.generate_synthetic_training_data()
        
        logger.info(f"Training flood model with {X.shape[0]} samples")
        
        self.feature_names = [
            'rainfall_mm', 'soil_moisture', 'elevation_m', 'slope_degrees',
            'river_distance_km', 'urbanization_factor', 'dam_capacity_ratio', 'antecedent_moisture'
        ]
        
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        logger.info("Flood model trained successfully")
    
    def predict(self, rainfall_mm: float = 50, soil_moisture: float = 0.5,
                elevation_m: float = 500, slope_deg: float = 5,
                river_distance_km: float = 10, urbanization: float = 0.3,
                dam_capacity_ratio: float = 0.5, antecedent_moisture: float = 0.4) -> Dict:
        """
        Predict flood risk for a location
        
        Returns:
            Dictionary with prediction results
        """
        if not self.is_trained:
            self.train()
        
        # Prepare features
        X = np.array([[rainfall_mm, soil_moisture, elevation_m, slope_deg, 
                      river_distance_km, urbanization, dam_capacity_ratio, antecedent_moisture]])
        X_scaled = self.scaler.transform(X)
        
        risk_score = self.model.predict(X_scaled)[0]
        
        # Calculate water depth if flood occurs
        runoff_coeff = (1 - np.clip(elevation_m/2000, 0, 1)) * (1 - np.clip(slope_deg/30, 0, 1))
        infiltration_rate = (1 - soil_moisture) * 10  # mm/hr
        excess_rainfall = max(0, rainfall_mm - infiltration_rate)
        predicted_water_depth = excess_rainfall * runoff_coeff / 10
        
        return {
            'rainfall_mm': rainfall_mm,
            'soil_moisture': soil_moisture,
            'elevation_m': elevation_m,
            'slope_degrees': slope_deg,
            'risk_score': float(risk_score),
            'risk_level': self._classify_flood_risk(risk_score),
            'predicted_water_depth_m': float(predicted_water_depth),
            'flood_probability': float(min(risk_score * 1.2, 1.0)),
            'warning_level': self._determine_warning_level(risk_score, rainfall_mm),
            'affected_area_sq_km': float(self._estimate_affected_area(risk_score, elevation_m, slope_deg)),
            'flood_prone_region': self._check_flood_prone_region(elevation_m),
            'recommendation': self._get_flood_recommendation(risk_score, rainfall_mm),
            'timestamp': datetime.now().isoformat()
        }
    
    def _classify_flood_risk(self, score: float) -> str:
        """Classify flood risk level"""
        if score < 0.2:
            return 'NO FLOOD RISK'
        elif score < 0.35:
            return 'LOW'
        elif score < 0.5:
            return 'MODERATE'
        elif score < 0.65:
            return 'HIGH'
        elif score < 0.8:
            return 'VERY HIGH'
        else:
            return 'CRITICAL'
    
    def _determine_warning_level(self, risk_score: float, rainfall_mm: float) -> str:
        """Determine warning level"""
        combined_score = risk_score * 0.6 + np.clip(rainfall_mm / 100, 0, 1) * 0.4
        
        if combined_score < 0.25:
            return 'GREEN'
        elif combined_score < 0.4:
            return 'YELLOW'
        elif combined_score < 0.6:
            return 'ORANGE'
        else:
            return 'RED'
    
    def _estimate_affected_area(self, risk_score: float, elevation: float, slope: float) -> float:
        """Estimate flood-affected area in sq km"""
        base_area = 100 * risk_score
        elevation_factor = np.clip(1 - elevation/2000, 0, 1)
        slope_factor = np.clip(1 - slope/30, 0, 1)
        
        return base_area * elevation_factor * slope_factor
    
    def _check_flood_prone_region(self, elevation: float) -> str:
        """Check if location is in known flood-prone region"""
        # In real implementation, would check actual coordinates
        if elevation < 500:
            return "High flood-prone area (low elevation)"
        elif elevation < 1000:
            return "Moderate flood-prone area"
        else:
            return "Low flood-prone area (high elevation)"
    
    def _get_flood_recommendation(self, risk_score: float, rainfall_mm: float) -> str:
        """Get flood-specific recommendations"""
        if risk_score < 0.2:
            return "Routine monitoring. No immediate action needed."
        elif risk_score < 0.35:
            return "Monitor weather forecasts. Prepare evacuation routes."
        elif risk_score < 0.5:
            return "Alert issued. Review emergency plans. Prepare shelters."
        elif risk_score < 0.65:
            return "Warning issued. Begin pre-positioning of resources."
        elif risk_score < 0.8:
            return "Flood Watch active. Activate emergency operations center."
        else:
            return "FLOOD WARNING - Evacuate immediately. All personnel to safe zones."
    
    def predict_temporal_series(self, rainfall_series: List[float], soil_moisture_series: List[float]) -> List[Dict]:
        """
        Predict flood risk over time series
        
        Args:
            rainfall_series: Time series of rainfall data
            soil_moisture_series: Time series of soil moisture
            
        Returns:
            List of predictions for each time step
        """
        results = []
        
        for i, rainfall in enumerate(rainfall_series):
            soil_moisture = soil_moisture_series[i] if i < len(soil_moisture_series) else 0.5
            
            result = self.predict(
                rainfall_mm=rainfall,
                soil_moisture=soil_moisture,
                elevation_m=500,
                slope_deg=5,
                river_distance_km=10,
                urbanization=0.3,
                dam_capacity_ratio=0.5,
                antecedent_moisture=soil_moisture
            )
            results.append(result)
        
        return results
    
    def generate_flood_risk_map(self, rainfall_grid: np.ndarray, 
                               elevation_grid: np.ndarray,
                               soil_moisture_grid: np.ndarray) -> np.ndarray:
        """
        Generate flood risk heatmap for a region
        
        Returns:
            2D flood risk array
        """
        if not self.is_trained:
            self.train()
        
        risk_map = np.zeros_like(rainfall_grid)
        
        for i in range(rainfall_grid.shape[0]):
            for j in range(rainfall_grid.shape[1]):
                X = np.array([[
                    rainfall_grid[i, j],
                    soil_moisture_grid[i, j],
                    elevation_grid[i, j],
                    5, 10, 0.3, 0.5, soil_moisture_grid[i, j]
                ]])
                X_scaled = self.scaler.transform(X)
                risk_map[i, j] = self.model.predict(X_scaled)[0]
        
        return risk_map
    
    def calculate_runoff(self, rainfall_mm: float, soil_type: str = 'loam') -> float:
        """Calculate runoff using simple CN method"""
        cn_values = {
            'sand': 50,
            'loam': 75,
            'clay': 85,
            'urban': 90
        }
        
        cn = cn_values.get(soil_type, 75)
        s = (25400 / cn) - 254
        
        if rainfall_mm > 0.2 * s:
            runoff = (rainfall_mm - 0.2 * s) ** 2 / (rainfall_mm + 0.8 * s)
        else:
            runoff = 0
        
        return runoff
