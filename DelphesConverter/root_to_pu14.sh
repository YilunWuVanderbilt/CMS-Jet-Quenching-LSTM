basedir_thermal=/store/user/yilun/thermal
basedir_jewelmed=/store/user/yilun/jewel/eventfiles
basedir_jewwelvac=/store/user/yilun/jewel_vac/eventfiles

for i in {1..100}
do
  echo $i
  
  ./root_to_pu14_EFlow $basedir_thermal/Angantyr_Delphes/Angantyr_Delphes_${i}.root$ basedir_thermal/Angantyr_pu14//angantyr_${i}.pu14
  ./root_to_pu14_EFlow $basedir_jewelmed/root/jewel_R_${i}.root $basedir_jewelmed/pu14_EFlow_1/jewel_R_${i}.pu14
  ./root_to_pu14_EFlow $basedir_jewelvac/root/jewel_R_${i}.root $basedir_jewelvac/pu14_EFlow_1/jewel_R_${i}.pu14
  #./root_to_pu14_track $basedir/root/jewel_R_${i}.root $basedir/pu14_Track_1/jewel_R_${i}.pu14
done
