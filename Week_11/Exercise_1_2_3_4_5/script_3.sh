#!/bin/sh
#BSUB -q hpc
#BSUB -J job
#BSUB -n 1
#BSUB -w 1234567
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -W 00:10
#BSUB -o output/job_%J.out
#BSUB -e output/job_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python script.py $LSB_JOBID