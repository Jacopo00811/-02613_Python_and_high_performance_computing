#!/bin/sh
#BSUB -q hpc
#BSUB -J Exercise_1
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -W 00:10
#BSUB -o /work3/02613/dump/JJ/job_Exercise_1_%J.out
#BSUB -e /work3/02613/dump/JJ/job_Exercise_1_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python -u code.py