#!/bin/bash
#BSUB -J Mandelbrot_memmap
#BSUB -q hpc
#BSUB -W 10
#BSUB -R "rusage[mem=2048MB]"
#BSUB -o Mandelbrot_memmap_%J.out
#BSUB -e Mandelbrot_memmap_%J.err

#BSUB -R "select[model == XeonGold6126]"

#BSUB -R "span[hosts=1]"
#BSUB -n 1

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

/usr/bin/time -f"mem=%M KB runtime=%e s" 2>&1 python code.py