
# Delphes Converter

We use the .pu14 file system to achieve full events consisting of both jewel hard process particles with thermal bkg particles. In this directory there are two steps: 1) get the Delphes root from GEN hepmc; 2) read the Delphes root produced from step 1 and output .pu14 files. Repeat the 2 steps for jewel-med, jewel-vac, and thermal bkg hepmc filesso the detector effects are applied to them separately. Later we reconstruct jets from this full events with a thermal bkg subtraction process. 

### 1. From hepmc file to DELPHES root

Submit `./slurm/hepmc_to_Delphes.slurm` to ACCRE, which runs the command line in `GetDelphes.sh` that runs the DELPHES module.

### 2. From DELPHES root to pu14 file

Firstly, `make` the directory to get `root_to_pu14_delphesGEN`, `root_to_pu14_track`, `root_to_pu14_EFlow` from the `src`.


The .pu14 saves the particle four-vector reading from the DELPHS root. For example, you can choose to run `root_to_pu14_delphesGEN` to save `[pT, eta, phi, Mass]` from Gen branch, or run `root_to_pu14_track` to save `[pT, eta, phi, Mass]` from Track branch, or run `root_to_pu14_EFlow` to save `[ET, eta,phi, Energy]` from EFlow neutral particle and save `[pT, eta,phi, Energy]` from EFlow track particle branch. You can add/modiy `src` files depending on which detector module you want to read from. 

Then, submit `./slurm/Delphes_to_pu14.slurm` to ACCRE, which runs the `root_to_pu14.sh` that excutes`root_to_pu14_XXX` that generate pu14 files for bkg, jewel_med, and jewel-vac separately.
