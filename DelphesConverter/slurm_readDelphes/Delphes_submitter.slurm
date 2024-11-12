#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=10G
#SBATCH --account=rke_group
#SBATCH --time=1-00:00:00
#SBATCH --job-name=delphes_converter_0
#SBATCH --output=delphes_converter_0.out

basedir=store/user/yilun/jewel/eventfiles/

cd /home/wuy55/JetML

singularity exec jetml_gpu_latest.sif python3 /home/wuy55/hep_converter/DelphesConverter/ReadDelphes_EFlow.py -i $basedir/root/jewel_R_0.root -o $basedir/pu14_EFlow/jewel_R_0.pu14


