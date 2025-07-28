# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment Setup

This project uses `uv` for dependency management. Always activate the virtual environment before running commands:

```bash
source .venv/bin/activate
```

## Development Commands

### Installation
```bash
# Install in development mode
pip install -e .

# Install with development dependencies
pip install -e .[test,lint]
```

### Testing
```bash
# Run all tests except slow ones
pytest tests/ -m "not slow"

# Run only regression tests  
pytest tests/ -m regression

# Run tests for specific components
pytest tests/model/layers/

# Run all tests including slow ones
pytest tests/
```

### Linting and Code Quality
```bash
# Run ruff linter and formatter
ruff check src/
ruff format src/

# Check specific files
ruff check src/boltz/model/model.py
```

### Inference
```bash
# Basic prediction with MSA server
boltz predict input_path --use_msa_server

# See all prediction options
boltz predict --help
```

### Training
```bash
# Train with full configuration
python scripts/train/train.py configs/full.yaml

# Train structure-only model
python scripts/train/train.py configs/structure.yaml

# Train confidence-only model  
python scripts/train/train.py configs/confidence.yaml
```

## Architecture Overview

Boltz is a diffusion-based biomolecular structure prediction model built on PyTorch Lightning. The architecture consists of several key components:

### Core Model (`src/boltz/model/model.py`)
- **Boltz1**: Main Lightning module containing the complete architecture
- **Pairformer**: 48-block transformer for pairwise sequence representations
- **MSA Module**: Processes multiple sequence alignments (4 blocks, 64 MSA sequences)
- **Diffusion Module**: Atom-level coordinate generation via score-based diffusion
- **Confidence Module**: Predicts confidence scores (pLDDT, PAE, PDE)

### Data Pipeline (`src/boltz/data/`)
- **Input Processing**: Supports FASTA, YAML, and directory inputs
- **Tokenization**: Converts biological sequences to model tokens
- **Feature Generation**: Creates embeddings and pair representations
- **MSA Generation**: Uses MMSeqs2 server or precomputed alignments

### Model Components (`src/boltz/model/modules/`)
- **`diffusion.py`**: AtomDiffusion implementation for structure sampling
- **`trunk.py`**: Core transformer blocks and input embedding
- **`confidence.py`**: Confidence prediction networks
- **`transformers.py`**: Attention mechanisms and transformer layers

### Attention Layers (`src/boltz/model/layers/`)
- **Triangular Attention**: Specialized for protein folding in `triangular_attention/`
- **Multi-head Attention**: Standard transformer attention in `attention.py`
- **Outer Product Mean**: Pair representation operations in `outer_product_mean.py`

## Key Data Types (`src/boltz/data/types.py`)
- **Structure**: Core molecular structure representation
- **MSA**: Multiple sequence alignment data
- **Target**: Training target with constraints and metadata
- **Record**: Input sequence record with chain information

## Configuration System

Uses Hydra for configuration management:
- **`scripts/train/configs/full.yaml`**: Complete training configuration
- **`scripts/train/configs/structure.yaml`**: Structure-only training
- **`scripts/train/configs/confidence.yaml`**: Confidence-only training

## Supported Input Types
1. **Proteins**: 20 standard amino acids + modified residues
2. **Nucleic Acids**: DNA/RNA with standard and modified nucleotides
3. **Small Molecules**: Via SMILES or CCD codes
4. **Complex Inputs**: YAML format for covalent bonds, pockets, constraints

## Testing Strategy
- **Regression Tests**: Validate model outputs haven't changed (`test_regression.py`)
- **Layer Tests**: Unit tests for specific model components
- **Markers**: Use `slow` and `regression` markers to categorize tests

## Development Notes
- **Mixed Precision**: Uses FP32 by default, FP16/BF16 configurable
- **Recycling**: 3 recycling steps for iterative refinement
- **EMA**: Exponential moving average for stable training
- **Diffusion Steps**: 200 sampling steps by default