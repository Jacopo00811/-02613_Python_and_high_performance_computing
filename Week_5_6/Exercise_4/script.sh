#!/bin/bash
#BSUB -J Pi
#BSUB -q hpc
#BSUB -W 10
#BSUB -R "rusage[mem=2048MB]"
#BSUB -o Pi_%J.out
#BSUB -e Pi_%J.err

#BSUB -R "select[model == XeonGold6126]"

#BSUB -R "span[hosts=1]"
#BSUB -n 10

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python code.py