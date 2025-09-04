#!/bin/bash
#BSUB -J PandasChunks100000
#BSUB -q hpc
#BSUB -W 10
#BSUB -R "rusage[mem=2048MB]"
#BSUB -o PandasChunks100000_%J.out
#BSUB -e PandasChunks100000_%J.err

#BSUB -R "select[model == XeonGold6126]"

#BSUB -R "span[hosts=1]"
#BSUB -n 1

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

/usr/bin/time -f"mem=%M KB runtime=%e s" 2>&1 python code.py /dtu/projects/02613_2025/data/dmi/2023_01.csv.zip 100000