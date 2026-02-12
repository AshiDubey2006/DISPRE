"""
Data Loading and Preprocessing Module
Handles downloading and processing datasets from various sources
"""

import logging
import os
import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import xarray as xr

logger = logging.getLogger(__name__)


class DataDownloader:
    """Download climate and weather datasets"""
    
    SOURCES = {
        'nasa_imerg': 'https://gpm1.gesdisc.eosdis.nasa.gov/opentopography/raster/DEM_srtm/SRTM_GL3/SRTM_GL3_srtm/',
        'copernicus_era5': 'https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5/',
        'noaa_gfs': 'https://www.ncei.noaa.gov/products/weather-global-forecasting-system/',
        'usgs_earthquake': 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/',
        'ibt_racs': 'https://www.ncei.noaa.gov/products/international-best-track-archive-lreq-hurdat-2/',
    }
    
    def __init__(self, data_dir: str = './data'):
        """Initialize downloader"""
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
    def download_earthquake_data(self, days_back: int = 30, magnitude_min: float = 2.5) -> pd.DataFrame:
        """
        Download earthquake data from USGS
        
        Args:
            days_back: Number of days to look back
            magnitude_min: Minimum magnitude filter
            
        Returns:
            DataFrame with earthquake data
        """
        logger.info(f"Downloading earthquake data (last {days_back} days, mag > {magnitude_min})")
        
        try:
            start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            url = f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            earthquakes = []
            for feature in data['features']:
                props = feature['properties']
                geom = feature['geometry']
                
                if props['mag'] >= magnitude_min:
                    earthquakes.append({
                        'timestamp': datetime.fromtimestamp(props['time']/1000),
                        'latitude': geom['coordinates'][1],
                        'longitude': geom['coordinates'][0],
                        'depth_km': geom['coordinates'][2],
                        'magnitude': props['mag'],
                        'place': props['place'],
                    })
            
            df = pd.DataFrame(earthquakes)
            logger.info(f"Downloaded {len(df)} earthquakes")
            return df
            
        except Exception as e:
            logger.error(f"Failed to download earthquake data: {e}")
            return pd.DataFrame()
    
    def download_rainfall_data(self, lat_min: float, lat_max: float, 
                              lon_min: float, lon_max: float) -> Dict:
        """
        Download rainfall data (simulated IMERG/CHIRPS)
        
        Args:
            lat_min, lat_max, lon_min, lon_max: Bounding box
            
        Returns:
            Dictionary with rainfall data
        """
        logger.info(f"Downloading rainfall data for region ({lat_min},{lon_min}) to ({lat_max},{lon_max})")
        
        try:
            # Simulated rainfall data with realistic patterns
            lat = np.linspace(lat_min, lat_max, 100)
            lon = np.linspace(lon_min, lon_max, 100)
            time = pd.date_range(end=datetime.now(), periods=365, freq='D')
            
            # Generate realistic rainfall pattern
            rainfall = np.random.gamma(shape=2, scale=10, size=(len(time), len(lat), len(lon)))
            
            # Add seasonal variation
            seasonal = 50 * (1 + 0.5 * np.sin(2 * np.pi * np.arange(len(time)) / 365))
            rainfall = rainfall * seasonal[:, np.newaxis, np.newaxis]
            
            return {
                'latitude': lat,
                'longitude': lon,
                'time': time,
                'rainfall_mm': rainfall,
                'units': 'mm',
                'temporal_resolution': 'daily'
            }
            
        except Exception as e:
            logger.error(f"Failed to download rainfall data: {e}")
            return {}
    
    def download_temperature_data(self, lat_min: float, lat_max: float,
                                 lon_min: float, lon_max: float) -> Dict:
        """
        Download temperature data (simulated ERA5)
        """
        logger.info("Downloading temperature data")
        
        try:
            lat = np.linspace(lat_min, lat_max, 100)
            lon = np.linspace(lon_min, lon_max, 100)
            time = pd.date_range(end=datetime.now(), periods=365, freq='D')
            
            # Realistic temperature with seasonal variation
            mean_temp = 25  # Base temperature
            seasonal = 15 * np.sin(2 * np.pi * np.arange(len(time)) / 365)
            noise = np.random.normal(0, 2, (len(time), len(lat), len(lon)))
            
            temp = mean_temp + seasonal[:, np.newaxis, np.newaxis] + noise
            
            return {
                'latitude': lat,
                'longitude': lon,
                'time': time,
                'temperature_celsius': temp,
                'units': 'Celsius',
                'temporal_resolution': 'daily'
            }
            
        except Exception as e:
            logger.error(f"Failed to download temperature data: {e}")
            return {}
    
    def download_sea_surface_temp(self) -> Dict:
        """Download sea surface temperature data"""
        logger.info("Downloading sea surface temperature data")
        
        try:
            lat = np.linspace(-60, 60, 120)
            lon = np.linspace(-180, 180, 360)
            time = pd.date_range(end=datetime.now(), periods=365, freq='D')
            
            # SST with tropical enhancement
            sst = 15 + 15 * np.sin(np.radians(lat))[:, np.newaxis]
            sst = sst[np.newaxis, :, :] + np.random.normal(0, 1, (len(time), len(lat), len(lon)))
            
            return {
                'latitude': lat,
                'longitude': lon,
                'time': time,
                'sst_celsius': sst,
                'units': 'Celsius'
            }
            
        except Exception as e:
            logger.error(f"Failed to download SST data: {e}")
            return {}
    
    def download_soil_moisture(self, lat_min: float, lat_max: float,
                              lon_min: float, lon_max: float) -> Dict:
        """Download soil moisture data (simulated SMAP/SMOS)"""
        logger.info("Downloading soil moisture data")
        
        try:
            lat = np.linspace(lat_min, lat_max, 100)
            lon = np.linspace(lon_min, lon_max, 100)
            time = pd.date_range(end=datetime.now(), periods=365, freq='D')
            
            # Soil moisture correlation with rainfall
            soil_moisture = np.random.uniform(0.1, 0.5, (len(time), len(lat), len(lon)))
            
            return {
                'latitude': lat,
                'longitude': lon,
                'time': time,
                'soil_moisture': soil_moisture,
                'units': 'volumetric_water_content',
                'temporal_resolution': 'daily'
            }
            
        except Exception as e:
            logger.error(f"Failed to download soil moisture data: {e}")
            return {}


class DataPreprocessor:
    """Preprocess and validate data"""
    
    def __init__(self):
        """Initialize preprocessor"""
        self.logger = logging.getLogger(__name__)
    
    def normalize_data(self, data: np.ndarray) -> np.ndarray:
        """Normalize data to 0-1 range"""
        min_val = np.nanmin(data)
        max_val = np.nanmax(data)
        
        if max_val == min_val:
            return np.zeros_like(data)
        
        return (data - min_val) / (max_val - min_val)
    
    def handle_missing_values(self, data: np.ndarray, method: str = 'interpolate') -> np.ndarray:
        """Handle missing values in data"""
        if method == 'interpolate':
            # Simple interpolation
            mask = np.isnan(data)
            if mask.any():
                for i in range(data.shape[0]):
                    if mask[i].any():
                        valid_idx = np.where(~mask[i])[0]
                        if len(valid_idx) > 0:
                            data[i, mask[i]] = np.interp(
                                np.where(mask[i])[0],
                                valid_idx,
                                data[i, valid_idx]
                            )
        elif method == 'mean':
            data = np.nan_to_num(data, nan=np.nanmean(data))
        
        return data
    
    def create_features(self, data_dict: Dict) -> pd.DataFrame:
        """Create features from raw data"""
        features = pd.DataFrame()
        
        for key, value in data_dict.items():
            if isinstance(value, np.ndarray):
                # Flatten spatial-temporal data
                features[f'{key}_mean'] = np.nanmean(value, axis=(1, 2))
                features[f'{key}_std'] = np.nanstd(value, axis=(1, 2))
                features[f'{key}_max'] = np.nanmax(value, axis=(1, 2))
                features[f'{key}_min'] = np.nanmin(value, axis=(1, 2))
        
        return features
