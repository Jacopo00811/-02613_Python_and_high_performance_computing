#!/bin/bash
#BSUB -J Hello_World
#BSUB -q hpc
#BSUB -W 2
#BSUB -R "rusage[mem=512MB]"
#BSUB -o Hello_world_%J.out
#BSUB -e Hello_world_%J.err

##BSUB -u s215158@dtu.dk
#BSUB -B 
#BSUB -N 

#BSUB -R "select[model == XeonGold6126]"
#BSUB -R "select[avx512]"

#BSUB -R "span[hosts=1]"
#BSUB -n 4


/bin/sleep 60