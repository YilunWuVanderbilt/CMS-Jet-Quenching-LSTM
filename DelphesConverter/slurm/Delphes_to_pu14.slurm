#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=10G
#SBATCH --account=rke_group
#SBATCH --time=1-00:00:00
#SBATCH --job-name=hepmc_converter2
#SBATCH --output=hepmc_converter2.out

module restore myroot
cd /home/wuy55/DelphesConverter
./root_to_pu14.sh
