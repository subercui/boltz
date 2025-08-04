#!/usr/bin/env python3
"""
Protein Multimer Demo Visualization Script
Creates presentation-ready visualizations for protein multimer complex prediction
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

def create_multimer_summary(confidence_data, output_path):
    """Create a summary visualization for multimer prediction"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Boltz1 Protein Multimer Complex Prediction', fontsize=20, fontweight='bold')
    
    # 1. Overall confidence scores
    overall_scores = {
        'Overall\nConfidence': confidence_data['confidence_score'],
        'Protein Structure\n(PTM)': confidence_data['ptm'],
        'Inter-Protein\nInteraction (iPTM)': confidence_data['iptm'],
        'Complex\nQuality (pLDDT)': confidence_data['complex_plddt']
    }
    
    bars = ax1.bar(overall_scores.keys(), [v*100 for v in overall_scores.values()],
                   color=['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd'], alpha=0.8)
    ax1.set_ylabel('Confidence Score (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Overall Complex Quality', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, score in zip(bars, overall_scores.values()):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score*100:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # 2. Per-chain confidence
    chain_scores = [v*100 for v in confidence_data['chains_ptm'].values()]
    chain_labels = [f'Chain {chr(65+i)}' for i in range(len(chain_scores))]
    
    bars2 = ax2.bar(chain_labels, chain_scores, 
                   color=['#e377c2', '#7f7f7f'], alpha=0.7, edgecolor='navy')
    ax2.set_ylabel('PTM Score (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Individual Chain Quality', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, score in zip(bars2, chain_scores):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # 3. Complex interaction metrics
    interaction_metrics = {
        'Protein-Protein\nInteraction': confidence_data['protein_iptm'],
        'Complex Interface\nAccuracy (ipLDDT)': confidence_data['complex_iplddt'],
        'Interface Distance\nError (iPDE)': min(confidence_data['complex_ipde']/10, 1.0),  # Scale down for visualization
    }
    
    bars3 = ax3.bar(interaction_metrics.keys(), [v*100 for v in interaction_metrics.values()],
                   color=['#2ca02c', '#d62728', '#ff7f0e'], alpha=0.8)
    ax3.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
    ax3.set_title('Interface Quality Metrics', fontsize=14, fontweight='bold')
    ax3.set_ylim(0, 100)
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3)
    
    # Add value labels (special handling for iPDE)
    for i, (bar, score) in enumerate(zip(bars3, interaction_metrics.values())):
        height = bar.get_height()
        if i == 2:  # iPDE - show original value
            ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{confidence_data["complex_ipde"]:.1f}Å', ha='center', va='bottom', fontweight='bold', fontsize=11)
        else:
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
    ax4.set_title('Chain-Chain Interaction Matrix', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Chain Index', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Chain Index', fontsize=12, fontweight='bold')
    
    # Set proper labels
    ax4.set_xticks(range(n_chains))
    ax4.set_yticks(range(n_chains))
    ax4.set_xticklabels([f'Chain {chr(65+i)}' for i in range(n_chains)])
    ax4.set_yticklabels([f'Chain {chr(65+i)}' for i in range(n_chains)])
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax4)
    cbar.set_label('Interaction Confidence', fontsize=12, fontweight='bold')
    
    # Add text annotations to heatmap
    for i in range(n_chains):
        for j in range(n_chains):
            color = "white" if matrix[i, j] < 0.5 else "black"
            ax4.text(j, i, f'{matrix[i, j]:.2f}',
                    ha="center", va="center", color=color, 
                    fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Multimer summary saved to: {output_path}")
    return fig

def create_interaction_analysis(confidence_data, output_path):
    """Create detailed interaction analysis"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Left panel: Interaction vs Individual quality
    chain_ptm = list(confidence_data['chains_ptm'].values())
    interaction_score = confidence_data['iptm']
    
    metrics = [
        ('Chain A Quality', chain_ptm[0] * 100),
        ('Chain B Quality', chain_ptm[1] * 100),
        ('A-B Interaction', interaction_score * 100),
        ('Overall Complex', confidence_data['confidence_score'] * 100)
    ]
    
    y_pos = np.arange(len(metrics))
    scores = [metric[1] for metric in metrics]
    labels = [metric[0] for metric in metrics]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    bars = ax1.barh(y_pos, scores, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(labels, fontsize=14, fontweight='bold')
    ax1.set_xlabel('Confidence Score (%)', fontsize=16, fontweight='bold')
    ax1.set_title('Multimer Quality Breakdown', fontsize=16, fontweight='bold')
    ax1.set_xlim(0, 100)
    
    # Add score labels
    for i, (bar, score) in enumerate(zip(bars, scores)):
        ax1.text(score + 1, bar.get_y() + bar.get_height()/2, 
               f'{score:.1f}%', va='center', ha='left', fontweight='bold', fontsize=12,
               bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Add reference lines
    ax1.axvline(x=90, color='green', linestyle='--', alpha=0.7, linewidth=2)
    ax1.axvline(x=70, color='orange', linestyle='--', alpha=0.7, linewidth=2)
    ax1.grid(True, alpha=0.3, axis='x')
    ax1.set_facecolor('#f8f9fa')
    
    # Right panel: Interface quality assessment
    interface_metrics = {
        'Interface Confidence\n(iPTM)': confidence_data['iptm'],
        'Interface Accuracy\n(ipLDDT)': confidence_data['complex_iplddt'],
        'Interface Positioning\n(Protein iPTM)': confidence_data['protein_iptm']
    }
    
    bars2 = ax2.bar(interface_metrics.keys(), [v*100 for v in interface_metrics.values()],
                   color=['#2ca02c', '#d62728', '#9467bd'], alpha=0.8, edgecolor='black', linewidth=1)
    
    ax2.set_ylabel('Score (%)', fontsize=14, fontweight='bold')
    ax2.set_title('Interface Quality Assessment', fontsize=16, fontweight='bold')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels
    for bar, score in zip(bars2, interface_metrics.values()):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{score*100:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    plt.suptitle('Boltz1 Protein-Protein Interaction Analysis', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Interaction analysis saved to: {output_path}")
    return fig

def main():
    """Main visualization function"""
    print("🎨 Creating Protein Multimer Demo Visualizations...")
    
    # Paths
    base_path = Path("output/boltz_results_multimer/predictions/multimer")
    confidence_path = base_path / "confidence_multimer_model_0.json"
    
    # Load confidence data
    confidence_data = load_confidence_data(confidence_path)
    
    # Create visualizations
    print("\n📊 Creating multimer analysis plots...")
    create_multimer_summary(confidence_data, "multimer_summary.png")
    create_interaction_analysis(confidence_data, "multimer_interactions.png")
    
    print(f"\n🎉 Multimer demo visualizations complete!")
    print(f"📁 Files created:")
    print(f"   • multimer_summary.png - Complete 4-panel analysis")
    print(f"   • multimer_interactions.png - Detailed interaction analysis")
    print(f"\n📝 For 3D structure visualization:")
    print(f"   • Use PyMOL: pymol output/boltz_results_multimer/predictions/multimer/multimer_model_0.cif")
    print(f"   • Or upload to ChimeraX/Mol* online viewers")
    print(f"\n🔗 Excellent protein-protein interaction prediction!")

if __name__ == "__main__":
    main()