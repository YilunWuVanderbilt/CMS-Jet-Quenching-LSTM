#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --account=rke_group
#SBATCH --time=1-00:00:00
#SBATCH --job-name=hepmc_converter
#SBATCH --output=hepmc_converter.out

module restore mymodule #module saved on ACCRE with python&root version setup
cd /home/wuy55/hep_converter/DelphesConverter
./GetDelphes.sh
