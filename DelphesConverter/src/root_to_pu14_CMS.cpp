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
   float Weight;
   float ET[MAX], Eta[MAX], Phi[MAX],Energy[MAX];
   int NP_T;
   int PID_T[MAX];
   float PT_T[MAX], Eta_T[MAX], Phi_T[MAX], Mass_T[MAX]; 
   
   int NP_P;
   float ET_P[MAX], Eta_P[MAX], Phi_P[MAX],Energy_P[MAX];
   
   Tree->SetBranchAddress("Event.Weight", &Weight);
   Tree->SetBranchAddress("EFlowNeutralHadron_size", &NP);
   Tree->SetBranchAddress("EFlowNeutralHadron.ET",&ET);
   Tree->SetBranchAddress("EFlowNeutralHadron.Eta",&Eta);
   Tree->SetBranchAddress("EFlowNeutralHadron.Phi",&Phi);
   Tree->SetBranchAddress("EFlowNeutralHadron.E",&Energy);
   
   Tree->SetBranchAddress("EFlowTrack_size", &NP_T);
   Tree->SetBranchAddress("EFlowTrack.PID",&PID_T);
   Tree->SetBranchAddress("EFlowTrack.PT",&PT_T);
   Tree->SetBranchAddress("EFlowTrack.Eta",&Eta_T);
   Tree->SetBranchAddress("EFlowTrack.Phi",&Phi_T);
   Tree->SetBranchAddress("EFlowTrack.Mass",&Mass_T);

   Tree->SetBranchAddress("EFlowPhoton_size", &NP_P);
   Tree->SetBranchAddress("EFlowPhoton.ET",&ET_P);
   Tree->SetBranchAddress("EFlowPhoton.Eta",&Eta_P);
   Tree->SetBranchAddress("EFlowPhoton.Phi",&Phi_P);
   Tree->SetBranchAddress("EFlowPhoton.E",&Energy_P);
   
   int EntryCount = Tree->GetEntries();
   for(int iE = 0; iE < EntryCount; iE++)
   {
      Tree->GetEntry(iE);
      out << "# event " << iE << endl;
      out << "weight " << Weight << endl;
      
      for(int i = 0; i < NP; i++)
      {
         
        out << ET[i] << " " << Eta[i] << " " << Phi[i] << " " << Energy[i] << " " << 0 << " " << 1 << endl;

      }
      
      for(int i = 0; i < NP_T; i++)
      {
       
        out << PT_T[i] << " " << Eta_T[i] << " " << Phi_T[i] << " " << Mass_T[i] << " " << PID_T[i] << " " << 1 << endl;
        
      }
      
    for(int i = 0; i < NP_P; i++)
      {
       
        out << ET_P[i] << " " << Eta_P[i] << " " << Phi_P[i] << " " << Energy_P[i] << " " << 22 << " " << 1 << endl;
        
      }
      out << "end" << endl;
   }

   _File->Close();
   out.close();

   return 0;
}
