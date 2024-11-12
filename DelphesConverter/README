
# Delphes Converter
```
basedir=/store/user/yilun/jewel/eventfiles

cd /home/wuy55/JetML

singularity exec jetml_gpu_latest.sif python3 /your/path/of/DelphesConverter/ReadDelphes_GenParticle.py -i $basedir/root/jewel_R_0.root -o $basedir/pu14/jewel_R_0.pu14
```
# Environment
To pull the container, see "https://github.com/ustcllh/JetML/tree/27482d7d258a01e1b7197c25ce4f4fbca89baa34"

# CMS-Jet-Quenching-LSTM
Using LSTM model to indentify different levels of jet quenching. 

### 1. Read from hiforest root and write particle four vector info to the pu14 file
```
basedir=/where/the/forest/root/is/stored/
./forest_to_pu14 $basedir/forestrootname.root $basedir/outputname.pu14
```

### 2. Read from pu14 file and reconstruct jets from the constituents. Also extract the substructre observables
```
cd /your/project/path/
singularity exec jetml_gpu_latest.sif ./doStructure.sh -i /where/you/store/the/pu14file/outputname.pu14 -o /where/you/want/to/store/the/training/data/training_data.root -n 2000
```
