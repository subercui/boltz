# Boltz Project Notes

## Project Overview
- **Goal**: Learn and reproduce Boltz1 molecular structure prediction model
- **Repository**: https://github.com/jwohlwend/boltz/tree/v1.0.0
- **Environment**: Using `uv` for dependency management with Python 3.11.13

## Chat History Summary

### Session 1 - Installation Verification & Training Setup (2025-07-28)
- **Context**: Initial setup verification and successful training setup for Boltz1 reproduction project
- **Key Actions**:
  - Verified Python 3.11.13 environment with `uv` management
  - Confirmed Boltz 1.0.0 package installation
  - Tested CLI functionality (`boltz predict --help` works)
  - Ran test suite: 2/4 layer tests passed, regression tests require model weights
  - Verified development tools: pytest and ruff installed and functional
  - **Analyzed training configurations**: full.yaml, structure.yaml, confidence.yaml
  - **Studied training pipeline**: Lightning-based with Hydra configs
  - **Downloaded training data**: RCSB processed targets & MSAs (~250GB)
  - **Created pilot config**: `scripts/train/configs/pilot_structure_train.yaml`
  - **Fixed PyTorch 2.7 compatibility**: Updated LRScheduler for verbose parameter removal
  - **Successfully tested training**: Debug mode works with 180K train/550 val samples

- **Key Decisions**:
  - Use `uv pip install` for dependency management (not regular pip)
  - Environment activation: `source .venv/bin/activate`
  - Focus on learning/reproduction rather than production deployment
  - **Training approach**: Two-stage (structure-only → confidence) or full end-to-end
  - **Data setup**: RCSB only (ignoring OpenFold for now)

- **Technical Findings**:
  - Core layer tests (outer_product_mean, triangle_attention) pass
  - Regression tests fail due to missing model weights (expected)
  - Code style: 1613 ruff violations found (typical for research code)
  - Dependencies properly installed: torch 2.7.1+cu126, pytorch-lightning 2.4.0
  - **Training configurations**:
    - Structure-only: 20 sampling steps (fast), no confidence
    - Confidence-only: Requires pretrained structure model
    - Full: 200 sampling steps, both structure + confidence
  - **Model**: 439M trainable parameters, runs on NVIDIA RTX A6000
  - **Data**: 180,540 training samples, 550 validation samples loaded successfully

## Todo List

### Current Planning
- ✅ Environment setup and verification complete
- ✅ Training data downloaded and configured (180K samples)
- ✅ Debug training verified working (439M params model)
- 🔄 **READY**: Full structure training ready to launch

### Completed Tasks
- ✅ Explore core model architecture (`src/boltz/model/model.py`)
- ✅ Understand data pipeline (`src/boltz/data/`)
- ✅ Review training configurations (`scripts/train/configs/`)
- ✅ Create pilot training config with real data paths
- ✅ Fix PyTorch 2.7 compatibility issues
- ✅ Test training pipeline with real data

### Next Steps
- 🎯 **Launch full structure training**: `python scripts/train/train.py scripts/train/configs/pilot_structure_train.yaml`
- 📊 Monitor training metrics and progress
- 🔧 Optional: Enable wandb logging for better monitoring
- 📈 Train confidence model after structure training completes

### Data Requirements (from docs/training.md)
**Pre-processed Datasets** (~250GB total):
- RCSB structures: `wget https://boltz1.s3.us-east-2.amazonaws.com/rcsb_processed_targets.tar`
- RCSB MSAs: `wget https://boltz1.s3.us-east-2.amazonaws.com/rcsb_processed_msa.tar`
- OpenFold structures: `wget https://boltz1.s3.us-east-2.amazonaws.com/openfold_processed_targets.tar`
- OpenFold MSAs: `wget https://boltz1.s3.us-east-2.amazonaws.com/openfold_processed_msa.tar`
- Symmetry file: `wget https://boltz1.s3.us-east-2.amazonaws.com/symmetry.pkl`

**Training Commands**:
```bash
# Debug mode first (single process)
python scripts/train/train.py scripts/train/configs/structure.yaml debug=1

# Full structure training
python scripts/train/train.py scripts/train/configs/structure.yaml

# Confidence training (requires structure checkpoint)
python scripts/train/train.py scripts/train/configs/confidence.yaml
```

**GPU Memory Considerations**:
- max_tokens=512, max_atoms=4608 (full GPU)
- max_tokens=256, max_atoms=2304 (smaller GPU)
- max_tokens=384, max_atoms=3456 (medium GPU)

### Future Features/Investigations
- Deep dive into diffusion-based structure prediction approach
- Understand attention mechanisms (triangular attention)
- Study MSA (Multiple Sequence Alignment) processing
- Download and test with official training data (~250GB)
- Set up multi-dataset training (PDB + OpenFold distillation)

## Development Environment Notes
- **Python**: 3.11.13 (in .venv)
- **Key Dependencies**: torch, pytorch-lightning, rdkit, hydra-core
- **Testing**: pytest with markers (`-m "not slow"`, `-m regression`)
- **Linting**: ruff check/format
- **Training**: Hydra-based configs in `scripts/train/configs/`

## Architecture Understanding
- **Core Model**: Diffusion-based biomolecular structure prediction
- **Key Components**: Pairformer (48 blocks), MSA Module (4 blocks), Diffusion Module, Confidence Module
- **Input Types**: Proteins, DNA/RNA, small molecules, complex YAML inputs
- **Output**: 3D atomic coordinates + confidence scores (pLDDT, PAE, PDE)