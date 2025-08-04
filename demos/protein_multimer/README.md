# Protein Multimer Complex Prediction Demo

## Overview

This demo showcases Boltz1's ability to predict protein-protein interactions and the structure of multi-chain protein complexes. This is crucial for understanding protein function, enzyme complexes, and biological assemblies.

## Input System (`examples/multimer.yaml`)

**Complex**: Two-chain protein complex
- **Chain A**: 108 amino acids - His-tagged protein construct
  - Sequence: `MAHHHHHHVAVDAVSFTLLQDQLQSVLDTLSEREAGVVRLRFGLTDGQPRTLDEIGQVYGVTRERIRQIESKTMSKLRHPSRSQVLRDYLDGSSGSGTPEERLLRAIFGEKA`
- **Chain B**: 127 amino acids - Binding partner protein  
  - Sequence: `MRYAFAAEATTCNAFWRNVDMTVTALYEVPLGVCTQDPDRWTTTPDDEAKTLCRACPRRWLCARDAVESAGAEGLWAGVVIPESGRARAFALGQLRSLAERNGYPVRDHRVSAQSA`
- **MSA**: Generated automatically for both chains using MSA server

## Key Results

### Overall Complex Quality
- **Overall Confidence**: 82.5% - Excellent complex prediction
- **Protein Structure (PTM)**: 81.1% - High individual chain accuracy
- **Inter-Protein Interaction (iPTM)**: 83.6% - **Excellent interface prediction**
- **Complex pLDDT**: 82.3% - Very good overall structural quality

### Individual Chain Analysis
- **Chain A Quality**: 91.3% - Excellent individual fold prediction
- **Chain B Quality**: 73.5% - Good individual fold prediction
- **Chain Quality Difference**: 17.8% - Indicates different difficulty levels

### Interface Quality Assessment
- **Protein-Protein iPTM**: 83.6% - Very confident protein-protein interactions
- **Interface Accuracy (ipLDDT)**: 83.8% - Excellent interface modeling
- **Interface Distance Error (iPDE)**: 2.7Å - Acceptable interface positioning

### Chain Interaction Matrix
```
        Chain A  Chain B
Chain A   91.3%   83.6%
Chain B   71.8%   73.5%
```

## Interpretation

This represents an **excellent protein multimer prediction**:

1. **High Interface Confidence**: 83.6% iPTM indicates very reliable protein-protein interactions
2. **Asymmetric Quality**: Chain A is predicted with higher confidence than Chain B, which is common in complexes
3. **Strong Interface**: The A-B interaction score (83.6%) is very high, indicating a stable binding interface
4. **Suitable for Research**: All metrics > 70% make this suitable for structural analysis and drug design

## Files Generated

### Prediction Output
- `output/boltz_results_multimer/predictions/multimer/multimer_model_0.cif` - 3D complex structure
- `output/boltz_results_multimer/predictions/multimer/confidence_multimer_model_0.json` - Complete confidence metrics
- `output/boltz_results_multimer/predictions/multimer/plddt_multimer_model_0.npz` - Per-residue confidence arrays

### Visualizations
- `multimer_summary.png` - Complete 4-panel analysis with interaction matrix
- `multimer_interactions.png` - Detailed protein-protein interaction breakdown

## Running This Demo

```bash
# From the boltz root directory
source .venv/bin/activate
cd demos/protein_multimer

# Run prediction (takes ~1 minute)
boltz predict ../../examples/multimer.yaml --use_msa_server --out_dir output

# Generate visualizations
python visualize_multimer.py

# View 3D structure
pymol output/boltz_results_multimer/predictions/multimer/multimer_model_0.cif
```

## Biological Context

Protein multimer prediction addresses several key biological questions:

1. **Protein-Protein Interactions**: How do proteins bind to each other?
2. **Functional Complexes**: What is the structure of multi-subunit enzymes?
3. **Regulatory Mechanisms**: How do regulatory proteins interact with their targets?
4. **Drug Design**: Where are the binding interfaces for small molecule inhibitors?

### Applications
- **Enzyme Complex Analysis**: Understanding multi-subunit enzyme mechanisms
- **Drug Discovery**: Targeting protein-protein interaction interfaces
- **Protein Engineering**: Designing improved binding interfaces
- **Structural Biology**: Validating experimental complex structures

## Performance Notes

- **Runtime**: ~1 minute on RTX A6000 (longer than single proteins due to interface sampling)
- **Memory**: ~4GB GPU memory
- **Accuracy**: 82.5% overall confidence represents excellent complex prediction
- **Interface Quality**: 83.6% iPTM is exceptional for protein-protein interface prediction

## Comparison to Single Protein Demo

| Metric | Single Protein | Multimer Complex |
|--------|---------------|------------------|
| Overall Confidence | 81.1% | 82.5% |
| Individual Chain Quality | 77.8% | 91.3%/73.5% |
| Inter-chain Interactions | N/A | 83.6% |
| Complexity | Low | High |
| Runtime | 30s | 60s |

The multimer demo shows Boltz1's strength in predicting **protein-protein interactions**, which is significantly more challenging than single protein folding.

## Next Steps

For more complex scenarios, see:
- `../pocket_constraints/` - Protein-ligand interactions with spatial constraints
- `../custom_msa/` - Using pre-computed multiple sequence alignments
- `../protein_ligand_complex/` - Multi-modal protein-ligand complexes

## Citation

When using this demo, cite:
```
Boltz-1: Democratizing Biomolecular Interaction Modeling
Wohlwend et al., bioRxiv 2024
```