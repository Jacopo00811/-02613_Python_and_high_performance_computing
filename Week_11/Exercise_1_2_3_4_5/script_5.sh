#!/bin/sh
#BSUB -q hpc
#BSUB -J job2
#BSUB -n 1
#BSUB -w ended(21241475)
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -W 00:10
#BSUB -o output/job2_%J.out
#BSUB -e output/job2_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python script.py $LSB_JOBID