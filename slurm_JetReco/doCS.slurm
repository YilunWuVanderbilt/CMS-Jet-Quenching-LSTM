#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=10G
#SBATCH --account=rke_group
#SBATCH --time=1-00:00:00
#SBATCH --job-name=jewel_R_0
#SBATCH --output=jewel_R_0.out

cd /home/wuy55/JetML
singularity exec --bind /store jetml_gpu_latest.sif ./doStructure.sh -i /store/user/yilun/jewel/eventfiles/pu14_EFlow_1/jewel_R_0.pu14 -b /store/user/yilun/thermal/Angantyr_pu14/angantyr_0.pu14 -o /store/user/yilun/jewel_med_train/Delphes_EFlow/jewel_R_mult7000_0.root -n 2000
