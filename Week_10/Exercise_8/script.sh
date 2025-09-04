#!/bin/sh
#BSUB -q c02613
#BSUB -J cupy
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -W 00:05
#BSUB -o batch_output/gpujob_%J.out
#BSUB -e batch_output/gpujob_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

time python points.py /dtu/projects/02613_2025/data/locations/locations_5000.csv
# nsys profile -o oneloop_profile python points.py /dtu/projects/02613_2025/data/locations/locations_5000.csv
# nsys profile -o noloop_profile python points.py /dtu/projects/02613_2025/data/locations/locations_5000.csv