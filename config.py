"""
Configuration file for DISPRE
Customize these settings to adjust model behavior
"""

# ============================================================================
# EARTHQUAKE PREDICTION CONFIGURATION
# ============================================================================

EARTHQUAKE_CONFIG = {
    # Model parameters
    'model_type': 'GradientBoosting',
    'n_estimators': 100,
    'learning_rate': 0.1,
    'max_depth': 7,
    
    # Risk thresholds
    'risk_thresholds': {
        'low': 0.2,
        'moderate': 0.4,
        'elevated': 0.6,
        'high': 0.8,
        'critical': 1.0
    },
    
    # Feature weights
    'feature_weights': {
        'tectonic_position': 0.3,
        'crustal_strain': 0.3,
        'plate_motion': 0.25,
        'depth': 0.15
    },
    
    # Training data
    'training_samples': 500,
    'random_seed': 42
}

# ============================================================================
# FLOOD PREDICTION CONFIGURATION
# ============================================================================

FLOOD_CONFIG = {
    # Model parameters
    'model_type': 'GradientBoosting',
    'n_estimators': 100,
    'learning_rate': 0.1,
    'max_depth': 8,
    
    # Risk thresholds
    'risk_thresholds': {
        'no_risk': 0.2,
        'low': 0.35,
        'moderate': 0.5,
        'high': 0.65,
        'very_high': 0.8,
        'critical': 1.0
    },
    
    # Warning levels
    'warning_thresholds': {
        'green': 0.25,
        'yellow': 0.4,
        'orange': 0.6,
        'red': 1.0
    },
    
    # Feature weights
    'feature_weights': {
        'rainfall': 0.4,
        'soil_moisture': 0.2,
        'topography': 0.2,
        'land_use': 0.15,
        'hydrology': 0.05
    },
    
    # Physical parameters
    'infiltration_rates': {
        'sand': 25,        # mm/hr
        'loam': 10,        # mm/hr
        'clay': 3,         # mm/hr
        'urban': 1         # mm/hr
    },
    
    # Training data
    'training_samples': 500,
    'random_seed': 42
}

# ============================================================================
# TSUNAMI PREDICTION CONFIGURATION
# ============================================================================

TSUNAMI_CONFIG = {
    # Model parameters
    'model_type': 'RandomForest',
    'n_estimators': 100,
    'max_depth': 10,
    'random_seed': 42,
    
    # Risk thresholds
    'risk_thresholds': {
        'no_threat': 0.2,
        'low': 0.4,
        'moderate': 0.6,
        'high': 0.75,
        'critical': 1.0
    },
    
    # Threat levels based on wave height
    'threat_levels': {
        'advisory': 0.5,     # meters
        'watch': 1.0,        # meters
        'warning': 2.0,      # meters
        'major_warning': 3.0 # meters
    },
    
    # Travel time alert
    'evacuation_time_minutes': 30,
    
    # Feature weights
    'feature_weights': {
        'earthquake_magnitude': 0.3,
        'epicenter_depth': 0.2,
        'coastal_proximity': 0.25,
        'coastal_vulnerability': 0.15,
        'ocean_bathymetry': 0.1
    },
    
    # Physical parameters
    'gravity': 9.81,  # m/s²
    'wave_shoaling_factor': 1.5,  # Run-up amplification
    
    # Training data
    'training_samples': 500
}

# ============================================================================
# DATA CONFIGURATION
# ============================================================================

DATA_CONFIG = {
    # Data directories
    'data_dir': './data',
    'output_dir': './output',
    'log_dir': './logs',
    
    # Data resolution settings
    'grid_resolution': {
        'fine': 50,      # Fine resolution for local analysis
        'medium': 20,    # Medium for regional analysis
        'coarse': 10     # Coarse for global overview
    },
    
    # Data retention (days)
    'earthquake_data_retention': 365,
    'rainfall_data_retention': 180,
    'sst_data_retention': 90,
    
    # Download timeouts (seconds)
    'download_timeout': 30
}

# ============================================================================
# VISUALIZATION CONFIGURATION
# ============================================================================

VISUALIZATION_CONFIG = {
    # Color schemes
    'colormaps': {
        'risk': 'RdYlGn_r',           # Red-Yellow-Green reversed
        'rainfall': 'Blues',
        'temperature': 'RdBu_r',
        'wave_height': 'viridis'
    },
    
    # Figure settings
    'figure_size': (14, 10),
    'dpi': 300,
    'font_size': 11,
    
    # Map projections
    'map_projection': 'PlateCarree',
    'contour_levels': 20
}

# ============================================================================
# ALERT CONFIGURATION
# ============================================================================

ALERT_CONFIG = {
    # Critical thresholds
    'critical_thresholds': {
        'earthquake_risk': 0.8,
        'flood_risk': 0.8,
        'tsunami_wave_height': 2.0,  # meters
        'tsunami_travel_time': 2.0   # hours
    },
    
    # Alert types
    'alert_types': {
        'advisory': {'color': 'yellow', 'sound': False},
        'watch': {'color': 'orange', 'sound': False},
        'warning': {'color': 'red', 'sound': True},
        'major_warning': {'color': 'darkred', 'sound': True}
    },
    
    # Notification methods
    'notifications': {
        'email': True,
        'sms': True,
        'siren': True,
        'broadcast': True
    }
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': './logs/dispre.log',
    'max_file_size': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 5
}

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

ADVANCED_CONFIG = {
    # Ensemble settings
    'use_ensemble': True,
    'ensemble_models': ['GradientBoosting', 'RandomForest', 'NeuralNetwork'],
    'ensemble_weights': [0.4, 0.35, 0.25],
    
    # Cross-validation
    'cv_folds': 5,
    'cv_strategy': 'stratified',
    
    # Hyperparameter optimization
    'optimize_hyperparameters': False,
    'optimization_iterations': 100,
    
    # Feature importance
    'calculate_feature_importance': True,
    'feature_importance_threshold': 0.01
}

# ============================================================================
# GEOGRAPHIC REGIONS
# ============================================================================

REGIONS = {
    'global': {
        'lat_range': (-90, 90),
        'lon_range': (-180, 180)
    },
    'asia_pacific': {
        'lat_range': (-60, 60),
        'lon_range': (80, 180)
    },
    'americas': {
        'lat_range': (-60, 85),
        'lon_range': (-180, -30)
    },
    'europe_africa': {
        'lat_range': (-60, 75),
        'lon_range': (-30, 90)
    },
    'indian_ocean': {
        'lat_range': (-60, 30),
        'lon_range': (30, 120)
    }
}

# ============================================================================
# MODEL TRAINING PARAMETERS
# ============================================================================

TRAINING_CONFIG = {
    # Data split
    'train_test_split': 0.8,
    'validation_split': 0.1,
    
    # Regularization
    'l1_penalty': 0.001,
    'l2_penalty': 0.001,
    'dropout_rate': 0.2,
    
    # Early stopping
    'early_stopping': True,
    'patience': 10,
    'min_delta': 0.0001,
    
    # Batch settings
    'batch_size': 32,
    'epochs': 100
}

# ============================================================================
# REAL-TIME PROCESSING
# ============================================================================

REALTIME_CONFIG = {
    'update_frequency_minutes': 60,  # Update predictions every hour
    'streaming_enabled': True,
    'buffer_size': 1000,  # Store last 1000 predictions
    'compression': True
}

# ============================================================================
# API CONFIGURATION (if web service deployed)
# ============================================================================

API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
    'debug': False,
    'max_request_size': 50 * 1024 * 1024,  # 50 MB
    'rate_limit': 100,  # requests per minute
    'timeout': 30  # seconds
}
