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
