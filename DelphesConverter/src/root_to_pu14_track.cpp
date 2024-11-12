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
   
   float Weight;
   int NP_T;
   int PID_T[MAX];
   float PT_T[MAX], Eta_T[MAX], Phi_T[MAX], Mass_T[MAX]; 
   
   
   Tree->SetBranchAddress("Event.Weight", &Weight);
   
   Tree->SetBranchAddress("Track_size", &NP_T);
   Tree->SetBranchAddress("Track.PID",&PID_T);
   Tree->SetBranchAddress("Track.PT",&PT_T);
   Tree->SetBranchAddress("Track.Eta",&Eta_T);
   Tree->SetBranchAddress("Track.Phi",&Phi_T);
   Tree->SetBranchAddress("Track.Mass",&Mass_T);

   
   int EntryCount = Tree->GetEntries();
   for(int iE = 0; iE < EntryCount; iE++)
   {
      Tree->GetEntry(iE);
      out << "# event " << iE << endl;
      out << "weight " << Weight << endl;
      
      
      for(int i = 0; i < NP_T; i++)
      {
       
        out << PT_T[i] << " " << Eta_T[i] << " " << Phi_T[i] << " " << Mass_T[i] << " " << PID_T[i] << " " << 1 << endl;
        
      }
      out << "end" << endl;
   }

   _File->Close();
   out.close();

   return 0;
}
