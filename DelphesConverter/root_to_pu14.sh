#basedir=/store/user/yilun/thermal
basedir=/store/user/yilun/jewel/eventfiles
#basedir=/store/user/yilun/jewel_vac/eventfiles

for i in {1..100}
do
  echo $i
  #./root_to_pu14_CMS $basedir/Angantyr_Delphes/Angantyr_Delphes_${i}.root /nobackup/user/wuy55/jetml_data/thermal/Angantyr_pu14/EFlow/angantyr_${i}.pu14
  ./root_to_pu14_CMS $basedir/root/jewel_R_${i}.root $basedir/pu14_EFlow_1/jewel_R_${i}.pu14
  #./root_to_pu14_CMS $basedir/Angantyr_Delphes_pp/Angantyr_Delphes_${i}.root $basedir/pu14_EFlow_pp/angantyr_${i}.pu14
  #./root_to_pu14_track $basedir/root/jewel_R_${i}.root $basedir/pu14_Track_1/jewel_R_${i}.pu14
done
