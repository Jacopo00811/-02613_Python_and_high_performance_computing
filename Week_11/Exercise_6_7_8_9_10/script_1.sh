#!/bin/sh
#BSUB -q hpc
#BSUB -J Hist[1-203]
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -W 00:10
#BSUB -o batch_output/arrayHist%J.out
#BSUB -e batch_output/arrayHist%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python code.py $LSB_JOBINDEX