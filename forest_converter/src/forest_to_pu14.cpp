#include <fstream>
#include <iostream>
#include <cmath>
#include<vector>
using namespace std;

#include "TFile.h"
#include "TTree.h"


int main(int argc, char *argv[])
{
    if(argc != 3) //There are three arguments to run the executable file: ./forest_to_pu14 InputRootFile OutputFileName
    {
        cerr << "Usage: " << argv[0] << " InputRootFile OutputFileName" << endl;
        return -1;
    }

    ofstream out(argv[2]); //take the output file name from the third argument: HiForestMiniAOD_13.pu14
    TFile File(argv[1]); //take the input file name from the second argument:HiForestMiniAOD_13.root
    TTree *Tree = (TTree *)File.Get("particleFlowAnalyser/pftree");
    
    int nPF;
    double Weight = 1;
    
    vector<int> *pfId = new vector<int>;
    vector<float> *pfPt = new vector<float>;
    vector<float> *pfEta = new vector<float>;
    vector<float> *pfPhi = new vector<float>;
    vector<float> *pfM = new vector<float>;
    
    Tree->SetBranchAddress("pfId", &pfId);
    Tree->SetBranchAddress("pfPt", &pfPt);
    Tree->SetBranchAddress("pfEta", &pfEta);
    Tree->SetBranchAddress("pfPhi", &pfPhi);
    Tree->SetBranchAddress("pfM", &pfM);
    Tree->SetBranchAddress("nPF", &nPF);
    
    int EntryCount = Tree->GetEntries();
    for(int iE = 0; iE < EntryCount; iE++)
    {
        Tree->GetEntry(iE);
        
        out << "# event " << iE << endl;
        out << "weight " << Weight << endl;
        
        for(int i = 0; i < nPF; i++)
        {
            
            out << pfPt->at(i) << " " << pfEta->at(i) << " " << pfPhi->at(i) << " " << pfM->at(i) << " " << pfId->at(i) << " " << 0 << endl;
        
        }
        out << "end" << endl;
    }
        
    File.Close();
    out.close();
    return 0;
}
