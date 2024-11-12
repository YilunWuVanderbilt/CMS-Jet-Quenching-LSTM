#basedir=store/user/yilun/jewel_vac/eventfiles/hepmc_PPJJ_allpT #pp hepmc location
basedir=store/user/yilun/jewel/eventfiles/hepmc_PPJJ_allpT #PbPb hepmc location
#basedir=/store/user/yilun/thermal #thermal bkg location

cd /home/wuy55/Delphes-3.5.0/

for i in {1..100}
do
  echo $i
  ./DelphesHepMC2 cards/MyCards/my_delphes_card_EFlow.tcl $basedir/root/jewel_R_${i}.root $basedir/hepmc/jewel_R_${i}.hepmc
done
