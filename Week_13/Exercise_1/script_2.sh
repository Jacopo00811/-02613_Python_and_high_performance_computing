#!/bin/sh
#BSUB -q hpc
#BSUB -J Exercise_1
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -W 00:10
#BSUB -o /work3/02613/dump/JJ/job_Exercise_1_output%J.out
#BSUB -e /work3/02613/dump/JJ/job_Exercise_1_error%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python -u code.py \
    1> /work3/02613/dump/JJ/job_Exercise_1_output${LSB_JOBID}.txt \
    2> /work3/02613/dump/JJ/job_Exercise_1_error${LSB_JOBID}.txt