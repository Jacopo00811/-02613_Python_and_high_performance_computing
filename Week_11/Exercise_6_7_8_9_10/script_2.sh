#!/bin/sh
#BSUB -q hpc
#BSUB -J Combine
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -W 00:10
#BSUB -o batch_output/Combine%J.out
#BSUB -e batch_output/Combine%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python combine.py