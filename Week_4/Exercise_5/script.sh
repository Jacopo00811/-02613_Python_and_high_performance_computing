#!/bin/bash
#BSUB -J Haversine
#BSUB -q hpc
#BSUB -W 10
#BSUB -R "rusage[mem=1024MB]"
#BSUB -o Performance_Comparison_%J.out
#BSUB -e Performance_Comparison_%J.err

#BSUB -R "select[model == XeonGold6126]"

#BSUB -R "span[hosts=1]"
#BSUB -n 1

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

python -m cProfile -s cumulative code.py /dtu/projects/02613_2025/data/locations/locations_5000.csv