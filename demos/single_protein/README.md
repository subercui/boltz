# Single Protein Structure Prediction Demo

## Overview

This demo showcases Boltz1's ability to predict the 3D structure of a single protein chain using only its amino acid sequence. This is the fundamental application of protein structure prediction.

## Input System (`examples/prot.yaml`)

**Protein**: Single chain, 120 amino acids
- **Sequence**: `QLEDSEVEAVAKGLEEMYANGVTEDNFKNYVKNNFAQQEISSVEEELNVNISDSCVANKIKDEFFAMISISAIVKAAQKKAWKELAVTVLRFAKANGLKTNAIIVAGQLALWAVQCG`
- **Chain ID**: A
- **MSA**: Generated automatically using MSA server

## Key Results

### Confidence Scores
- **Overall Confidence**: 81.1% - Good quality prediction
- **Protein Structure (PTM)**: 77.8% - Reliable structural accuracy
- **Complex pLDDT**: 81.9% - Good local confidence
- **Complex PDE**: 77.8% - Acceptable distance error prediction

### Interpretation
- This represents a **good quality** single protein prediction
- Confidence scores in the 70-85% range indicate the structure is reliable for most research applications
- No inter-chain interactions (iPTM = 0) as expected for single protein
- Suitable for structural analysis, functional studies, and drug design

## Files Generated

### Prediction Output
- `output/boltz_results_prot/predictions/prot/prot_model_0.cif` - 3D structure in CIF format
- `output/boltz_results_prot/predictions/prot/confidence_prot_model_0.json` - Confidence metrics
- `output/boltz_results_prot/predictions/prot/plddt_prot_model_0.npz` - Per-residue confidence scores

### Visualizations
- `protein_summary.png` - Summary with gauge-style confidence visualization
- `protein_detailed.png` - Detailed horizontal bar chart analysis

## Running This Demo

```bash
# From the boltz root directory
source .venv/bin/activate
cd demos/single_protein

# Run prediction (takes ~30 seconds)
boltz predict ../../examples/prot.yaml --use_msa_server --out_dir output

# Generate visualizations
python visualize_protein.py

# View 3D structure
pymol output/boltz_results_prot/predictions/prot/prot_model_0.cif
```

## Biological Context

Single protein structure prediction is the foundation of computational structural biology. This demo shows:

1. **Ab Initio Prediction**: Starting only from sequence, Boltz1 predicts the complete 3D fold
2. **MSA Integration**: Automatically incorporates evolutionary information for better accuracy
3. **Confidence Assessment**: Provides detailed quality metrics for result validation
4. **Research Applications**: Suitable for protein engineering, drug discovery, and functional analysis

## Performance Notes

- **Runtime**: ~30 seconds on RTX A6000
- **Memory**: ~2GB GPU memory
- **Accuracy**: 81% confidence represents good prediction quality
- **Validation**: Confidence scores align with typical single-domain protein predictions

## Next Steps

For more complex scenarios, see:
- `../protein_multimer/` - Multi-chain protein complexes
- `../pocket_constraints/` - Protein-ligand interactions with constraints
- `../custom_msa/` - Using pre-computed multiple sequence alignments

## Citation

When using this demo, cite:
```
Boltz-1: Democratizing Biomolecular Interaction Modeling
Wohlwend et al., bioRxiv 2024
```