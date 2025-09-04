#!/bin/sh
#BSUB -q hpc
#BSUB -J matrix
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -R "select[model == XeonGold6126 && avx512]"
#BSUB -W 00:10
#BSUB -o output/array_job_%J.out
#BSUB -e output/array_job_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

export OMP_NUM_THREADS=8  
export MKL_NUM_THREADS=8 
export MPI_NUM_THREADS=8 
export OPENBLAS_NUM_THREADS=8

python script.py $LSB_JOBID