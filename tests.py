"""
Testing module for DISPRE
Unit tests for all prediction models
"""

import unittest
import sys
import os
import numpy as np

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.earthquake import EarthquakePredictor
from models.flood import FloodPredictor
from models.tsunami import TsunamiPredictor
from data.data_loader import DataDownloader, DataPreprocessor


class TestEarthquakePredictor(unittest.TestCase):
    """Test earthquake prediction model"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.predictor = EarthquakePredictor()
        self.predictor.train()
    
    def test_predict_returns_dict(self):
        """Test that predict returns a dictionary"""
        result = self.predictor.predict(lat=35.0, lon=140.0)
        self.assertIsInstance(result, dict)
    
    def test_predict_contains_required_fields(self):
        """Test that prediction contains required fields"""
        result = self.predictor.predict(lat=35.0, lon=140.0)
        required_fields = ['risk_score', 'risk_level', 'expected_magnitude', 'recommendation']
        
        for field in required_fields:
            self.assertIn(field, result)
    
    def test_risk_score_range(self):
        """Test that risk score is between 0 and 1"""
        result = self.predictor.predict(lat=35.0, lon=140.0)
        self.assertGreaterEqual(result['risk_score'], 0)
        self.assertLessEqual(result['risk_score'], 1)
    
    def test_magnitude_range(self):
        """Test that magnitude is realistic"""
        result = self.predictor.predict(lat=35.0, lon=140.0)
        magnitude = result['expected_magnitude']
        self.assertGreater(magnitude, 0)
        self.assertLess(magnitude, 10)
    
    def test_batch_predict(self):
        """Test batch predictions"""
        locations = [
            {'latitude': 35.0, 'longitude': 140.0},
            {'latitude': 36.5, 'longitude': -120.5},
            {'latitude': -8.5, 'longitude': 95.0}
        ]
        
        results = self.predictor.predict_batch(locations)
        self.assertEqual(len(results), 3)
    
    def test_high_risk_zones(self):
        """Test high risk zone identification"""
        grid_lat = np.linspace(30, 45, 10)
        grid_lon = np.linspace(130, 145, 10)
        
        risk_grid = self.predictor.get_high_risk_zones(grid_lat, grid_lon)
        self.assertEqual(risk_grid.shape, (10, 10))
        self.assertGreater(np.max(risk_grid), 0)


class TestFloodPredictor(unittest.TestCase):
    """Test flood prediction model"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.predictor = FloodPredictor()
        self.predictor.train()
    
    def test_predict_returns_dict(self):
        """Test that predict returns a dictionary"""
        result = self.predictor.predict()
        self.assertIsInstance(result, dict)
    
    def test_flood_risk_classification(self):
        """Test flood risk classification"""
        # Low risk
        low_risk = self.predictor.predict(rainfall_mm=10, soil_moisture=0.3)
        self.assertIn(low_risk['risk_level'], ['NO FLOOD RISK', 'LOW'])
        
        # High risk
        high_risk = self.predictor.predict(rainfall_mm=200, soil_moisture=0.9)
        self.assertIn(high_risk['risk_level'], ['HIGH', 'VERY HIGH', 'CRITICAL'])
    
    def test_water_depth_positive(self):
        """Test that predicted water depth is non-negative"""
        result = self.predictor.predict(rainfall_mm=100)
        self.assertGreaterEqual(result['predicted_water_depth_m'], 0)
    
    def test_temporal_series_predict(self):
        """Test temporal series prediction"""
        rainfall_series = [10, 25, 50, 100, 75, 30, 10]
        soil_moisture_series = [0.3, 0.4, 0.5, 0.8, 0.7, 0.5, 0.3]
        
        results = self.predictor.predict_temporal_series(rainfall_series, soil_moisture_series)
        self.assertEqual(len(results), 7)
    
    def test_runoff_calculation(self):
        """Test runoff calculation"""
        runoff = self.predictor.calculate_runoff(rainfall_mm=100)
        self.assertGreaterEqual(runoff, 0)


class TestTsunamiPredictor(unittest.TestCase):
    """Test tsunami prediction model"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.predictor = TsunamiPredictor()
        self.predictor.train()
    
    def test_predict_returns_dict(self):
        """Test that predict returns a dictionary"""
        result = self.predictor.predict()
        self.assertIsInstance(result, dict)
    
    def test_wave_height_positive(self):
        """Test that wave height is non-negative"""
        result = self.predictor.predict(earthquake_magnitude=7.0)
        wave_height = result['tsunami_wave']['maximum_height_m']
        self.assertGreaterEqual(wave_height, 0)
    
    def test_travel_time_reasonable(self):
        """Test that travel time is reasonable"""
        result = self.predictor.predict(distance_to_coast_km=100, ocean_depth_m=3000)
        travel_time = result['timing']['travel_time_hours']
        self.assertGreater(travel_time, 0)
        self.assertLess(travel_time, 24)  # Less than 24 hours
    
    def test_threat_level_classification(self):
        """Test threat level classification"""
        # Low wave
        low = self.predictor.predict(earthquake_magnitude=5.0, distance_to_coast_km=500)
        self.assertIsNotNone(low['risk_assessment']['threat_level'])
        
        # High wave
        high = self.predictor.predict(earthquake_magnitude=8.5, distance_to_coast_km=50)
        self.assertIsNotNone(high['risk_assessment']['threat_level'])
    
    def test_coastal_impact_multiple_locations(self):
        """Test impact prediction for multiple coastal locations"""
        coasts = [
            {'latitude': 35.0, 'longitude': 140.0, 'magnitude': 8.0, 'depth_km': 20},
            {'latitude': 36.5, 'longitude': -120.5, 'magnitude': 7.5, 'depth_km': 15}
        ]
        
        results = self.predictor.predict_coastal_impact(coasts)
        self.assertEqual(len(results), 2)


class TestDataProcessing(unittest.TestCase):
    """Test data loading and preprocessing"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.downloader = DataDownloader('./test_data')
        self.preprocessor = DataPreprocessor()
    
    def test_earthquake_data_download(self):
        """Test earthquake data download"""
        data = self.downloader.download_earthquake_data(days_back=30)
        # May return empty DataFrame if no internet, but shouldn't error
        self.assertIsNotNone(data)
    
    def test_rainfall_data_download(self):
        """Test rainfall data download"""
        data = self.downloader.download_rainfall_data(20, 40, 100, 120)
        self.assertIsNotNone(data)
        self.assertIn('rainfall_mm', data)
    
    def test_normalize_data(self):
        """Test data normalization"""
        data = np.array([[1, 2, 3], [4, 5, 6]])
        normalized = self.preprocessor.normalize_data(data)
        
        self.assertGreaterEqual(np.min(normalized), 0)
        self.assertLessEqual(np.max(normalized), 1)
    
    def test_missing_value_handling(self):
        """Test missing value handling"""
        data = np.array([[1, np.nan, 3], [np.nan, 5, 6]])
        cleaned = self.preprocessor.handle_missing_values(data)
        
        self.assertEqual(np.isnan(cleaned).sum(), 0)


class TestModelIntegration(unittest.TestCase):
    """Integration tests for all models"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.eq_predictor = EarthquakePredictor()
        self.flood_predictor = FloodPredictor()
        self.tsunami_predictor = TsunamiPredictor()
        
        self.eq_predictor.train()
        self.flood_predictor.train()
        self.tsunami_predictor.train()
    
    def test_multi_hazard_prediction(self):
        """Test predictions for all three hazards at same location"""
        lat, lon = 35.0, 140.0
        
        eq = self.eq_predictor.predict(lat=lat, lon=lon)
        flood = self.flood_predictor.predict(rainfall_mm=75)
        tsunami = self.tsunami_predictor.predict(latitude=lat, longitude=lon)
        
        self.assertIsNotNone(eq)
        self.assertIsNotNone(flood)
        self.assertIsNotNone(tsunami)
    
    def test_cascade_prediction(self):
        """Test cascading prediction (earthquake -> tsunami)"""
        # Large earthquake
        eq = self.eq_predictor.predict(lat=35.0, lon=140.0, strain=0.9, depth_km=15)
        
        # If high risk, check tsunami
        if eq['risk_level'] in ['HIGH', 'CRITICAL']:
            tsunami = self.tsunami_predictor.predict(
                earthquake_magnitude=eq['expected_magnitude'],
                latitude=35.0,
                longitude=140.0
            )
            self.assertIsNotNone(tsunami)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEarthquakePredictor))
    suite.addTests(loader.loadTestsFromTestCase(TestFloodPredictor))
    suite.addTests(loader.loadTestsFromTestCase(TestTsunamiPredictor))
    suite.addTests(loader.loadTestsFromTestCase(TestDataProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestModelIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("\n" + "="*70)
    print("DISPRE Test Suite")
    print("="*70 + "\n")
    
    result = run_tests()
    
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70 + "\n")
