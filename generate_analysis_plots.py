#!/usr/bin/env python3
"""
Advanced Analysis Plotting Script for DISPRE Simulation Results
Generates comprehensive visualizations of disaster predictions
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10

def load_simulation_results():
    """Load all simulation results from output directory"""
    try:
        with open('./output/dispre_report_Pacific_Ring_of_Fire_(Japan)_data.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading results: {e}")
        return None

def create_disaster_overview_plot(data):
    """Create overview of all three disaster predictions"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('DISPRE - Multi-Hazard Disaster Prediction Analysis', 
                 fontsize=18, fontweight='bold', y=0.995)
    
    # Earthquake Risk Analysis
    ax = axes[0, 0]
    eq_data = data['earthquake']
    categories = ['Risk Score', 'Prob M>5', 'Prob M>7']
    values = [eq_data['risk_score'], eq_data['probability_magnitude_gt_5'], 
              eq_data['probability_magnitude_gt_7']]
    colors = ['#FF6B6B', '#FFA500', '#FFD700']
    
    bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=2)
    ax.set_ylabel('Risk Level / Probability', fontsize=12, fontweight='bold')
    ax.set_title('🏔️ EARTHQUAKE RISK ASSESSMENT', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Add risk level annotation
    eq_level = eq_data['risk_level']
    ax.text(0.5, 0.95, f"Risk Level: {eq_level}", transform=ax.transAxes,
            ha='center', va='top', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Flood Risk Analysis
    ax = axes[0, 1]
    flood_data = data['flood']
    flood_metrics = ['Risk Score', 'Water Depth (m)', 'Flood Prob']
    flood_values = [flood_data['risk_score'], flood_data['predicted_water_depth_m']/10, 
                    flood_data['flood_probability']]
    colors_flood = ['#FF0000', '#FF6B6B', '#FF8C8C']
    
    bars = ax.bar(flood_metrics, flood_values, color=colors_flood, edgecolor='black', linewidth=2)
    ax.set_ylabel('Value / Normalized', fontsize=12, fontweight='bold')
    ax.set_title('💧 FLOOD RISK ASSESSMENT', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 1.2)
    ax.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, flood_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
    
    flood_level = flood_data['risk_level']
    ax.text(0.5, 0.95, f"Risk Level: {flood_level}", transform=ax.transAxes,
            ha='center', va='top', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.7))
    
    # Tsunami Risk Analysis
    ax = axes[1, 0]
    tsunami_data = data['tsunami']
    tsunami_metrics = ['Risk Score', 'Wave Height\n(scaled)', 'Vulnerable\nArea (%)']
    tsunami_values = [tsunami_data['risk_assessment']['risk_score'],
                      min(tsunami_data['tsunami_wave']['maximum_height_m'] * 1000, 1),
                      tsunami_data['risk_assessment']['coastal_vulnerability']]
    colors_tsunami = ['#4169E1', '#87CEEB', '#00BFFF']
    
    bars = ax.bar(tsunami_metrics, tsunami_values, color=colors_tsunami, edgecolor='black', linewidth=2)
    ax.set_ylabel('Value / Score', fontsize=12, fontweight='bold')
    ax.set_title('🌊 TSUNAMI RISK ASSESSMENT', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 1.2)
    ax.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, tsunami_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{val:.2f}', ha='center', va='bottom', fontweight='bold')
    
    threat_level = tsunami_data['risk_assessment']['threat_level']
    ax.text(0.5, 0.95, f"Threat Level: {threat_level}", transform=ax.transAxes,
            ha='center', va='top', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='cyan', alpha=0.7))
    
    # Summary Comparison
    ax = axes[1, 1]
    ax.axis('off')
    
    # Create summary text
    summary_text = f"""
    LOCATION: {data['location']['latitude']:.1f}°, {data['location']['longitude']:.1f}°
    TIME: {data['timestamp']}
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    🏔️  EARTHQUAKE
    ├─ Risk Score: {eq_data['risk_score']:.3f}
    ├─ Level: {eq_data['risk_level']}
    ├─ Expected Magnitude: {eq_data['expected_magnitude']:.1f}
    ├─ Magnitude Range: {eq_data['predicted_magnitude_range'][0]:.1f} - {eq_data['predicted_magnitude_range'][1]:.1f}
    ├─ Tectonic Zone: {eq_data['tectonic_zone']}
    └─ Depth: {eq_data['depth_km']} km
    
    💧 FLOOD
    ├─ Risk Score: {flood_data['risk_score']:.3f}
    ├─ Level: {flood_data['risk_level']}
    ├─ Water Depth: {flood_data['predicted_water_depth_m']:.2f} m
    ├─ Warning: {flood_data['warning_level']}
    ├─ Affected Area: {flood_data['affected_area_sq_km']:.2f} km²
    └─ Rainfall: {flood_data['rainfall_mm']:.0f} mm
    
    🌊 TSUNAMI
    ├─ Risk Score: {tsunami_data['risk_assessment']['risk_score']:.3f}
    ├─ Threat Level: {tsunami_data['risk_assessment']['threat_level']}
    ├─ Max Wave Height: {tsunami_data['tsunami_wave']['maximum_height_m']:.4f} m
    ├─ Wave Speed: {tsunami_data['tsunami_wave']['estimated_speed_ms']:.2f} m/s
    ├─ Travel Time: {tsunami_data['timing']['travel_time_hours']:.2f} hours
    └─ Escape Time: {tsunami_data['timing']['time_to_escape_minutes']:.1f} minutes
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    OVERALL RISK: {data['summary']['overall_risk_level']}
    """
    
    ax.text(0.05, 0.95, summary_text, transform=ax.transAxes,
            fontfamily='monospace', fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('./output/disaster_analysis_overview.png', dpi=300, bbox_inches='tight')
    logger.info('✓ Saved: disaster_analysis_overview.png')
    plt.close()

def create_risk_magnitude_plot(data):
    """Create risk vs magnitude scatter plot"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    eq_data = data['earthquake']
    flood_data = data['flood']
    tsunami_data = data['tsunami']
    
    # Create scatter plot
    disasters = ['Earthquake', 'Flood', 'Tsunami']
    risk_scores = [eq_data['risk_score'], flood_data['risk_score'], 
                   tsunami_data['risk_assessment']['risk_score']]
    impacts = [eq_data['expected_magnitude'] / 10,  # Normalize magnitude
               flood_data['predicted_water_depth_m'],
               tsunami_data['tsunami_wave']['maximum_height_m']]
    colors = ['#FF6B6B', '#FF0000', '#4169E1']
    sizes = [1000, 1200, 1100]
    
    scatter = ax.scatter(disasters, risk_scores, c=colors, s=sizes, alpha=0.7, 
                        edgecolors='black', linewidth=2)
    
    ax.set_ylabel('Risk Score (0-1)', fontsize=13, fontweight='bold')
    ax.set_title('Risk Score Comparison Across Disaster Types', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 1.1)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, (disaster, risk) in enumerate(zip(disasters, risk_scores)):
        ax.text(i, risk + 0.05, f'{risk:.3f}', ha='center', fontweight='bold', fontsize=11)
    
    # Add risk level lines
    ax.axhline(y=0.2, color='green', linestyle='--', alpha=0.5, label='LOW')
    ax.axhline(y=0.4, color='yellow', linestyle='--', alpha=0.5, label='MODERATE')
    ax.axhline(y=0.6, color='orange', linestyle='--', alpha=0.5, label='ELEVATED')
    ax.axhline(y=0.8, color='red', linestyle='--', alpha=0.5, label='HIGH')
    
    ax.legend(loc='upper right', fontsize=11)
    plt.tight_layout()
    plt.savefig('./output/risk_magnitude_comparison.png', dpi=300, bbox_inches='tight')
    logger.info('✓ Saved: risk_magnitude_comparison.png')
    plt.close()

def create_timeline_plot(data):
    """Create timing and arrival time visualization"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    tsunami_data = data['tsunami']
    timing = tsunami_data['timing']
    
    # Create timeline
    events = ['Current Time\n(T+0h)', 
              'Tsunami\nArrival', 
              'Maximum\nWave',
              'Peak\nInundation']
    
    times = [0, 
             timing['travel_time_hours'],
             timing['travel_time_hours'] + 0.5,
             timing['travel_time_hours'] + 1.5]
    
    wave_heights = [0,
                    tsunami_data['tsunami_wave']['maximum_height_m'] * 100,
                    tsunami_data['tsunami_wave']['maximum_height_m'] * 100 * 0.8,
                    tsunami_data['tsunami_wave']['maximum_height_m'] * 100 * 0.5]
    
    colors_timeline = ['green', 'red', 'orange', 'yellow']
    
    ax.plot(times, wave_heights, 'o-', linewidth=3, markersize=15, color='darkblue')
    
    for i, (event, time, height, color) in enumerate(zip(events, times, wave_heights, colors_timeline)):
        ax.scatter(time, height, s=500, c=color, edgecolors='black', linewidth=2, zorder=5)
        ax.text(time, height + 0.02, event, ha='center', fontweight='bold', fontsize=11)
    
    ax.set_xlabel('Time (Hours)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Wave Height (cm)', fontsize=13, fontweight='bold')
    ax.set_title('Tsunami Timeline and Wave Propagation', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.05, max(wave_heights) + 0.05)
    
    # Add escape time annotation
    escape_time = timing['time_to_escape_minutes']
    ax.axvline(x=escape_time/60, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(escape_time/60, max(wave_heights) * 0.9, f'Escape Window\n{escape_time:.0f} min', 
            ha='center', fontweight='bold', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('./output/tsunami_timeline.png', dpi=300, bbox_inches='tight')
    logger.info('✓ Saved: tsunami_timeline.png')
    plt.close()

def create_hazard_heatmap(data):
    """Create hazard risk heatmap"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create hazard matrix
    hazards = ['Earthquake', 'Flood', 'Tsunami']
    risk_factors = [
        [data['earthquake']['risk_score'],
         data['earthquake']['probability_magnitude_gt_5'],
         data['earthquake']['probability_magnitude_gt_7']],
        
        [data['flood']['risk_score'],
         data['flood']['flood_probability'],
         data['flood']['predicted_water_depth_m'] / 10],
        
        [data['tsunami']['risk_assessment']['risk_score'],
         data['tsunami']['risk_assessment']['coastal_vulnerability'],
         min(data['tsunami']['tsunami_wave']['maximum_height_m'] * 1000, 1)]
    ]
    
    risk_matrix = np.array(risk_factors)
    
    factor_names = ['Primary Risk', 'Secondary Risk', 'Impact Factor']
    
    im = ax.imshow(risk_matrix, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=1)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(factor_names)))
    ax.set_yticks(np.arange(len(hazards)))
    ax.set_xticklabels(factor_names, fontsize=11, fontweight='bold')
    ax.set_yticklabels(hazards, fontsize=11, fontweight='bold')
    
    # Rotate the tick labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add text annotations
    for i in range(len(hazards)):
        for j in range(len(factor_names)):
            text = ax.text(j, i, f'{risk_matrix[i, j]:.2f}',
                          ha="center", va="center", color="black", fontweight='bold', fontsize=12)
    
    ax.set_title('Multi-Hazard Risk Factor Heatmap', fontsize=14, fontweight='bold')
    fig.colorbar(im, ax=ax, label='Risk Level (0-1)')
    
    plt.tight_layout()
    plt.savefig('./output/hazard_heatmap.png', dpi=300, bbox_inches='tight')
    logger.info('✓ Saved: hazard_heatmap.png')
    plt.close()

def create_statistical_summary(data):
    """Create statistical summary visualization"""
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    eq_data = data['earthquake']
    flood_data = data['flood']
    tsunami_data = data['tsunami']
    
    # Earthquake magnitude distribution
    ax1 = fig.add_subplot(gs[0, 0])
    mag_range = np.linspace(eq_data['predicted_magnitude_range'][0], 
                            eq_data['predicted_magnitude_range'][1], 50)
    # Simple normal distribution around expected magnitude
    probs = (1 / (2 * 1)) * np.exp(-((mag_range - eq_data['expected_magnitude']) ** 2) / (2 * 1 ** 2))
    ax1.fill_between(mag_range, probs, alpha=0.7, color='#FF6B6B')
    ax1.axvline(eq_data['expected_magnitude'], color='red', linestyle='--', linewidth=2)
    ax1.set_xlabel('Magnitude', fontweight='bold')
    ax1.set_ylabel('Probability', fontweight='bold')
    ax1.set_title('Earthquake Magnitude Distribution', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Flood water depth by area
    ax2 = fig.add_subplot(gs[0, 1])
    areas = np.linspace(0, flood_data['affected_area_sq_km'], 50)
    depths = flood_data['predicted_water_depth_m'] * (1 - (areas / flood_data['affected_area_sq_km']) ** 1.5)
    ax2.fill_between(areas, depths, alpha=0.7, color='#FF0000')
    ax2.set_xlabel('Area (km²)', fontweight='bold')
    ax2.set_ylabel('Water Depth (m)', fontweight='bold')
    ax2.set_title('Flood Inundation Extent', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Tsunami wave propagation
    ax3 = fig.add_subplot(gs[1, 0])
    distances = np.linspace(0, tsunami_data['timing']['travel_time_hours'] * 
                           tsunami_data['tsunami_wave']['estimated_speed_ms'] * 3.6, 50)
    heights = tsunami_data['tsunami_wave']['maximum_height_m'] * np.exp(-distances / 100000)
    ax3.plot(distances / 1000, heights * 100, linewidth=2, color='#4169E1')
    ax3.fill_between(distances / 1000, heights * 100, alpha=0.3, color='#4169E1')
    ax3.set_xlabel('Distance (km)', fontweight='bold')
    ax3.set_ylabel('Wave Height (cm)', fontweight='bold')
    ax3.set_title('Tsunami Wave Attenuation', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Risk distribution
    ax4 = fig.add_subplot(gs[1, 1])
    risk_data = {
        'Earthquake': eq_data['risk_score'],
        'Flood': flood_data['risk_score'],
        'Tsunami': tsunami_data['risk_assessment']['risk_score']
    }
    colors = ['#FF6B6B', '#FF0000', '#4169E1']
    wedges, texts, autotexts = ax4.pie(list(risk_data.values()), labels=list(risk_data.keys()),
                                        autopct='%1.1f%%', colors=colors, startangle=90)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax4.set_title('Risk Score Distribution', fontweight='bold')
    
    # Recommendation summary
    ax5 = fig.add_subplot(gs[2, :])
    ax5.axis('off')
    
    recommendations = f"""
    IMMEDIATE ACTIONS & RECOMMENDATIONS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    🏔️  EARTHQUAKE:
         {eq_data['recommendation']}
    
    💧 FLOOD:
         {flood_data['recommendation']}
    
    🌊 TSUNAMI:
         {tsunami_data['recommendation']}
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    
    ax5.text(0.05, 0.95, recommendations, transform=ax5.transAxes,
            fontfamily='monospace', fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    fig.suptitle('Statistical Analysis and Risk Assessment Summary', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig('./output/statistical_summary.png', dpi=300, bbox_inches='tight')
    logger.info('✓ Saved: statistical_summary.png')
    plt.close()

def main():
    """Main execution"""
    logger.info("=" * 80)
    logger.info("DISPRE Advanced Analysis Plot Generator")
    logger.info("=" * 80)
    
    # Load data
    data = load_simulation_results()
    if not data:
        logger.error("Failed to load simulation results")
        return
    
    logger.info(f"Loaded simulation data for location: ({data['location']['latitude']}, {data['location']['longitude']})")
    logger.info("\nGenerating advanced visualization plots...")
    
    # Generate plots
    create_disaster_overview_plot(data)
    create_risk_magnitude_plot(data)
    create_timeline_plot(data)
    create_hazard_heatmap(data)
    create_statistical_summary(data)
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ ALL PLOTS GENERATED SUCCESSFULLY")
    logger.info("=" * 80)
    logger.info("\nGenerated files:")
    logger.info("  • disaster_analysis_overview.png")
    logger.info("  • risk_magnitude_comparison.png")
    logger.info("  • tsunami_timeline.png")
    logger.info("  • hazard_heatmap.png")
    logger.info("  • statistical_summary.png")
    logger.info("\nAll files saved to: ./output/")

if __name__ == "__main__":
    main()
