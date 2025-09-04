#!/bin/bash
#BSUB -J Performance_Comparison
#BSUB -q hpc
#BSUB -W 2
#BSUB -R "rusage[mem=15360MB]"
#BSUB -o Performance_Comparison_%J.out
#BSUB -e Performance_Comparison_%J.err

#BSUB -R "select[model == XeonGold6126]"

#BSUB -R "span[hosts=1]"
#BSUB -n 1

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python code.py