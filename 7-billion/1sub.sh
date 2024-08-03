#!/bin/bash
#SBATCH --job-name=10000
#SBATCH --output=py.out
#SBATCH --error=py1.err
#SBATCH --mail-type=NONE
#SBATCH --mail-user=some_user@some_domain.com
#SBATCH --time=7-00:00:00 # adjust time
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --mem-per-cpu=100gb
#SBATCH --account=rmirandaquintana
#SBATCH --qos=rmirandaquintana

ml python
python distance.py