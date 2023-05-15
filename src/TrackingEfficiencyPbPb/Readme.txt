Get the tracking efficiency tables(root files) from: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HITracking2018PbPb

Environment Setting:
export ROOTSYS=/workspace/root
export PATH=$ROOTSYS/bin:$PATH
export LD_LIBRARY_PATH=$ROOTSYS/lib:$LD_LIBRARY_PATH
source /workspace/root/bin/thisroot.sh

Compiling lines once you have the .i interfacing file: 
g++ `root-config --cflags` `root-config --libs` -std=c++11 -fPIC -fno-lto -c TrkEff2018PbPb_wrap.cxx -o TrkEff2018PbPb_wrap.o  `python3-config --includes` -ITrackingEfficiencyconfig 
g++ `root-config --cflags` `root-config --libs` -std=c++11 -fPIC -fno-lto -c TrkEff2018PbPb_wrap.cxx -o TrkEff2018PbPb_wrap.o  `python3-config --includes` 
g++ -std=c++11 -fPIC -fno-lto TrkEff2018PbPb.o TrkEff2018PbPb_wrap.o -shared -o _TrkEff2018PbPb.so `python3-config --ldflags`  `python3-config --libs` -lstdc++ -L/workspace/root/lib -lCore –lRIO 

Example of testing the compiled interfacing files:
>>> from TrkEff2018PbPb import*
>>> trkEff = TrkEff2018PbPb("general", "", False, "./Table/")
TrkEff2018PbPb class opening in general tracks mode!
>>> correction = trkEff.getEfficiency(1.0, 1.0, 20)
