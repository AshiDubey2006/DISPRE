"""
Visualization and Reporting Module
Creates maps, charts, and reports for disaster predictions
"""

import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
from typing import Dict, List, Optional
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class DisasterVisualizer:
    """Create visualizations for disaster predictions"""
    
    def __init__(self, output_dir: str = './output'):
        """Initialize visualizer"""
        self.output_dir = output_dir
        self.cmap_risk = 'RdYlGn_r'  # Red-Yellow-Green reversed
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 10)
    
    def plot_earthquake_risk_map(self, risk_grid: np.ndarray, 
                                grid_lat: np.ndarray, grid_lon: np.ndarray,
                                earthquake_data: List[Dict] = None,
                                title: str = "Earthquake Risk Assessment") -> str:
        """
        Create earthquake risk heatmap
        
        Args:
            risk_grid: 2D array of risk scores
            grid_lat, grid_lon: Grid coordinates
            earthquake_data: Optional list of recent earthquakes
            title: Plot title
            
        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Plot risk grid
        im = ax.contourf(grid_lon, grid_lat, risk_grid, levels=20, cmap=self.cmap_risk)
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Earthquake Risk Score (0-1)', fontsize=12)
        
        # Plot recent earthquakes if provided
        if earthquake_data:
            for eq in earthquake_data:
                if eq['magnitude'] >= 5.0:
                    size = (eq['magnitude'] - 4) * 100
                    ax.scatter(eq['longitude'], eq['latitude'], 
                             s=size, c='red', marker='X', 
                             edgecolors='black', linewidth=1, zorder=5,
                             label=f"M{eq['magnitude']}" if eq == earthquake_data[0] else "")
        
        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Save figure
        filepath = f"{self.output_dir}/earthquake_risk_map.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved earthquake risk map to {filepath}")
        return filepath
    
    def plot_flood_risk_map(self, risk_grid: np.ndarray,
                           rainfall_grid: np.ndarray,
                           grid_lat: np.ndarray, grid_lon: np.ndarray,
                           title: str = "Flood Risk Assessment") -> str:
        """
        Create flood risk heatmap with rainfall overlay
        """
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        
        # Flood risk
        im1 = axes[0].contourf(grid_lon, grid_lat, risk_grid, 
                              levels=20, cmap='Blues')
        cbar1 = plt.colorbar(im1, ax=axes[0])
        cbar1.set_label('Flood Risk Score', fontsize=11)
        axes[0].set_title('Flood Risk Distribution', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Longitude')
        axes[0].set_ylabel('Latitude')
        
        # Rainfall
        im2 = axes[1].contourf(grid_lon, grid_lat, rainfall_grid,
                              levels=20, cmap='viridis')
        cbar2 = plt.colorbar(im2, ax=axes[1])
        cbar2.set_label('Rainfall (mm)', fontsize=11)
        axes[1].set_title('Rainfall Distribution', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Longitude')
        axes[1].set_ylabel('Latitude')
        
        fig.suptitle(title, fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        filepath = f"{self.output_dir}/flood_risk_map.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved flood risk map to {filepath}")
        return filepath
    
    def plot_tsunami_hazard_map(self, hazard_grid: np.ndarray,
                               lat_grid: np.ndarray, lon_grid: np.ndarray,
                               title: str = "Tsunami Hazard Map") -> str:
        """
        Create tsunami wave height hazard map
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Wave height levels with appropriate colors
        levels = [0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
        colors = ['white', 'yellow', 'orange', 'red', 'darkred', 'maroon']
        
        im = ax.contourf(lon_grid, lat_grid, hazard_grid, 
                         levels=levels, colors=colors, extend='max')
        
        cbar = plt.colorbar(im, ax=ax, label='Wave Height (m)')
        
        # Add contour lines
        cs = ax.contour(lon_grid, lat_grid, hazard_grid, 
                       levels=[0.5, 1.0, 2.0, 3.0], colors='black', 
                       linewidths=0.5, alpha=0.5)
        ax.clabel(cs, inline=True, fontsize=8)
        
        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        filepath = f"{self.output_dir}/tsunami_hazard_map.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved tsunami hazard map to {filepath}")
        return filepath
    
    def plot_risk_comparison(self, predictions: Dict) -> str:
        """
        Compare risk levels across three disaster types
        """
        disasters = ['Earthquake', 'Flood', 'Tsunami']
        risk_scores = [
            predictions.get('earthquake', {}).get('risk_score', 0),
            predictions.get('flood', {}).get('risk_score', 0),
            predictions.get('tsunami', {}).get('risk_assessment', {}).get('risk_score', 0)
        ]
        
        colors = ['#ff6b6b' if r > 0.6 else '#ffd93d' if r > 0.3 else '#6bcf7f' 
                 for r in risk_scores]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(disasters, risk_scores, color=colors, edgecolor='black', linewidth=2)
        
        # Add risk level labels
        risk_labels = []
        for score in risk_scores:
            if score < 0.2:
                risk_labels.append('LOW')
            elif score < 0.4:
                risk_labels.append('MODERATE')
            elif score < 0.6:
                risk_labels.append('ELEVATED')
            elif score < 0.8:
                risk_labels.append('HIGH')
            else:
                risk_labels.append('CRITICAL')
        
        # Add value labels on bars
        for bar, score, label in zip(bars, risk_scores, risk_labels):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{score:.2f}\n{label}',
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax.set_ylabel('Risk Score (0-1)', fontsize=12)
        ax.set_title('Multi-Hazard Risk Comparison', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 1.1)
        ax.axhline(y=0.6, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Critical Threshold')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        filepath = f"{self.output_dir}/risk_comparison.png"
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved risk comparison chart to {filepath}")
        return filepath
    
    def plot_temporal_forecast(self, forecast_data: pd.DataFrame, 
                              disaster_type: str = 'Flood') -> str:
        """
        Plot temporal forecast for a disaster type
        """
        fig, axes = plt.subplots(2, 1, figsize=(14, 8))
        
        # Risk evolution
        axes[0].plot(forecast_data.index, forecast_data.get('risk_score', []), 
                    color='red', linewidth=2, marker='o', markersize=6)
        axes[0].fill_between(forecast_data.index, forecast_data.get('risk_score', []), 
                           alpha=0.3, color='red')
        axes[0].axhline(y=0.6, color='darkred', linestyle='--', linewidth=2, alpha=0.7, label='Warning Threshold')
        axes[0].set_ylabel('Risk Score', fontsize=11)
        axes[0].set_title(f'{disaster_type} Risk Forecast', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        axes[0].set_ylim(0, 1)
        
        # Impact metrics
        impact_cols = [col for col in forecast_data.columns if 'impact' in col.lower()]
        if impact_cols:
            for col in impact_cols[:2]:
                axes[1].plot(forecast_data.index, forecast_data[col], 
                           marker='o', markersize=5, linewidth=2, label=col)
            axes[1].set_ylabel('Impact Magnitude', fontsize=11)
            axes[1].set_xlabel('Time', fontsize=11)
            axes[1].set_title('Impact Evolution', fontsize=12, fontweight='bold')
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filepath = f"{self.output_dir}/temporal_forecast_{disaster_type.lower()}.png"
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Saved temporal forecast to {filepath}")
        return filepath
    
    def create_html_report(self, predictions: Dict, output_filename: str = 'disaster_report.html') -> str:
        """
        Create comprehensive HTML report
        """
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DISPRE - Disaster Prediction Report</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                }}
                h1 {{
                    color: #333;
                    border-bottom: 4px solid #667eea;
                    padding-bottom: 10px;
                    text-align: center;
                }}
                h2 {{
                    color: #667eea;
                    margin-top: 30px;
                    border-left: 4px solid #667eea;
                    padding-left: 15px;
                }}
                .risk-box {{
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 15px 0;
                    background: #f9f9f9;
                }}
                .risk-high {{
                    border-left: 5px solid #ff6b6b;
                    background: #ffe5e5;
                }}
                .risk-moderate {{
                    border-left: 5px solid #ffd93d;
                    background: #fff9e5;
                }}
                .risk-low {{
                    border-left: 5px solid #6bcf7f;
                    background: #e5ffe5;
                }}
                .metric {{
                    display: inline-block;
                    width: 45%;
                    margin: 10px 2%;
                    padding: 15px;
                    background: white;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                }}
                .timestamp {{
                    text-align: center;
                    color: #999;
                    font-size: 12px;
                    margin-top: 20px;
                    border-top: 1px solid #ddd;
                    padding-top: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #667eea;
                    color: white;
                }}
                .recommendation {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌍 DISPRE - Disaster Prediction Report</h1>
                
                <h2>Executive Summary</h2>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        """
        
        # Earthquake section
        if 'earthquake' in predictions:
            eq = predictions['earthquake']
            risk_level = eq.get('risk_level', 'UNKNOWN')
            risk_class = 'risk-high' if risk_level in ['HIGH', 'CRITICAL'] else 'risk-moderate' if risk_level in ['MODERATE', 'ELEVATED'] else 'risk-low'
            
            html_content += f"""
                <h2>🌍 Earthquake Assessment</h2>
                <div class="risk-box {risk_class}">
                    <h3>Risk Level: {risk_level}</h3>
                    <p><strong>Risk Score:</strong> {eq.get('risk_score', 0):.3f}</p>
                    <p><strong>Tectonic Zone:</strong> {eq.get('tectonic_zone', 'Unknown')}</p>
                    <div class="metric">
                        <strong>Expected Magnitude:</strong><br>
                        {eq.get('expected_magnitude', 0):.1f}
                    </div>
                    <div class="metric">
                        <strong>Probability Mag > 5.0:</strong><br>
                        {eq.get('probability_magnitude_gt_5', 0)*100:.1f}%
                    </div>
                    <div class="metric">
                        <strong>Probability Mag > 7.0:</strong><br>
                        {eq.get('probability_magnitude_gt_7', 0)*100:.1f}%
                    </div>
                    <div class="recommendation">
                        <strong>🚨 Recommendation:</strong> {eq.get('recommendation', 'N/A')}
                    </div>
                </div>
            """
        
        # Flood section
        if 'flood' in predictions:
            fl = predictions['flood']
            risk_level = fl.get('risk_level', 'UNKNOWN')
            risk_class = 'risk-high' if 'HIGH' in risk_level or 'CRITICAL' in risk_level else 'risk-moderate' if 'MODERATE' in risk_level else 'risk-low'
            
            html_content += f"""
                <h2>💧 Flood Assessment</h2>
                <div class="risk-box {risk_class}">
                    <h3>Risk Level: {risk_level}</h3>
                    <p><strong>Risk Score:</strong> {fl.get('risk_score', 0):.3f}</p>
                    <p><strong>Warning Level:</strong> {fl.get('warning_level', 'N/A')}</p>
                    <div class="metric">
                        <strong>Rainfall:</strong><br>
                        {fl.get('rainfall_mm', 0):.1f} mm
                    </div>
                    <div class="metric">
                        <strong>Predicted Water Depth:</strong><br>
                        {fl.get('predicted_water_depth_m', 0):.2f} m
                    </div>
                    <div class="metric">
                        <strong>Flood Probability:</strong><br>
                        {fl.get('flood_probability', 0)*100:.1f}%
                    </div>
                    <div class="metric">
                        <strong>Affected Area:</strong><br>
                        {fl.get('affected_area_sq_km', 0):.1f} km²
                    </div>
                    <div class="recommendation">
                        <strong>🚨 Recommendation:</strong> {fl.get('recommendation', 'N/A')}
                    </div>
                </div>
            """
        
        # Tsunami section
        if 'tsunami' in predictions:
            ts = predictions['tsunami']
            risk_level = ts.get('risk_assessment', {}).get('risk_level', 'UNKNOWN')
            risk_class = 'risk-high' if 'CRITICAL' in risk_level or 'WARNING' in risk_level else 'risk-moderate' if 'WATCH' in risk_level else 'risk-low'
            
            wave_height = ts.get('tsunami_wave', {}).get('maximum_height_m', 0)
            
            html_content += f"""
                <h2>🌊 Tsunami Assessment</h2>
                <div class="risk-box {risk_class}">
                    <h3>Threat Level: {ts.get('risk_assessment', {}).get('threat_level', 'UNKNOWN')}</h3>
                    <p><strong>Risk Score:</strong> {ts.get('risk_assessment', {}).get('risk_score', 0):.3f}</p>
                    <div class="metric">
                        <strong>Maximum Wave Height:</strong><br>
                        {wave_height:.2f} m
                    </div>
                    <div class="metric">
                        <strong>Estimated Speed:</strong><br>
                        {ts.get('tsunami_wave', {}).get('estimated_speed_ms', 0):.1f} m/s
                    </div>
                    <div class="metric">
                        <strong>Travel Time to Coast:</strong><br>
                        {ts.get('timing', {}).get('travel_time_hours', 0):.1f} hours
                    </div>
                    <div class="metric">
                        <strong>Inundation Depth:</strong><br>
                        {ts.get('coastal_impact', {}).get('estimated_inundation_depth_m', 0):.2f} m
                    </div>
                    <div class="recommendation">
                        <strong>🚨 Recommendation:</strong> {ts.get('recommendation', 'N/A')}
                    </div>
                </div>
            """
        
        html_content += """
                <div class="timestamp">
                    <p>This report is automatically generated by DISPRE v1.0</p>
                    <p>For emergency: Contact local disaster management authorities immediately</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        filepath = f"{self.output_dir}/{output_filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Saved HTML report to {filepath}")
        return filepath
