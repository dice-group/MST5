### Instructions for noctua2 (slurm-based) cluster

**Load required modules**
```bash
module load lib/NCCL/2.12.12-GCCcore-11.3.0-CUDA-11.7.0
module load ai/PyTorch/1.12.0-foss-2022a-CUDA-11.7.0
module load vis/torchvision/0.13.1-foss-2022a-CUDA-11.7.0
```
**Activate Previously created Python Environment**
```bash
source mst5-venv/bin/activate
```

Set the hugginface cache to parallel file-system:
```bash
export HF_DATASETS_CACHE="/scratch/hpc-prf-lola/nikit/.cache/huggingface"
export HUGGINGFACE_HUB_CACHE="/scratch/hpc-prf-lola/nikit/.cache/huggingface"
```