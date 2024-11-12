for i in {1..100}
do
    echo ${i}
    cp doCS.slurm doCS_${i}.slurm
    vim -c ":%s/_0/_${i}/g" -c":wq" doCS_${i}.slurm
done
