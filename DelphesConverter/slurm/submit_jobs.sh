for i in {1..100}
do
    echo Delphes_submitter_${i}.slurm
    sbatch Delphes_submitter_${i}.slurm
done
