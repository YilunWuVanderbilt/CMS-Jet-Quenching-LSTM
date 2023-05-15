%module TrkEff2018PbPb

%{
#define SWIG
#include "TrkEff2018PbPb.h"
%}

%include "std_string.i"

%apply const std::string& { std::string& collectionName };

%include "TrkEff2018PbPb.h"
