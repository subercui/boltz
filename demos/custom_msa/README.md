# Custom MSA Protein Prediction Demo

## Overview

This demo illustrates the impact of Multiple Sequence Alignment (MSA) quality on protein structure prediction accuracy. It compares the same protein predicted with a pre-computed MSA versus automatic MSA generation using the MSA server.

## Input System (`prot_custom_msa_fixed.yaml`)

**Protein**: Single chain, 120 amino acids (identical to single_protein demo)
- **Sequence**: `QLEDSEVEAVAKGLEEMYANGVTEDNFKNYVKNNFAQQEISSVEEELNVNISDSCVANKIKDEFFAMISISAIVKAAQKKAWKELAVTVLRFAKANGLKTNAIIVAGQLALWAVQCG`
- **Chain ID**: A
- **MSA**: Pre-computed from `examples/msa/seq2.a3m` (16.8KB file)

## Key Results: MSA Quality Impact

### Performance Comparison

| Metric | MSA Server | Pre-computed MSA | Difference |
|--------|------------|------------------|------------|
| Overall Confidence | 81.1% | **69.1%** | -12.0% |
| Protein Structure (PTM) | 77.8% | **63.5%** | -14.3% |
| Structure Quality (pLDDT) | 81.9% | **70.5%** | -11.4% |
| Distance Error (PDE) | 77.8% | **97.1%** | +19.3% (worse) |

### Custom MSA Results
- **Overall Confidence**: 69.1% - Moderate quality prediction
- **Protein Structure (PTM)**: 63.5% - Acceptable but reduced accuracy
- **Structure Quality (pLDDT)**: 70.5% - Good local confidence
- **Distance Error (PDE)**: 97.1% - Higher error rates

### Key Findings

1. **MSA Quality Matters**: The MSA server achieved **12% higher overall confidence**
2. **Evolutionary Information**: Better MSA provides richer evolutionary context
3. **Structural Accuracy**: PTM scores dropped by 14.3% with limited MSA
4. **Distance Errors**: PDE increased significantly, indicating less accurate geometry

## Quality Assessment

**Pre-computed MSA Performance**: 69.1% overall confidence places this in the **"Moderate"** quality range:
- ✅ Suitable for general structural analysis
- ⚠️ Use with caution for detailed applications
- ❌ Not recommended for high-precision drug design

## Files Generated

### Prediction Output
- `output/boltz_results_prot_custom_msa_fixed/predictions/prot_custom_msa_fixed/prot_custom_msa_fixed_model_0.cif` - 3D structure
- `output/boltz_results_prot_custom_msa_fixed/predictions/prot_custom_msa_fixed/confidence_prot_custom_msa_fixed_model_0.json` - Confidence metrics

### Visualizations
- `msa_comparison.png` - Side-by-side comparison of MSA server vs custom MSA
- `msa_performance_analysis.png` - Detailed performance breakdown with quality bands

## Running This Demo

```bash
# From the boltz root directory
source .venv/bin/activate
cd demos/custom_msa

# Run prediction with custom MSA (takes ~25 seconds)
boltz predict prot_custom_msa_fixed.yaml --out_dir output

# Generate visualizations
python visualize_custom_msa.py

# View 3D structure
pymol output/boltz_results_prot_custom_msa_fixed/predictions/prot_custom_msa_fixed/prot_custom_msa_fixed_model_0.cif
```

## Biological Context

Multiple Sequence Alignments are crucial for protein structure prediction because they provide:

1. **Evolutionary Constraints**: Show which residues are conserved vs variable
2. **Coevolution Signals**: Identify residue pairs that change together (indicating contacts)
3. **Structural Context**: Reveal functional and structural importance of regions
4. **Homology Information**: Leverage knowledge from related protein structures

### MSA Quality Factors

**High-Quality MSA** (MSA Server):
- ✅ Comprehensive database search
- ✅ Recent evolutionary relationships
- ✅ Diverse sequence coverage
- ✅ Automated quality filtering

**Limited MSA** (Pre-computed):
- ⚠️ Fixed at time of creation
- ⚠️ May miss recent sequences
- ⚠️ Limited diversity
- ⚠️ No quality optimization

## Performance Notes

| Aspect | MSA Server | Pre-computed MSA |
|--------|------------|------------------|
| **Runtime** | 30 seconds | 25 seconds |
| **Memory** | ~2GB GPU | ~2GB GPU |
| **Network** | Required | Not required |
| **Accuracy** | Higher | Lower |
| **Reproducibility** | Variable | Fixed |

## When to Use Each Approach

### Use MSA Server When:
- ✅ Network connectivity available
- ✅ Want highest accuracy
- ✅ Working with well-studied proteins
- ✅ Have computational time budget

### Use Pre-computed MSA When:
- ✅ Working offline
- ✅ Need reproducible results
- ✅ Have high-quality custom MSAs
- ✅ Studying novel/orphan proteins

## Comparison to Other Demos

| Demo | Overall Confidence | Complexity | Runtime |
|------|-------------------|------------|---------|
| Single Protein (MSA Server) | 81.1% | Low | 30s |
| **Custom MSA** | **69.1%** | **Low** | **25s** |
| Protein Multimer | 82.5% | High | 60s |
| Protein-Ligand Complex | 92.2% | High | 180s |

This demo ranks **lowest in confidence** due to MSA limitations, highlighting the critical importance of high-quality evolutionary information.

## Best Practices

1. **Prefer MSA Server**: Unless specific reasons exist, use `--use_msa_server`
2. **MSA Quality Control**: If using custom MSAs, ensure they're recent and diverse
3. **Validation**: Compare custom MSA results with MSA server when possible
4. **Documentation**: Always document MSA sources and generation methods

## Next Steps

For optimal results, see:
- `../single_protein/` - Same protein with MSA server (higher accuracy)
- `../protein_multimer/` - Multi-chain complexes with automatic MSA
- `../protein_ligand_complex/` - Multi-modal predictions with MSA server

## Citation

When using this demo, cite:
```
Boltz-1: Democratizing Biomolecular Interaction Modeling
Wohlwend et al., bioRxiv 2024
```

**Key Takeaway**: This demo demonstrates that MSA quality significantly impacts prediction accuracy. The MSA server's 12% improvement over pre-computed MSA shows why evolutionary information is crucial for protein structure prediction.