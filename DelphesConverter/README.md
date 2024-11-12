
# Delphes Converter

We use the .pu14 file system to achieve full events consisting of both jewel hard process particles with thermal bkg particles. In this directory there are two steps: 1) get the Delphes root from GEN hepmc; 2) read the Delphes root produced from step 1 and output .pu14 files. Repeat the 2 steps for jewel-med, jewel-vac, and thermal bkg hepmc filesso the detector effects are applied to them separately. Later we reconstruct jets from this full events with a thermal bkg subtraction process. 

### 1. From hepmc file to DELPHES root

Submit `slurm_GetDelphes` to ACCRE, which runs the command line in `GetDelphes.sh` that runs the DELPHES module.

### 2. From DELPHES root to pu14 file

Submit `slurm_readDelphes` to ACCRE, which runs the  `ReadDelphes_XXX.py` that generate pu14 files.

The .pu14 saves the particle four-vector reading from the DELPHS root. For example, you can choose to run `ReadDelphes_GenParticle.py` to save `[px, py, pz, Mass]` from Gen branch, or run `ReadDelphes_Track.py` to save `[pT, eta, phi, Mass]` from Track branch, or run `ReadDelphes_EFlow.py` to save `[ET, eta,phi, Energy]` from EFlow branch--depending on which detector module you want to use. 

This step may requires to be run within singuarity container `jetml_gpu_latest.sif` that is installed in `/home/wuy55/JetML`. You can pull the container to somewhere else. To pull the container, see "https://github.com/ustcllh/JetML/tree/27482d7d258a01e1b7197c25ce4f4fbca89baa34"
