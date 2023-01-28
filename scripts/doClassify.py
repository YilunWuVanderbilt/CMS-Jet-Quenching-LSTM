import torch
import torch.nn as nn
import numpy as np
from array import array
from ROOT import TFile, TTree

from src.JetML.Classifier import *

########################################
#               parsing
########################################
import argparse

parser = argparse.ArgumentParser(description='JetML CML Parser')
parser.add_argument('-i','--input', help='Input file path', required=True)
parser.add_argument('-o','--output',help='Output file path', required=True)
parser.add_argument('-t','--tree',help='Input tree name', required=True)
parser.add_argument('-c',help='Neural Network path', required=True)

args = parser.parse_args()

label = []
if 'pythia' in args.input:
    label = [0, 1]
if 'jewel' in args.input:
    label = [1, 0]

# print values
print('*********Initialization**********')
print('Input file:\t%s' % args.input)
print('Output file:\t%s' % args.output)
print('Input tree:\t%s' % args.tree)
print('Neural Network: \t%s' % args.c)
print('*********************************')

##################################################

ifn = args.input

ifs = TFile(ifn, 'READ')
itr = ifs.Get(args.tree)

jc = Classifier(args.c)

ofn = args.output
ofs = TFile(ofn, 'recreate')

maxn = 100
x = array('f', [0.])
y = array('f', [0.])
eta = array('f', [0.])
phi = array('f', [0.])
weight = array('f', [0.])
jetpt = array('f', [0.])
depth = array('i', [0])
z = array('f', maxn * [0.])
delta = array('f', maxn * [0.])
kperp = array('f', maxn * [0.])
m = array('f', maxn * [0.])
lstm = array('f', [0.])
cn = array('i', [0])
cpt = array('f', 500 * [0.])
cdeta = array('f', 500 * [0.])
cdphi = array('f', 500 * [0.])

otr = TTree('jet', 'lstm' )
otr.Branch('lstm', lstm, 'lstm/F')
otr.Branch('x', x, 'x/F')
otr.Branch('y', y, 'y/F')
otr.Branch('eta', eta, 'eta/F')
otr.Branch('phi', phi, 'phi/F')
otr.Branch('weight', weight, 'weight/F')
otr.Branch('jetpt', jetpt, 'jetpt/F')
otr.Branch('depth', depth, 'depth/I')
otr.Branch('z', z, 'z[depth]/F')
otr.Branch('delta', delta, 'delta[depth]/F')
otr.Branch('kperp', kperp, 'kperp[depth]/F')
otr.Branch('m', m, 'm[depth]/F')
otr.Branch('cn', cn, 'cn/I')  #record the number of constituents within jets
otr.Branch('cpt', cpt, 'cpt[cn]/F') #constituents pt
otr.Branch('cdeta', cdeta, 'cdeta[cn]/F') #relative eta between constituent and jet axis
otr.Branch('cdphi', cdphi, 'cdphi[cn]/F') #relative phi between constituent and jet axis

nevent = 0
loss_sum = 0
weight_sum = 0
for entry in itr:
    lstm[0] = -999

    weight[0] = entry.weight
    jetpt[0] = entry.jetpt
    depth[0] = entry.depth
    cn[0] = entry.cn #record the number of constituents within jets
    eta[0] = entry.eta
    phi[0] = entry.phi
    
    if entry.depth==0 or entry.jetpt<120:
        continue

    for i in range(entry.depth):
        z[i] = entry.z[i]
        delta[i] = entry.delta[i]
        kperp[i] = entry.kperp[i]
        m[i] = entry.m[i]
    
    for i in range(entry.cn): #record constituents information
        cpt[i] = entry.cpt[i]
        cdeta[i] = entry.cdeta[i] 
        cdphi[i] = entry.cdphi[i]
    
    item = []
    for i in range(entry.depth):
        item.append([z[i], delta[i], kperp[i], m[i]])
    lstm[0] = jc(item)[0]

    otr.Fill()
    nevent += 1

    if nevent % 1000 == 0:
        print('No. of Events Completed: {}'.format(nevent))


ofs.Write()
ofs.Close()
