# Environment
To pull the container, see "https://github.com/ustcllh/JetML/tree/27482d7d258a01e1b7197c25ce4f4fbca89baa34"

# CMS-Jet-Quenching-LSTM
Using LSTM model to indentify different levels of jet quenching. 

### 1. Read from hiforest root and write particle four vector info to the pu14 file
```
basedir=/where/the/forest/root/is/stored/
./forest_to_pu14 $basedir/forestrootname.root $basedir/outputname.pu14
```
#### 1.1 For Delphes root generation and pu14 conversion, see `./DelphesConverter/README`

### 2. Read from pu14 file and reconstruct jets from the constituents. Also extract the substructre observables
```
cd /your/project/path/
singularity exec jetml_gpu_latest.sif ./doStructure.sh -i /where/you/store/the/pu14file/outputname.pu14 -o /where/you/want/to/store/the/training/data/training_data.root -n 2000
```
#### 2.1 For jet reconstruction and thermal bkg subtraction with DELPHES detector effets, run the command in `./slurm_JetReco/doCS.slurm`

In `./slurm_JetReco/doCS.slurm`, `dostructure.sh` runs the python code `doStructure_Delphes.py`, which is the core part doing thermal bkg subtraction and jet reconstruction. It requires fastjet package, so the easiest way is pull the singularity container `jetml_gpu_latest.sif` from "https://github.com/ustcllh/JetML/tree/27482d7d258a01e1b7197c25ce4f4fbca89baa34" to get the envirment setup quickly. 
