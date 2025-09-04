#!/bin/bash
#BSUB -J python
#BSUB -q hpc
#BSUB -W 15
#BSUB -R "rusage[mem=512MB]"
#BSUB -o batch_output/python_%J.out
#BSUB -e batch_output/python_%J.err
#BSUB -R "span[hosts=1]"
#BSUB -n 1
# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

# Run Pythonscript
python code.py ./input.npy 10


