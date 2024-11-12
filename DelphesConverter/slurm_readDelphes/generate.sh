for i in {1..100}
do
    echo ${i}
    cp Delphes_submitter.slurm Delphes_submitter_${i}.slurm
    vim -c ":%s/_0/_${i}/g" -c":wq" Delphes_submitter_${i}.slurm
done
