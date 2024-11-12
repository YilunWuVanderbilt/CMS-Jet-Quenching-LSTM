for i in {1..100}
do
    echo doCS_${i}.slurm
    sbatch doCS_${i}.slurm
done
