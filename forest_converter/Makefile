CXX=g++
CXXFLAGS=-g -std=c++11 -Wall -pedantic

SRC=src

ROOTFLAG=`root-config --cflags --libs`

all: forest_to_pu14
	
forest_to_pu14: $(SRC)/forest_to_pu14.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(ROOTFLAG)

.PHONY:
	clean
	all

clean:
	rm -f forest_to_pu14
