
########################################
#               parsing
########################################
import argparse

parser = argparse.ArgumentParser(description='JetML CML Parser')
parser.add_argument('-i','--input', help='Input file name', required=True) # input file "HiForestMiniAOD_PythiaHydjet2018_1.root":Dijet events simulation with bkg.
parser.add_argument('-o','--output',help='Output file name', required=True)
parser.add_argument('-n',help='number of events', required=False)

args = parser.parse_args()

# print values
print('*********Initialization**********')
print('Input file:\t%s' % args.input)
print('Output file: \t%s' % args.output)
if args.n:
    print('Number of events:\t%s' % args.n)
else:
    print('Number of events:\t100')
print('*********************************')

########################################
#              Root Tree
########################################

from ROOT import TFile, TTree, TLorentzVector
from array import array

output = TFile(args.output, 'recreate') # Create the output file from the argument command
trcse = TTree('csejet', 'cs event wide') # Create the tree

maxn = 100
# event variables
x = array('f', [0.])
y = array('f', [0.])
weight = array('f', [0.])
event = array('i', [0])

# jet variables
eta = array('f', [0.])
phi = array('f', [0.])
jetpt = array('f', [0.])
depth = array('i', [0])
jetm = array('f', [0.])

# constituents
cn = array('i', [0])
cpt = array('f', 500 * [0.])
cdeta = array('f', 500 * [0.])
cdphi = array('f', 500 * [0.])
cpid = array('i', 500 * [0])

# groomed jet variables
jetmg = array('f', [0.])

# sequential variables
z = array('f', maxn * [0.])
delta = array('f', maxn * [0.])
kperp = array('f', maxn * [0.])
m = array('f', maxn * [0.])

def set_branches(tr):
    # event variables
    tr.Branch('event', event, 'event/I')
    tr.Branch('x', x, 'x/F')
    tr.Branch('y', y, 'y/F')
    tr.Branch('weight', weight, 'weight/F')

    # jet variables
    tr.Branch('eta', eta, 'eta/F')
    tr.Branch('phi', phi, 'phi/F')
    tr.Branch('jetpt', jetpt, 'jetpt/F')
    tr.Branch('depth', depth, 'depth/I')
    tr.Branch('jetm', jetm, 'jetm/F')

    # constituents
    tr.Branch('cn', cn, 'cn/I')
    tr.Branch('cpt', cpt, 'cpt[cn]/F')
    tr.Branch('cdeta', cdeta, 'cdeta[cn]/F')
    tr.Branch('cdphi', cdphi, 'cdphi[cn]/F')
    tr.Branch('cpid', cpid, 'cpid[cn]/I')

    # groomed jet variables
    tr.Branch('jetmg', jetmg, 'jetmg/F')

    # substructure variables without grooming
    tr.Branch('z', z, 'z[depth]/F')
    tr.Branch('delta', delta, 'delta[depth]/F')
    tr.Branch('kperp', kperp, 'kperp[depth]/F')
    tr.Branch('m', m, 'm[depth]/F')

set_branches(trcse) # jet clustering using event wide subtraction method. 


########################################
#                Jet
########################################

import sys

fastjet_dir='/workspace/fastjet/lib/python3.6/site-packages'
sys.path.append(fastjet_dir)
import fastjet as fj
from src.JetML.Event import *
from src.JetTree.JetTree import *

# constituent subtraction python module
constituent_subtractor_dir='/workspace/ConstituentSubtractor'
sys.path.append(constituent_subtractor_dir)
import ConstituentSubtractor as cs
import IterativeConstituentSubtractor as ics


# soft drop groomer
zcut=0.1
beta=0
sd = SoftDropGroomer(zcut=zcut, beta=beta)
print('Soft Drop Groomer: zcut=%.1f, beta=%.1f' % (zcut, beta))

# CS parameters
max_distance = 0.3
alpha = 1
ghost_area = 0.005

print('Constituent Subtraction [max_distance, alpha, ghost_area]: [%.1f, %.1f, %.3f]' % (max_distance, alpha, ghost_area))

# jet clustering with cs
def do_cs_event_wide(full_event, ptmin=100.):
    max_eta = 2.

    # background estimator
    bge = fj.GridMedianBackgroundEstimator(max_eta, 0.5)
    bge.set_particles(full_event)

    rho = bge.rho();
    rhom = bge.rho_m();

    subtractor = cs.ConstituentSubtractor()
    subtractor.set_distance_type(0)
    subtractor.set_max_distance(max_distance)
    subtractor.set_alpha(alpha)
    subtractor.set_ghost_area(ghost_area)
    subtractor.set_max_eta(max_eta)
    subtractor.set_background_estimator(bge)
    subtractor.set_scalar_background_density(rho, rhom)
    subtractor.initialize()

    corrected_event = subtractor.subtract_event(full_event)
    jet_def = fj.JetDefinition(fj.antikt_algorithm, 0.4)
    clust_seq_corr = fj.ClusterSequence(corrected_event, jet_def)
    corrected_jets = clust_seq_corr.inclusive_jets(ptmin)

    return corrected_jets, clust_seq_corr

########################################
#                Running
########################################
from particle import PDGID, Particle

ifn = args.input # input file path and name readed from the arguments: "HiForestMiniAOD_PythiaHydjet2018_1.root"--Dijet events simulation with bkg. 
ifs = TFile(ifn, 'READ')
itr = ifs.Get('HiGenParticleAna/hi') # Particle tree in generator level. 
itr.AddFriend("hiEvtAnalyzer/HiTree","") # Centrality information, event weight information

# jet recluster
jr = JetFinder(algorithm=fj.cambridge_algorithm, R=999., ptmin=0)

def delta_phi(phi1, phi2):
    pi = 3.1415926
    dphi = phi1 - phi2
    if dphi > pi:
        dphi -= 2*pi
    if dphi < -pi:
        dphi += 2*pi
    return dphi

def delta_eta(eta1, eta2):
    deta = eta1 - eta2
    return deta

nevent = 0

try:
    nevent_max = int(args.n)
except:
    nevent_max = 100


idx=0
nevent = 0
weight_sum = 0

for entry in itr:
    if nevent == 2000:
        break
    if entry.hiBin > 20: continue # Centrality selection: 0-10%
    event[0] = nevent
    try:
        weight[0] = entry.weight
    except:
        weight[0] = 1
    res = []
    for i in range(len(entry.matchingID)):
        if (Particle.from_pdgid(entry.pdg[i]).mass) is None: continue # some particles, like tau, does not have mass info. 
        p=Particle.from_pdgid(entry.pdg[i]) # get the particle information with PDG package. 
        constituent1 = TLorentzVector()
        constituent1.SetPtEtaPhiM(entry.pt[i], entry.eta[i], entry.phi[i], p.mass/1000) # four-vector conversion: (pt, eta, phi, m)->(px,py,pz,E)
        temp = fj.PseudoJet(constituent1.Px(), constituent1.Py(),constituent1.Pz(), constituent1.E()) # build the PseudoJet object for each particle
        temp.set_user_index(int(entry.pdg[i]))
        res.append(temp) # particles in one event are stored as [[px,py,pz,E], [px,py,pz,E], ...]
        
    full_event = cs.PseudoJetVec()
    full_event.clear()
    for p in res:
        full_event.push_back(p)
    
    # cuts
    ptmin = 100
    ptmin_cs = 100
    jet_eta_cut = 2.

    # Jet clustering from full events
    corrected_jets, clust_seq_corr = do_cs_event_wide(full_event, ptmin)
    
    for jet in corrected_jets:
        if abs(jet.eta())>jet_eta_cut:
            continue

        constituents = [i for i in jet.constituents()] # find the constituents inside the jets

        cn[0] = len(constituents)
        for i in range(cn[0]):
            cdeta[i] = delta_eta(constituents[i].eta(), jet.eta())
            cdphi[i] = delta_phi(constituents[i].phi(), jet.phi())
            cpt[i] = constituents[i].pt()
            cpid[i] = constituents[i].user_index()

        if not constituents:
            continue
        rjets = jr(constituents) # reference line 167: jet recluster
        rjet = rjets[0]

        x[0] = 0
        y[0] = 0

        depth[0] = 0

        jtr = JetTree(rjet) 

        eta[0] = jtr.pseudojet().eta()
        phi[0] = jtr.pseudojet().phi()
        jetpt[0] = jtr.pseudojet().pt()
        jetm[0] = jtr.pseudojet().m()

        temp = jtr
        temp.groom(groomer=sd) # grooming method
        jetmg[0] = temp.pseudojet().m()
        while temp.has_structure():
            z[depth[0]] = temp.z()
            delta[depth[0]] = temp.delta()
            kperp[depth[0]] = temp.kperp()
            m[depth[0]] = temp.m()
            depth[0] += 1
            temp = temp.harder()
        
        trcse.Fill()
    nevent += 1
    #if nevent == 40: break
    if nevent % 100 == 0:
        print('%d events completed!' % nevent)
output.Write()
output.Close()
