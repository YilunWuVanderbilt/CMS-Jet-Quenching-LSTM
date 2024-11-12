#include <fstream>
#include <iostream>
#include <cmath>
using namespace std;

#include "TFile.h"
#include "TTree.h"

#define MAX 20000

int main(int argc, char *argv[])
{
   if(argc != 3)
   {
      cerr << "Usage: " << argv[0] << " InputRootFile OutputFileName" << endl;
      return -1;
   }

   ofstream out(argv[2]);
   TFile *_File = TFile::Open(argv[1]);

   TTree *Tree = (TTree *)_File->Get("Delphes");
   
   int NP;
   int PID[MAX];
   float Weight;
   float PT[MAX], Eta[MAX], Phi[MAX], Mass[MAX], PStatus[MAX];
   Tree->SetBranchAddress("Event.Weight", &Weight);
   Tree->SetBranchAddress("Particle_size", &NP);
   Tree->SetBranchAddress("Particle.PID",&PID);
   Tree->SetBranchAddress("Particle.PT",&PT);
   Tree->SetBranchAddress("Particle.Eta",&Eta);
   Tree->SetBranchAddress("Particle.Phi",&Phi);
   Tree->SetBranchAddress("Particle.Mass",&Mass);
   Tree->SetBranchAddress("Particle.Status", &PStatus);

   int EntryCount = Tree->GetEntries();
   for(int iE = 0; iE < EntryCount; iE++)
   {
      Tree->GetEntry(iE);
      out << "# event " << iE << endl;
      //out << "weight " << Weight << endl;
      
      for(int i = 0; i < NP; i++)
      {
        if(Eta[i]>-3.0 and Eta[i]<3.0){
            out << PT[i] << " " << Eta[i] << " " << Phi[i] << " " << Mass[i] << " " << PID[i] << " " << 0 << endl;
            //out << Px[i] << " " << Py[i] << endl;
        }

      }
      out << "end" << endl;
   }

   _File->Close();
   out.close();

   return 0;
}
