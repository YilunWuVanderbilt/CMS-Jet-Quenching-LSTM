CXX=g++
CXXFLAGS=-g -std=c++11 -Wall -pedantic

SRC=src

ROOTFLAG=`root-config --cflags --libs`

all: root_to_pu14_EFlow  root_to_pu14_delphesGEN root_to_pu14_track


root_to_pu14_CMS: $(SRC)/root_to_pu14_EFlow.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(ROOTFLAG)


root_to_pu14_delpheGENs: $(SRC)/root_to_pu14_delphesGEN.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(ROOTFLAG)

root_to_pu14_track: $(SRC)/root_to_pu14_track.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(ROOTFLAG)
	
.PHONY:
	clean
	all

clean:
  rm -f root_to_pu14_EFlow
	rm -f root_to_pu14_delphesGEN
	rm -f root_to_pu14_track
