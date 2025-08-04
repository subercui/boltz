#!/usr/bin/env python3
"""
Single Protein Demo Visualization Script
Creates presentation-ready visualizations for single protein structure prediction
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Set style for publication-quality figures
plt.style.use('default')
sns.set_palette("husl")

def load_confidence_data(json_path):
    """Load confidence scores from Boltz output"""
    with open(json_path, 'r') as f:
        return json.load(f)

def create_single_protein_summary(confidence_data, output_path):
    """Create a summary visualization for single protein prediction"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left panel: Main confidence metrics
    main_metrics = {
        'Overall\nConfidence': confidence_data['confidence_score'],
        'Protein Structure\n(PTM)': confidence_data['ptm'],
        'Structure Quality\n(pLDDT)': confidence_data['complex_plddt'],
        'Distance Error\n(PDE)': confidence_data['complex_pde']
    }
    
    bars1 = ax1.bar(main_metrics.keys(), [v*100 for v in main_metrics.values()],
                   color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], alpha=0.8,
                   edgecolor='black', linewidth=1)
    
    ax1.set_ylabel('Score (%)', fontsize=14, fontweight='bold')
    ax1.set_title('Single Protein Prediction Quality', fontsize=16, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, score in zip(bars1, main_metrics.values()):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{score*100:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Right panel: Quality interpretation
    score = confidence_data['confidence_score'] * 100
    
    # Create a gauge-style visualization
    theta = np.linspace(0, np.pi, 100)
    r = np.ones_like(theta)
    
    # Color zones
    colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
    boundaries = [0, 50, 70, 85, 95, 100]
    
    for i in range(len(boundaries)-1):
        mask = (theta >= (boundaries[i]/100) * np.pi) & (theta <= (boundaries[i+1]/100) * np.pi)
        ax2.fill_between(theta[mask], 0, r[mask], color=colors[i], alpha=0.3)
    
    # Plot the score indicator
    score_angle = (score/100) * np.pi
    ax2.plot([score_angle, score_angle], [0, 1], 'black', linewidth=4)
    ax2.plot(score_angle, 1, 'ko', markersize=10)
    
    ax2.set_xlim(0, np.pi)
    ax2.set_ylim(0, 1.2)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title('Confidence Assessment', fontsize=16, fontweight='bold')
    
    # Add labels
    ax2.text(0, -0.1, 'Poor\n(0-50%)', ha='left', va='top', fontsize=10, fontweight='bold')
    ax2.text(np.pi/4, -0.1, 'Fair\n(50-70%)', ha='center', va='top', fontsize=10, fontweight='bold')
    ax2.text(np.pi/2, -0.1, 'Good\n(70-85%)', ha='center', va='top', fontsize=10, fontweight='bold')
    ax2.text(3*np.pi/4, -0.1, 'Very Good\n(85-95%)', ha='center', va='top', fontsize=10, fontweight='bold')
    ax2.text(np.pi, -0.1, 'Excellent\n(95%+)', ha='right', va='top', fontsize=10, fontweight='bold')
    
    # Add score text
    ax2.text(np.pi/2, 0.6, f'{score:.1f}%', ha='center', va='center', 
             fontsize=24, fontweight='bold', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    plt.suptitle('Boltz1 Single Protein Structure Prediction Results', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Single protein summary saved to: {output_path}")
    return fig

def create_detailed_analysis(confidence_data, output_path):
    """Create detailed analysis for single protein"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Get sequence length from chain data (approximate)
    # Since we only have one chain, we'll create a simple analysis
    
    metrics = [
        ('Overall Confidence', confidence_data['confidence_score'] * 100),
        ('Protein Structure (PTM)', confidence_data['ptm'] * 100),
        ('Complex pLDDT', confidence_data['complex_plddt'] * 100),
        ('Complex PDE', confidence_data['complex_pde'] * 100)
    ]
    
    y_pos = np.arange(len(metrics))
    scores = [metric[1] for metric in metrics]
    labels = [metric[0] for metric in metrics]
    
    bars = ax.barh(y_pos, scores, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], 
                   alpha=0.8, edgecolor='black', linewidth=1)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=14, fontweight='bold')
    ax.set_xlabel('Score (%)', fontsize=16, fontweight='bold')
    ax.set_title('Detailed Single Protein Analysis\nConfidence and Quality Metrics', 
                fontsize=18, fontweight='bold', pad=20)
    ax.set_xlim(0, 100)
    
    # Add score labels
    for i, (bar, score) in enumerate(zip(bars, scores)):
        ax.text(score + 1, bar.get_y() + bar.get_height()/2, 
               f'{score:.1f}%', va='center', ha='left', fontweight='bold', fontsize=12,
               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Add reference lines
    ax.axvline(x=90, color='green', linestyle='--', alpha=0.7, linewidth=2, label='Excellent (>90%)')
    ax.axvline(x=70, color='orange', linestyle='--', alpha=0.7, linewidth=2, label='Good (>70%)')
    ax.axvline(x=50, color='red', linestyle='--', alpha=0.7, linewidth=2, label='Acceptable (>50%)')
    ax.legend(loc='lower right', fontsize=12)
    
    # Style
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_facecolor('#f8f9fa')
    
    # Add interpretation text
    overall_score = confidence_data['confidence_score'] * 100
    if overall_score >= 90:
        interpretation = "Excellent prediction - Near experimental quality"
        color = "green"
    elif overall_score >= 70:
        interpretation = "Good prediction - Reliable for most applications"
        color = "orange"
    elif overall_score >= 50:
        interpretation = "Moderate prediction - Use with caution"
        color = "red"
    else:
        interpretation = "Low confidence prediction - Not recommended"
        color = "darkred"
    
    textstr = f"""
    Prediction Summary:
    • Single protein chain (120 amino acids)
    • Overall confidence: {overall_score:.1f}%
    • Structure quality: {confidence_data['complex_plddt']*100:.1f}%
    • Assessment: {interpretation}
    """
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=12,
           verticalalignment='top', 
           bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Detailed analysis saved to: {output_path}")
    return fig

def main():
    """Main visualization function"""
    print("🎨 Creating Single Protein Demo Visualizations...")
    
    # Paths
    base_path = Path("output/boltz_results_prot/predictions/prot")
    confidence_path = base_path / "confidence_prot_model_0.json"
    
    # Load confidence data
    confidence_data = load_confidence_data(confidence_path)
    
    # Create visualizations
    print("\n📊 Creating protein analysis plots...")
    create_single_protein_summary(confidence_data, "protein_summary.png")
    create_detailed_analysis(confidence_data, "protein_detailed.png")
    
    print(f"\n🎉 Single protein demo visualizations complete!")
    print(f"📁 Files created:")
    print(f"   • protein_summary.png - Summary with gauge visualization")
    print(f"   • protein_detailed.png - Detailed confidence analysis")
    print(f"\n📝 For 3D structure visualization:")
    print(f"   • Use PyMOL: pymol output/boltz_results_prot/predictions/prot/prot_model_0.cif")
    print(f"   • Or upload to ChimeraX/Mol* online viewers")
    print(f"\n🧬 Single protein prediction complete!")

if __name__ == "__main__":
    main()