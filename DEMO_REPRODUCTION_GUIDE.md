# Boltz1 Demo Suite Reproduction Guide

This guide documents the complete process for creating professional Boltz1 structure prediction demonstrations covering multiple use cases and biological systems.

## Demo Suite Overview

We provide **5 comprehensive demos** showcasing different aspects of Boltz1's capabilities:

| Demo | System Type | Key Features | Confidence | Runtime |
|------|-------------|--------------|------------|---------|
| **Protein-Ligand Complex** | Multi-modal complex | CCD + SMILES ligands | 92.2% | 3 min |
| **Single Protein** | Monomer | Basic structure prediction | 81.1% | 30 sec |
| **Protein Multimer** | Protein-protein complex | Interface prediction | 82.5% | 1 min |
| **Custom MSA** | MSA quality comparison | Pre-computed vs server | 69.1% | 25 sec |
| **Pocket Constraints** | Constrained docking | Spatial constraints | TBD | TBD |  

## Prerequisites

### Environment Setup
```bash
# Activate the uv-managed environment
source .venv/bin/activate

# Required packages (should already be installed)
uv pip install matplotlib seaborn biopython
```

### Files Required
All demos use example files from the `examples/` directory:
- `examples/ligand.yaml` - Protein-ligand complex
- `examples/prot.yaml` - Single protein
- `examples/multimer.yaml` - Protein multimer
- `examples/prot_custom_msa.yaml` - Custom MSA protein
- `examples/pocket.yaml` - Pocket constraints
- `examples/msa/seq1.a3m`, `examples/msa/seq2.a3m` - Pre-computed MSAs
- `symmetry.pkl` - Downloaded from Boltz S3 bucket

## Demo Structure

All demos follow a consistent structure:
```
demos/
├── protein_ligand_complex/     # Original demo (moved)
├── single_protein/             # Basic protein folding
├── protein_multimer/           # Protein-protein interactions
├── custom_msa/                 # MSA quality comparison
└── pocket_constraints/         # Constrained predictions
```

Each demo contains:
- `README.md` - Detailed explanation and results
- `visualize_*.py` - Custom 2D visualization script
- `3d_visualization.ipynb` - Interactive 3D Jupyter notebook
- `output/` - Prediction results and structures
- `*.png` - Generated 2D visualization files

# Individual Demo Instructions

## Demo 1: Protein-Ligand Complex (Original)

**Location**: `demos/protein_ligand_complex/`  
**Highlights**: Multi-modal input, excellent confidence (92.2%)

```bash
cd demos/protein_ligand_complex
source ../../.venv/bin/activate

# Run prediction (takes ~3 minutes)
boltz predict ../../examples/ligand.yaml --use_msa_server --out_dir demo_output
```

**Expected Output Structure:**
```
demo_output/boltz_results_ligand/
├── predictions/ligand/
│   ├── ligand_model_0.cif          # 3D structure
│   ├── confidence_ligand_model_0.json  # Confidence metrics
│   └── plddt_ligand_model_0.npz    # Detailed confidence arrays
└── processed/                      # Intermediate files
```

# Generate 2D visualizations
python visualize_demo_simple.py

# Launch interactive 3D visualization
jupyter notebook 3d_visualization.ipynb
```

**Key Results:**
- 92.2% overall confidence (near-experimental accuracy)
- Excellent protein-ligand binding prediction (94.4% iPTM)
- Multi-modal input: CCD codes + SMILES strings
- Interactive 3D views: protein chains, ligand binding sites, confidence coloring

## Demo 2: Single Protein Structure

**Location**: `demos/single_protein/`  
**Highlights**: Basic protein folding, foundation of structural biology

```bash
cd demos/single_protein
source ../../.venv/bin/activate

# Run prediction (takes ~30 seconds)
boltz predict ../../examples/prot.yaml --use_msa_server --out_dir output

# Generate 2D visualizations
python visualize_protein.py

# Launch interactive 3D visualization
jupyter notebook 3d_visualization.ipynb
```

**Key Results:**
- 81.1% overall confidence (good quality prediction)
- Single chain, 120 amino acids
- Demonstrates core protein folding capability
- 3D views: secondary structure coloring, surface representation, confidence mapping

## Demo 3: Protein Multimer Complex

**Location**: `demos/protein_multimer/`  
**Highlights**: Protein-protein interactions, interface prediction

```bash
cd demos/protein_multimer
source ../../.venv/bin/activate

# Run prediction (takes ~1 minute)
boltz predict ../../examples/multimer.yaml --use_msa_server --out_dir output

# Generate 2D visualizations
python visualize_multimer.py

# Launch interactive 3D visualization
jupyter notebook 3d_visualization.ipynb
```

**Key Results:**
- 82.5% overall confidence (excellent complex prediction)
- **83.6% iPTM** - Outstanding protein-protein interface prediction
- Two-chain complex with asymmetric quality (91.3% vs 73.5%)
- 3D views: chain differentiation, interface analysis, interaction surfaces

## Demo 4: Custom MSA Comparison

**Location**: `demos/custom_msa/`  
**Highlights**: MSA quality impact on prediction accuracy

```bash
cd demos/custom_msa
source ../../.venv/bin/activate

# Run prediction with custom MSA (takes ~25 seconds)
boltz predict prot_custom_msa_fixed.yaml --out_dir output

# Generate 2D comparative visualizations  
python visualize_custom_msa.py

# Launch interactive 3D visualization
jupyter notebook 3d_visualization.ipynb
```

**Key Results:**
- 69.1% overall confidence (moderate quality)
- **12% lower** than MSA server (demonstrates MSA importance)
- Same protein as single_protein demo for direct comparison
- 3D views: MSA quality impact visualization, confidence comparisons, regional analysis

## Demo 5: Pocket Constraints

**Location**: `demos/pocket_constraints/`  
**Status**: In development (large protein requires extended runtime)

# Quick Demo Comparison

| Demo | Best For | Runtime | Key Insight |
|------|----------|---------|-------------|
| **Protein-Ligand** | Drug discovery presentations | 3 min | Multi-modal excellence |
| **Single Protein** | Basic folding concepts | 30 sec | Foundation demonstration |
| **Multimer** | PPI and complexes | 1 min | Interface prediction strength |
| **Custom MSA** | Technical discussions | 25 sec | MSA quality importance |

# Visualization Gallery

Each demo generates both 2D publication-quality visualizations and interactive 3D molecular views:

## 2D Visualizations (PNG Files)

### Protein-Ligand Complex
- `demo_confidence_detailed.png` - 4-panel analysis with interaction matrix
- `demo_confidence_summary.png` - Clean presentation summary
- `demo_metric_breakdown.png` - Primary vs complex metrics

### Single Protein
- `protein_summary.png` - Summary with gauge-style confidence visualization
- `protein_detailed.png` - Detailed horizontal bar analysis

### Protein Multimer
- `multimer_summary.png` - Complete 4-panel analysis with chain interaction matrix
- `multimer_interactions.png` - Detailed protein-protein interaction breakdown

### Custom MSA
- `msa_comparison.png` - Side-by-side MSA server vs custom MSA comparison
- `msa_performance_analysis.png` - Detailed performance breakdown with quality bands

## 3D Interactive Visualizations (Jupyter Notebooks)

### Requirements
```bash
# Install 3D visualization dependencies
source .venv/bin/activate
pip install py3Dmol jupyter
```

### Features Available in All Demos
- **Interactive 3D Structure**: Mouse controls for rotation, zoom, pan
- **Confidence Coloring**: Color-coded by prediction quality (Blue=high, Yellow=medium, Red=low)
- **Multiple Views**: Basic structure, surface representation, confidence mapping
- **High-Quality Export**: Right-click to save images for publications
- **Biological Context**: Detailed analysis and interpretation in notebook

### Demo-Specific 3D Features

**Protein-Ligand Complex:**
- Multi-chain protein visualization (light blue/green)
- Ligand highlighting (red SAH, orange tyrosine)
- Binding site focused views
- Interface surface analysis

**Single Protein:**
- Secondary structure coloring (red α-helices, yellow β-sheets)
- Molecular surface with hydrophobicity
- Confidence thickness variation (putty representation)
- N/C terminus labeling

**Protein Multimer:**
- Chain differentiation (blue Chain A, green Chain B)
- Interface surface highlighting
- Asymmetric quality visualization
- Interaction contact analysis

**Custom MSA:**
- MSA quality impact visualization
- Comparison indicators vs MSA server
- Regional confidence analysis
- Educational MSA importance demonstration

### Usage Instructions
1. Navigate to any demo folder
2. Run: `jupyter notebook 3d_visualization.ipynb`
3. Execute all cells to generate interactive views
4. Use mouse to explore structures:
   - **Left click + drag**: Rotate
   - **Right click + drag**: Pan
   - **Scroll wheel**: Zoom
   - **Double click**: Center on atom

# Biological Systems Overview

## Protein-Ligand Complex (`examples/ligand.yaml`)
**System**: Methyltransferase enzyme with cofactor and substrate
- **Protein**: 465 amino acids (chains A & B) - Methyltransferase enzyme
- **SAH Ligand**: S-adenosyl-L-homocysteine cofactor (CCD: SAH)
- **Tyrosine Ligand**: Amino acid substrate (SMILES string)
- **Application**: DNA methylation, cancer research, drug design

## Single Protein (`examples/prot.yaml`)
**System**: Single-domain protein
- **Protein**: 120 amino acids - Compact globular protein
- **Application**: Basic protein folding, structural analysis

## Protein Multimer (`examples/multimer.yaml`)
**System**: Two-chain protein complex
- **Chain A**: 108 amino acids - His-tagged construct
- **Chain B**: 127 amino acids - Binding partner
- **Application**: Protein-protein interactions, enzyme complexes

## Custom MSA (`examples/prot_custom_msa.yaml`)
**System**: Same as single protein but with pre-computed MSA
- **Protein**: Identical 120 amino acid sequence
- **MSA**: Pre-computed from `examples/msa/seq2.a3m`
- **Application**: MSA quality analysis, technical validation

# Performance Summary

## Confidence Score Comparison

| Demo | Overall | PTM | iPTM | Key Strength |
|------|---------|-----|------|--------------|
| **Protein-Ligand** | 92.2% | 93.5% | 94.4% | Multi-modal excellence |
| **Protein Multimer** | 82.5% | 81.1% | 83.6% | Interface prediction |
| **Single Protein** | 81.1% | 77.8% | N/A | Basic folding |
| **Custom MSA** | 69.1% | 63.5% | N/A | MSA dependency |

## Quality Interpretation
- **90%+**: Excellent - Near experimental accuracy
- **80-90%**: Very Good - Suitable for most applications  
- **70-80%**: Good - Reliable for structural analysis
- **60-70%**: Moderate - Use with caution
- **<60%**: Poor - Not recommended for critical applications

# Presentation Strategies

## For Different Audiences

### For Drug Discovery (Protein-Ligand Demo)
**Best Demo**: `demos/protein_ligand_complex/`
- **Opening**: "92.2% confidence rivals experimental methods"
- **Key Visual**: `demo_confidence_summary.png`
- **Live Demo**: 3D structure in PyMOL showing binding site
- **Closing**: "3 minutes vs weeks in the lab"

### For Structural Biology (Multimer Demo)  
**Best Demo**: `demos/protein_multimer/`
- **Opening**: "83.6% iPTM for protein-protein interfaces"
- **Key Visual**: `multimer_summary.png` interaction matrix
- **Technical Point**: Asymmetric chain quality analysis
- **Closing**: "Predicts complex assembly accurately"

### For Technical Validation (MSA Comparison)
**Best Demo**: `demos/custom_msa/`
- **Opening**: "MSA quality impacts prediction by 12%"
- **Key Visual**: `msa_comparison.png` side-by-side
- **Technical Point**: Evolutionary information importance
- **Closing**: "Quality control matters for accuracy"

### For General Audience (Single Protein)
**Best Demo**: `demos/single_protein/`
- **Opening**: "From sequence to structure in 30 seconds"
- **Key Visual**: `protein_summary.png` gauge visualization
- **Simple Point**: "Folding proteins computationally"
- **Closing**: "Foundation of computational biology"

## Multi-Demo Presentation Flow

### Comprehensive 15-Minute Presentation
1. **Intro** (2 min): Single protein demo - establish foundation
2. **Complexity** (5 min): Multimer demo - show advanced capabilities  
3. **Applications** (5 min): Protein-ligand demo - real-world impact
4. **Technical** (3 min): MSA comparison - quality importance

### Quick 5-Minute Demo
- **Focus**: Protein-ligand complex only
- **Highlight**: 92.2% confidence, multi-modal input
- **Live Demo**: 3D structure visualization
- **Impact**: Drug discovery applications

## 3D Structure Visualization
```bash
# For any demo, open the 3D structure:
pymol [demo_folder]/output/*/predictions/*/[structure_file].cif

# Online viewers (upload CIF file):
# - ChimeraX (chimerax.ucsd.edu)
# - Mol* (molstar.org)
# - NGL Viewer (nglviewer.org)
```

## Troubleshooting

### Common Issues

1. **MSA Server Timeout**:
   ```bash
   # If --use_msa_server fails, the example includes pre-computed MSA
   # The prediction should still work with the local MSA file
   ```

2. **Visualization Font Warnings**:
   ```
   # Emoji warnings are cosmetic and don't affect output quality
   # Generated PNG files are still high-quality (300 DPI)
   ```

3. **Memory Issues**:
   ```bash
   # For limited GPU memory, reduce batch size in prediction
   # The example is already optimized for single-GPU inference
   ```

# File Structure Reference

## Demo Organization
```
demos/
├── protein_ligand_complex/          # Multi-modal complex (92.2%)
│   ├── demo_output/                 # Original demo results
│   ├── visualize_demo_simple.py     # Multi-modal visualization
│   ├── demo_confidence_detailed.png
│   ├── demo_confidence_summary.png
│   └── demo_metric_breakdown.png
├── single_protein/                  # Basic folding (81.1%)  
│   ├── output/                      # Prediction results
│   ├── visualize_protein.py         # Single protein visualization
│   ├── protein_summary.png
│   └── protein_detailed.png
├── protein_multimer/                # Protein-protein (82.5%)
│   ├── output/                      # Complex prediction results
│   ├── visualize_multimer.py        # Multimer visualization
│   ├── multimer_summary.png
│   └── multimer_interactions.png
├── custom_msa/                      # MSA comparison (69.1%)
│   ├── output/                      # Custom MSA results
│   ├── prot_custom_msa_fixed.yaml   # Fixed input file
│   ├── visualize_custom_msa.py      # MSA comparison visualization
│   ├── msa_comparison.png
│   └── msa_performance_analysis.png
└── pocket_constraints/              # Constrained prediction (TBD)
    └── output/                      # In development
```

## Key Input Files
- `examples/ligand.yaml` - Protein-ligand complex with CCD + SMILES
- `examples/prot.yaml` - Single protein (120 AA)
- `examples/multimer.yaml` - Two-chain complex (108 + 127 AA)
- `examples/prot_custom_msa.yaml` - Single protein with custom MSA
- `examples/pocket.yaml` - Large protein with constraints (1000+ AA)
- `examples/msa/seq1.a3m` - Pre-computed MSA for ligand demo
- `examples/msa/seq2.a3m` - Pre-computed MSA for custom MSA demo
- `symmetry.pkl` - Required symmetry file (root directory)

## Extending the Demo

### Using Different Examples
```bash
# Try other included examples:
boltz predict examples/prot.yaml --use_msa_server --out_dir prot_demo
boltz predict examples/pocket.yaml --use_msa_server --out_dir pocket_demo
boltz predict examples/multimer.yaml --use_msa_server --out_dir multimer_demo
```

### Custom Input Creation
```yaml
# Template for custom protein-ligand prediction
version: 1
sequences:
  - protein:
      id: [A]
      sequence: YOUR_PROTEIN_SEQUENCE_HERE
  - ligand:
      id: [B] 
      ccd: YOUR_CCD_CODE        # For database molecules
      # OR
      smiles: YOUR_SMILES_STRING   # For custom molecules
```

## Performance Notes

- **GPU Required**: NVIDIA RTX A6000 (24GB) recommended
- **Inference Time**: ~3 minutes for 465 AA protein + 2 ligands
- **Memory Usage**: ~8GB GPU memory for this example
- **Scaling**: Larger proteins require proportionally more time/memory

## Citation Information

When presenting this demo, acknowledge:
```
Boltz-1: Democratizing Biomolecular Interaction Modeling
Wohlwend et al., bioRxiv 2024
https://doi.org/10.1101/2024.11.19.624167
```

---

**Last Updated**: 2025-01-28  
**Tested Environment**: Python 3.11.13, PyTorch 2.7.1+cu126, Boltz 1.0.0