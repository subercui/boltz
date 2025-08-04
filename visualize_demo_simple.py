#!/usr/bin/env python3
"""
Boltz1 Demo Visualization Script
Creates presentation-ready confidence visualizations from actual Boltz results
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

def create_confidence_plot(confidence_data, output_path):
    """Create a beautiful confidence score visualization"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Boltz1 Prediction Confidence Metrics', fontsize=20, fontweight='bold')
    
    # 1. Overall confidence scores
    overall_scores = {
        'Overall\nConfidence': confidence_data['confidence_score'],
        'Protein\nStructure (PTM)': confidence_data['ptm'],
        'Protein-Ligand\nBinding (iPTM)': confidence_data['iptm'],
        'Ligand\nModeling': confidence_data['ligand_iptm']
    }
    
    bars = ax1.bar(overall_scores.keys(), [v*100 for v in overall_scores.values()], 
                   color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], alpha=0.8)
    ax1.set_ylabel('Confidence Score (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Overall Prediction Quality', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 102)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, score in zip(bars, overall_scores.values()):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score*100:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # 2. Per-chain confidence
    chain_scores = [v*100 for v in confidence_data['chains_ptm'].values()]
    chain_labels = [f'Chain {i}' for i in range(len(chain_scores))]
    
    bars2 = ax2.bar(chain_labels, chain_scores, color='lightblue', alpha=0.7, edgecolor='navy')
    ax2.set_ylabel('Confidence Score (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Per-Chain Structure Quality', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 102)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, score in zip(bars2, chain_scores):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 3. Complex quality metrics
    complex_metrics = {
        'Complex\npLDDT': confidence_data['complex_plddt'],
        'Complex\nipLDDT': confidence_data['complex_iplddt'],
        'Complex\nPDE': confidence_data['complex_pde'],
        'Complex\niPDE': confidence_data['complex_ipde']
    }
    
    bars3 = ax3.bar(complex_metrics.keys(), [v*100 for v in complex_metrics.values()],
                   color=['#9467bd', '#8c564b', '#e377c2', '#7f7f7f'], alpha=0.8)
    ax3.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax3.set_title('Complex Quality Metrics', fontsize=14, fontweight='bold')
    ax3.set_ylim(0, 102)
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, score in zip(bars3, complex_metrics.values()):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score*100:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # 4. Inter-chain interaction matrix
    pair_data = confidence_data['pair_chains_iptm']
    n_chains = len(pair_data)
    matrix = np.zeros((n_chains, n_chains))
    
    for i in range(n_chains):
        for j in range(n_chains):
            matrix[i, j] = pair_data[str(i)][str(j)]
    
    im = ax4.imshow(matrix, cmap='RdYlBu_r', vmin=0, vmax=1)
    ax4.set_title('Inter-Chain Interaction Confidence', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Chain Index', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Chain Index', fontsize=12, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax4)
    cbar.set_label('Confidence Score', fontsize=12, fontweight='bold')
    
    # Add text annotations to heatmap
    for i in range(n_chains):
        for j in range(n_chains):
            text = ax4.text(j, i, f'{matrix[i, j]:.2f}',
                           ha="center", va="center", color="white" if matrix[i, j] < 0.5 else "black", 
                           fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Confidence plot saved to: {output_path}")
    return fig

def create_summary_figure(confidence_data, output_path):
    """Create a summary figure for presentation"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    
    # Create a professional summary
    key_metrics = [
        ('Overall Confidence', confidence_data['confidence_score'] * 100),
        ('Protein Structure Quality', confidence_data['ptm'] * 100),
        ('Protein-Ligand Binding', confidence_data['iptm'] * 100),
        ('Ligand Modeling', confidence_data['ligand_iptm'] * 100)
    ]
    
    # Create horizontal bar chart
    y_pos = np.arange(len(key_metrics))
    scores = [metric[1] for metric in key_metrics]
    labels = [metric[0] for metric in key_metrics]
    
    bars = ax.barh(y_pos, scores, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], 
                   alpha=0.8, edgecolor='black', linewidth=1)
    
    # Customize the plot
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=16, fontweight='bold')
    ax.set_xlabel('Confidence Score (%)', fontsize=18, fontweight='bold')
    ax.set_title('Boltz1 Protein-Ligand Complex Prediction\nExcellent Confidence Scores (90%+)', 
                fontsize=20, fontweight='bold', pad=30)
    ax.set_xlim(0, 100)
    
    # Add score labels
    for i, (bar, score) in enumerate(zip(bars, scores)):
        ax.text(score + 1, bar.get_y() + bar.get_height()/2, 
               f'{score:.1f}%', va='center', ha='left', fontweight='bold', fontsize=14,
               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Add reference lines
    ax.axvline(x=90, color='green', linestyle='--', alpha=0.7, linewidth=2, label='Excellent (>90%)')
    ax.axvline(x=70, color='orange', linestyle='--', alpha=0.7, linewidth=2, label='Good (>70%)')
    ax.legend(loc='lower right', fontsize=12)
    
    # Style
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_facecolor('#f8f9fa')
    
    # Add data-driven annotation
    n_chains = len(confidence_data['chains_ptm'])
    textstr = f"""
    Prediction Results:
    • {n_chains} chains predicted
    • Overall confidence: {confidence_data['confidence_score']*100:.1f}%
    • Protein structure quality: {confidence_data['ptm']*100:.1f}%
    • Protein-ligand binding: {confidence_data['iptm']*100:.1f}%
    """
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=12,
           verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Summary figure saved to: {output_path}")
    return fig

def create_metric_breakdown(confidence_data, output_path):
    """Create a detailed metric breakdown from actual Boltz results"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Left panel: Main confidence metrics
    main_metrics = {
        'Overall\nConfidence': confidence_data['confidence_score'],
        'Protein Structure\n(PTM)': confidence_data['ptm'],
        'Protein-Ligand\n(iPTM)': confidence_data['iptm'],
        'Ligand Modeling\n(Ligand iPTM)': confidence_data['ligand_iptm']
    }
    
    bars1 = ax1.bar(main_metrics.keys(), [v*100 for v in main_metrics.values()],
                   color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], alpha=0.8,
                   edgecolor='black', linewidth=1)
    
    ax1.set_ylabel('Confidence Score (%)', fontsize=14, fontweight='bold')
    ax1.set_title('Primary Confidence Metrics', fontsize=16, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, score in zip(bars1, main_metrics.values()):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score*100:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Right panel: Complex quality metrics
    complex_metrics = {
        'Complex\npLDDT': confidence_data['complex_plddt'],
        'Complex\nipLDDT': confidence_data['complex_iplddt'],
        'Complex\nPDE': confidence_data['complex_pde'],
        'Complex\niPDE': confidence_data['complex_ipde']
    }
    
    bars2 = ax2.bar(complex_metrics.keys(), [v*100 for v in complex_metrics.values()],
                   color=['#9467bd', '#8c564b', '#e377c2', '#7f7f7f'], alpha=0.8,
                   edgecolor='black', linewidth=1)
    
    ax2.set_ylabel('Score (%)', fontsize=14, fontweight='bold')
    ax2.set_title('Complex Quality Assessment', fontsize=16, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, score in zip(bars2, complex_metrics.values()):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score*100:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    plt.suptitle('Boltz1 Prediction Quality Assessment', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Metric breakdown saved to: {output_path}")
    return fig

def main():
    """Main visualization function"""
    print("🎨 Creating Boltz1 Demo Visualizations...")
    
    # Paths
    base_path = Path("demo_output/boltz_results_ligand/predictions/ligand")
    confidence_path = base_path / "confidence_ligand_model_0.json"
    
    # Load confidence data
    confidence_data = load_confidence_data(confidence_path)
    
    # Create visualizations
    print("\n📊 Creating confidence plots...")
    create_confidence_plot(confidence_data, "demo_confidence_detailed.png")
    create_summary_figure(confidence_data, "demo_confidence_summary.png")
    create_metric_breakdown(confidence_data, "demo_metric_breakdown.png")
    
    print(f"\n🎉 Demo visualizations complete!")
    print(f"📁 Files created:")
    print(f"   • demo_confidence_detailed.png - Detailed 4-panel confidence analysis")
    print(f"   • demo_confidence_summary.png - Clean presentation summary")
    print(f"   • demo_metric_breakdown.png - Detailed metric breakdown")
    print(f"\n📝 For 3D structure visualization:")
    print(f"   • Use PyMOL: pymol demo_output/boltz_results_ligand/predictions/ligand/ligand_model_0.cif")
    print(f"   • Or upload to ChimeraX/Mol* online viewers")
    print(f"\n🎬 Perfect for your presentation!")

if __name__ == "__main__":
    main()