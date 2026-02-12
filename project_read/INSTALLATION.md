# 🚀 DISPRE Installation & Execution Guide

## Complete Setup Instructions

### Step-by-Step Installation

#### 1️⃣ Download/Extract Project

Ensure you have the complete project in:
```
C:\Users\Arpit Shreya\OneDrive\Desktop\DISPRE_vs\
```

#### 2️⃣ Open Terminal/PowerShell

Navigate to the project:
```powershell
cd "C:\Users\Arpit Shreya\OneDrive\Desktop\DISPRE_vs"
```

#### 3️⃣ Install Python Dependencies

```powershell
# Method 1: Using requirements.txt (RECOMMENDED)
pip install -r requirements.txt

# Method 2: Manual installation (if above fails)
pip install numpy pandas scikit-learn matplotlib seaborn requests scipy
```

**Expected Duration**: 5-15 minutes (depends on internet speed)

---

## 🎯 Quick Execution

### Run the Complete System

```powershell
python main.py
```

**What this does:**
1. ✅ Initializes DISPRE Engine
2. ✅ Trains earthquake, flood, and tsunami models
3. ✅ Runs predictions for 4 test locations:
   - Pacific Ring of Fire (Japan) - 35°N, 140°E
   - Coastal California - 36.5°N, -120.5°E
   - Indian Ocean Region - -8.5°S, 95°E
   - Himalayan Region - 28.5°N, 84°E
4. ✅ Generates comprehensive reports
5. ✅ Creates visualizations

**Expected Output**: 
- Console output with risk assessments
- Files in `./output/` directory
- Logs in `./logs/dispre.log`

---

## 📊 Expected Output

### Console Output
```
============================================================
  DISPRE - Disaster Prediction and Response Engine v1.0
============================================================

🚀 Initializing DISPRE Engine...
   ✓ Engine initialized

🤖 Training prediction models...
   ✓ All models trained

📊 Running multi-hazard predictions...

  • Analyzing: Pacific Ring of Fire (Japan)
    Coordinates: 35.0°, 140.0°
    Risk Assessment:
      - Earthquake: HIGH
      - Flood: MODERATE
      - Tsunami: WATCH
    
  • Analyzing: Coastal California
    ...

✅ DISPRE Execution Complete!

Generated Files:
  ✓ html_report....................  ./output/dispre_report_...html (250.5 KB)
  ✓ risk_comparison.................  ./output/risk_comparison.png (150.2 KB)
  ✓ json_data.......................  ./output/dispre_report_...json (45.3 KB)
```

### Generated Files

#### 1. HTML Report (`./output/dispre_report_*.html`)
- Interactive web page
- Risk assessments for all three disasters
- Color-coded risk levels
- Recommendations and alerts
- **View in**: Any web browser

#### 2. Risk Comparison Chart (`./output/risk_comparison.png`)
- Bar chart comparing risks
- Color-coded by severity
- Visual comparison across disasters

#### 3. JSON Data (`./output/dispre_report_*_data.json`)
- Raw prediction data
- Machine-readable format
- For further analysis or integration

---

## 🔍 Understanding the Output

### Risk Levels Explained

#### Earthquake Risk
```
RISK LEVEL          SCORE       ACTION
─────────────────────────────────────────────────
LOW                 0.0-0.2     Monitor
MODERATE            0.2-0.4     Increase monitoring
ELEVATED            0.4-0.6     Public awareness
HIGH                0.6-0.8     Emergency prep
CRITICAL            0.8-1.0     Activate protocols
```

#### Flood Risk
```
RISK LEVEL          WARNING     ACTION
─────────────────────────────────────────────────
NO FLOOD RISK       GREEN       Normal
LOW                 YELLOW      Prepare
MODERATE            ORANGE      Alert issued
HIGH                ORANGE      Begin evacuation
VERY HIGH           RED         Immediate action
CRITICAL            RED         Full evacuation
```

#### Tsunami Threat
```
THREAT LEVEL        WAVE HEIGHT   ACTION
─────────────────────────────────────────────────
ADVISORY            < 0.5m        Monitor
WATCH               0.5-1.0m      Prepare
WARNING             1.0-2.0m      Evacuate
MAJOR WARNING       > 2.0m        Immediate evacuation
```

---

## 🔧 Customization

### Modify Test Locations

Edit `main.py`, line ~90:

```python
test_locations = [
    {
        'name': 'My Custom Location',
        'latitude': 28.5,      # Change this
        'longitude': 77.5,     # Change this
        'rainfall': 100,       # mm
        'magnitude': 6.5       # Richter scale
    },
    # ... more locations
]
```

### Adjust Model Thresholds

Edit `config.py`:

```python
# Example: Change earthquake critical threshold
EARTHQUAKE_CONFIG['risk_thresholds']['critical'] = 0.7  # Default: 0.8

# Example: Change flood warning thresholds
FLOOD_CONFIG['warning_thresholds']['red'] = 0.8  # Default: 1.0
```

### Enable/Disable Features

Edit `config.py`:

```python
# Disable visualizations
VISUALIZATION_CONFIG['enabled'] = False

# Change output directory
DATA_CONFIG['output_dir'] = 'C:/MyReports'

# Adjust model complexity
EARTHQUAKE_CONFIG['n_estimators'] = 200  # More = slower but more accurate
```

---

## 🧪 Testing the System

### Run Unit Tests

```powershell
python tests.py
```

**What it tests:**
- Earthquake model accuracy
- Flood model predictions
- Tsunami model calculations
- Data processing
- Model integration

### Quick Verification

```powershell
# Test if Python packages are installed
python -c "import numpy; print('✓ NumPy OK')"
python -c "import sklearn; print('✓ Scikit-learn OK')"
python -c "from src.dispre_engine import DISPREEngine; print('✓ DISPRE OK')"
```

---

## 🌐 Using as REST API (Optional)

### Start API Server

```powershell
python api_server.py
```

**Server starts on**: `http://localhost:8000`

### Test API

```powershell
# Get API info
curl http://localhost:8000/

# Get earthquake prediction
curl -X POST http://localhost:8000/predict/earthquake `
  -H "Content-Type: application/json" `
  -d '{"latitude": 35.0, "longitude": 140.0}'

# Get all predictions
curl -X POST http://localhost:8000/predict/all `
  -H "Content-Type: application/json" `
  -d '{"latitude": 35.0, "longitude": 140.0, "rainfall_mm": 75}'
```

---

## 📈 Using as Python Library

### Example 1: Single Location

```python
from src.dispre_engine import DISPREEngine

engine = DISPREEngine()
engine.train_all_models()

# Predict
result = engine.predict_all_hazards(
    latitude=35.0,
    longitude=140.0,
    rainfall_mm=75
)

# Print results
print(f"Earthquake Risk: {result['earthquake']['risk_level']}")
print(f"Flood Risk: {result['flood']['risk_level']}")
print(f"Tsunami Threat: {result['tsunami']['risk_assessment']['threat_level']}")
```

### Example 2: Batch Predictions

```python
locations = [
    (35.0, 140.0),    # Japan
    (36.5, -120.5),   # California
    (-8.5, 95.0)      # Indonesia
]

engine = DISPREEngine()
engine.train_all_models()

for lat, lon in locations:
    result = engine.predict_all_hazards(lat, lon)
    print(f"Location ({lat}, {lon}): {result}")
```

### Example 3: Regional Heatmaps

```python
# Generate risk maps for region
heatmaps = engine.generate_regional_heatmaps(
    lat_min=30, lat_max=45,
    lon_min=130, lon_max=145,
    resolution=20
)

# Use heatmaps for visualization or analysis
earthquake_risk_grid = heatmaps['earthquake_risk']
flood_risk_grid = heatmaps['flood_risk']
tsunami_hazard_grid = heatmaps['tsunami_hazard']
```

---

## 🚨 Emergency Alert System

### Automatic Alert Generation

When critical risk is detected:

```python
engine = DISPREEngine()
predictions = engine.predict_all_hazards(35.0, 140.0)

# Check for critical alerts
alerts = engine.run_emergency_alert(predictions)

if alerts['alert_count'] > 0:
    print("⚠️ CRITICAL ALERTS DETECTED!")
    for alert in alerts['active_alerts']:
        print(f"[{alert['disaster_type']}] {alert['message']}")
```

---

## 📊 Data Integration

### Using Real Climate Data

1. **Download data** from:
   - NASA IMERG (rainfall): https://gpm.nasa.gov/
   - Copernicus CDS (climate): https://cds.climate.copernicus.eu/
   - USGS (earthquakes): https://earthquake.usgs.gov/
   - NOAA (forecasts): https://www.ncei.noaa.gov/

2. **Place files** in `./data/` directory

3. **Update data loader** in `src/data/data_loader.py`:
   ```python
   def load_real_rainfall(filepath):
       # Load your GeoTIFF, NetCDF, or HDF5 file
       pass
   ```

4. **Use in predictions**:
   ```python
   real_data = engine.downloader.load_real_rainfall('./data/rainfall.tif')
   ```

---

## ⚠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'numpy'"

**Solution**:
```powershell
pip install -r requirements.txt --upgrade
```

### Issue: "Permission denied" errors

**Solution** (Windows):
```powershell
# Run PowerShell as Administrator
# Then retry the command
```

### Issue: "No output files generated"

**Solution**:
```powershell
# Ensure directories exist
mkdir data
mkdir output
mkdir logs

# Check write permissions
cd output
echo "test" > test.txt
del test.txt
```

### Issue: Slow execution

**Solution**:
- Reduce grid resolution in `config.py`
- Use fewer training samples
- Close other applications
- Ensure sufficient RAM (8+ GB recommended)

### Issue: Out of memory

**Solution**:
```python
# Process smaller regions
from src.dispre_engine import DISPREEngine

engine = DISPREEngine()

# Use lower resolution
heatmaps = engine.generate_regional_heatmaps(
    lat_min=30, lat_max=40,
    lon_min=130, lon_max=140,
    resolution=10  # Lower = less memory
)
```

---

## 📚 Project Files Explained

```
DISPRE_vs/
├── main.py                    ← Run this to execute system
├── api_server.py              ← Optional REST API
├── tests.py                   ← Run unit tests
├── setup.py                   ← Initial setup script
│
├── src/
│   ├── dispre_engine.py       ← Main orchestrator
│   ├── data/
│   │   └── data_loader.py     ← Download & process climate data
│   ├── models/
│   │   ├── earthquake.py      ← Earthquake prediction
│   │   ├── flood.py           ← Flood prediction
│   │   └── tsunami.py         ← Tsunami prediction
│   └── visualization/
│       └── visualizer.py      ← Maps & charts
│
├── data/                      ← Input datasets
├── output/                    ← Generated reports
├── logs/                      ← Application logs
│
├── requirements.txt           ← Python packages to install
├── config.py                  ← Configuration settings
├── README.md                  ← Full documentation
├── QUICKSTART.md             ← Quick reference
└── INSTALLATION.md           ← This file
```

---

## ✅ Verification Checklist

Before running, ensure:

- [ ] Python 3.7+ installed (`python --version`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Project directory accessible
- [ ] 500 MB+ free disk space
- [ ] 8+ GB RAM available
- [ ] Internet connection (for optional real data download)

---

## 🎯 Next Steps

1. **Run the system**:
   ```powershell
   python main.py
   ```

2. **Review generated reports**:
   - Open `./output/dispre_report_*.html` in web browser
   - Check `./output/risk_comparison.png` for visual summary
   - Examine `./output/dispre_report_*.json` for raw data

3. **Customize for your needs**:
   - Edit test locations in `main.py`
   - Adjust thresholds in `config.py`
   - Integrate real datasets

4. **Explore advanced features**:
   - Run REST API with `python api_server.py`
   - Run tests with `python tests.py`
   - Review detailed documentation in `README.md`

---

## 💡 Tips

✅ Start with provided test locations first
✅ Check `./logs/dispre.log` for detailed execution info
✅ Use smaller regions to test before going global
✅ Save predictions for offline analysis
✅ Monitor memory usage with large grids

---

## 🆘 Get Help

**Issue Location**: `./logs/dispre.log`
**Configuration**: `config.py`
**Documentation**: `README.md` and `QUICKSTART.md`
**Code Examples**: `main.py` and `tests.py`

---

**DISPRE v1.0** | Disaster Prediction and Response Engine
**Created**: November 2025 | **Status**: Ready to Use 🚀

