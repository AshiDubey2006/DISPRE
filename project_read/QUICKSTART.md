# DISPRE Quick Start Guide

## 🚀 Installation

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd DISPRE_vs

# Install all required packages
pip install -r requirements.txt
```

This will install:
- NumPy, Pandas, SciPy (data processing)
- Scikit-learn (machine learning)
- Matplotlib, Seaborn, Plotly (visualization)
- TensorFlow/Keras (deep learning - optional)
- And more...

**Installation time**: ~5-10 minutes

### Step 2: Run the System

```bash
# Run the complete disaster prediction system
python main.py
```

This will:
1. ✅ Initialize the DISPRE engine
2. ✅ Train all three prediction models
3. ✅ Run predictions for 4 test locations
4. ✅ Generate comprehensive reports
5. ✅ Create visualizations and charts

**Execution time**: ~2-5 minutes

### Step 3: Review Results

Check the `./output/` directory for:
- `disaster_report_*.html` - Interactive HTML report
- `risk_comparison.png` - Multi-hazard risk comparison chart
- `*_data.json` - Raw prediction data

---

## 📊 Basic Usage

### Single Location Prediction

```python
from src.dispre_engine import DISPREEngine

# Initialize
engine = DISPREEngine()
engine.train_all_models()

# Predict for one location
predictions = engine.predict_all_hazards(
    latitude=35.0,
    longitude=140.0,
    rainfall_mm=75,
    earthquake_magnitude=7.0
)

# Print results
print("Earthquake Risk:", predictions['earthquake']['risk_level'])
print("Flood Risk:", predictions['flood']['risk_level'])
print("Tsunami Threat:", predictions['tsunami']['risk_assessment']['threat_level'])
```

### Get Specific Hazard Predictions

```python
# Earthquake only
earthquake = engine.predict_earthquake(lat=35.0, lon=140.0)
print(f"Expected magnitude: {earthquake['expected_magnitude']:.1f}")

# Flood only
flood = engine.predict_flood(latitude=35.0, longitude=140.0, rainfall_mm=100)
print(f"Flood probability: {flood['flood_probability']*100:.1f}%")

# Tsunami only
tsunami = engine.predict_tsunami(latitude=35.0, longitude=140.0, magnitude=7.5)
print(f"Max wave height: {tsunami['tsunami_wave']['maximum_height_m']:.2f}m")
```

### Generate Reports

```python
# Create comprehensive report
predictions = engine.predict_all_hazards(35.0, 140.0)
report = engine.create_full_report(predictions, "my_report")

# Check for critical alerts
alerts = engine.run_emergency_alert(predictions)
if alerts['alert_count'] > 0:
    print("CRITICAL ALERTS:", alerts['active_alerts'])
```

---

## 🌐 REST API Usage

### Start API Server

```bash
python api_server.py
```

Server runs on `http://localhost:8000`

### API Endpoints

#### Get All Predictions
```bash
curl -X POST http://localhost:8000/predict/all \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 35.0,
    "longitude": 140.0,
    "rainfall_mm": 75,
    "earthquake_magnitude": 7.0
  }'
```

#### Earthquake Only
```bash
curl -X POST http://localhost:8000/predict/earthquake \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 35.0,
    "longitude": 140.0
  }'
```

#### Flood Only
```bash
curl -X POST http://localhost:8000/predict/flood \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 35.0,
    "longitude": 140.0,
    "rainfall_mm": 100
  }'
```

#### Tsunami Only
```bash
curl -X POST http://localhost:8000/predict/tsunami \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 35.0,
    "longitude": 140.0,
    "earthquake_magnitude": 7.5
  }'
```

---

## 🧪 Run Tests

```bash
python tests.py
```

This runs comprehensive unit and integration tests to verify all models.

---

## 📈 Customize Models

Edit `config.py` to adjust:

```python
# Earthquake risk thresholds
EARTHQUAKE_CONFIG['risk_thresholds'] = {
    'low': 0.2,
    'moderate': 0.4,
    'high': 0.8,
    'critical': 1.0
}

# Flood warning levels
FLOOD_CONFIG['warning_thresholds'] = {
    'green': 0.25,
    'yellow': 0.4,
    'orange': 0.6,
    'red': 1.0
}

# Tsunami threat levels
TSUNAMI_CONFIG['threat_levels'] = {
    'advisory': 0.5,
    'watch': 1.0,
    'warning': 2.0,
    'major_warning': 3.0
}
```

---

## 📂 Project Structure

```
DISPRE_vs/
├── src/
│   ├── data/
│   │   └── data_loader.py        # Download & process data
│   ├── models/
│   │   ├── earthquake.py          # Earthquake model
│   │   ├── flood.py               # Flood model
│   │   └── tsunami.py             # Tsunami model
│   ├── visualization/
│   │   └── visualizer.py          # Maps & reports
│   └── dispre_engine.py           # Main orchestrator
├── data/                           # Input datasets (auto-created)
├── output/                         # Generated reports (auto-created)
├── logs/                           # Log files (auto-created)
├── main.py                         # Main execution script
├── api_server.py                   # REST API server (optional)
├── tests.py                        # Unit tests
├── config.py                       # Configuration
├── requirements.txt                # Python dependencies
└── README.md                       # Full documentation
```

---

## 🔄 Data Integration

### Using Real Data

1. **Download datasets from:**
   - NASA IMERG: `https://gpm1.gesdisc.eosdis.nasa.gov/`
   - Copernicus CDS: `https://cds.climate.copernicus.eu/`
   - USGS Earthquake: `https://earthquake.usgs.gov/earthquakes/feed/`

2. **Place files in `./data/` directory**

3. **Update data loaders in `src/data/data_loader.py`**:
   ```python
   def load_real_rainfall_data(self, filepath):
       # Load your TIFF, NetCDF, or HDF5 file
       pass
   ```

4. **Use in predictions:**
   ```python
   real_rainfall = engine.downloader.load_real_rainfall_data('./data/rainfall.tif')
   ```

---

## ⚠️ Common Issues & Solutions

### Issue: "Module not found" errors
**Solution:**
```bash
# Ensure you're in the right directory
cd DISPRE_vs

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: No output files generated
**Solution:**
```bash
# Create directories manually
mkdir -p data output logs

# Check permissions
# Ensure write access to project directory
```

### Issue: Slow execution
**Solution:**
- Reduce grid resolution in `config.py`
- Use fewer training samples
- Disable visualizations initially
- Run on a machine with more RAM

### Issue: Memory errors with large datasets
**Solution:**
```python
# Process data in chunks
from src.data.data_loader import DataPreprocessor

preprocessor = DataPreprocessor()

# Process smaller regions
for region in regions:
    data = engine.downloader.download_rainfall_data(
        region['lat_min'], region['lat_max'],
        region['lon_min'], region['lon_max']
    )
```

---

## 🎯 Example Workflows

### Workflow 1: Quick Risk Check
```python
engine = DISPREEngine()
engine.train_all_models()

# Quick prediction
result = engine.predict_all_hazards(35.0, 140.0)

# Print alert
print(f"Overall Risk: {max(
    result['earthquake']['risk_score'],
    result['flood']['risk_score'],
    result['tsunami']['risk_assessment']['risk_score']
):.2f}")
```

### Workflow 2: Generate Regional Heatmaps
```python
engine = DISPREEngine()
engine.train_all_models()

# Get regional heatmaps
heatmaps = engine.generate_regional_heatmaps(
    lat_min=30, lat_max=45,
    lon_min=130, lon_max=145,
    resolution=20
)

# Visualize
engine.visualizer.plot_earthquake_risk_map(
    heatmaps['earthquake_risk'],
    heatmaps['grid_latitude'],
    heatmaps['grid_longitude']
)
```

### Workflow 3: Batch Predictions
```python
locations = [
    {'latitude': 35.0, 'longitude': 140.0},
    {'latitude': 36.5, 'longitude': -120.5},
    {'latitude': -8.5, 'longitude': 95.0}
]

for loc in locations:
    result = engine.predict_all_hazards(loc['latitude'], loc['longitude'])
    report = engine.create_full_report(result)
    print(f"Report created for {loc}")
```

---

## 📞 Troubleshooting

### Enable Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

engine = DISPREEngine()
```

### Check Logs
```bash
# View recent logs
tail -f ./logs/dispre.log

# Or on Windows PowerShell
Get-Content ./logs/dispre.log -Tail 50 -Wait
```

### Verify Installation
```bash
# Test imports
python -c "import numpy, pandas, sklearn; print('✓ All packages installed')"

# Test DISPRE
python -c "from src.dispre_engine import DISPREEngine; print('✓ DISPRE ready')"
```

---

## 🚀 Next Steps

1. ✅ Run `python main.py` to test the system
2. ✅ Review generated reports in `./output/`
3. ✅ Customize models in `config.py`
4. ✅ Integrate real datasets
5. ✅ Deploy REST API with `python api_server.py`
6. ✅ Build web dashboard or mobile app using API

---

## 📚 Learning Resources

- **Machine Learning**: Scikit-learn documentation
- **Data Processing**: Pandas & NumPy tutorials
- **Climate Data**: NASA EOSDIS, Copernicus CDS guides
- **Hazard Modeling**: USGS, NOAA technical papers

---

## 💡 Tips & Tricks

✅ **Use smaller regions first** - Test with limited area before global
✅ **Monitor memory** - Large grids need 8+ GB RAM
✅ **Cache results** - Save predictions to avoid recomputation
✅ **Profile code** - Find bottlenecks with `cProfile`
✅ **Parallel processing** - Use `multiprocessing` for batch predictions

---

**Created**: November 2025
**Version**: 1.0.0
**Status**: Ready to Use

Enjoy DISPRE! 🌍
