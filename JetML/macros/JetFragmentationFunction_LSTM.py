from ROOT import TFile,TH1F,TH2F,TCanvas,gPad,TLatex,TLegend,TPad,TLine,THStack,TGraph,TH1D
from ROOT import TColor
from math import sqrt,log
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt

mult = 7000

# input files
f1 = TFile('vac_particles_mse_mult7000.root', "READ")
f2 = TFile('jewel_particles_mult7000.root', "READ")

# jet pt cut
jetpt_min = 200
jetpt_max = 400

# plot utils
from ROOT import gPad

def DrawFrame(xmin, xmax, ymin, ymax, Title, setMargins):

    if setMargins:
      gPad.SetLeftMargin(0.2)
      gPad.SetRightMargin(0.05)
      gPad.SetBottomMargin(0.1)
      gPad.SetTopMargin(0.05)

    frame = gPad.DrawFrame(xmin,ymin,xmax,ymax)
    frame.SetTitle(Title)
    frame.GetXaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetLabelSize(0.04)
    frame.GetXaxis().SetTitleSize(0.06)
    frame.GetYaxis().SetTitleSize(0.06)
    frame.GetXaxis().SetTitleOffset(0.8)
    frame.GetYaxis().SetTitleOffset(1.3)
    frame.GetXaxis().CenterTitle()
    frame.GetYaxis().CenterTitle()
    gPad.SetTicks(1,1)
    return frame

def SetMarkerStyle(hist, style, color, alpha, size):
    hist.SetMarkerStyle(style)
    hist.SetMarkerColorAlpha(color, alpha)
    hist.SetMarkerSize(size)

def SetLineStyle(hist, style, color, alpha, width):
    hist.SetLineStyle(style)
    hist.SetLineColorAlpha(color, alpha)
    hist.SetLineWidth(width)

def SetFillStyle(hist, style, color, alpha):
    hist.SetFillStyle(style)
    hist.SetFillColorAlpha(color, alpha)

######################################################################################################
# roc curve & selecting thresholds based on different quenching levels
######################################################################################################

x = []
y = []
weight = []

# pp jets
tr = f1.Get('jet')
max = tr.GetEntriesFast()
idx=0
weight_sum = 0
weight_pythia = [] #name is pythia but actually is jewel vacuum
while idx<max:
    tr.GetEntry(idx)
    if tr.depth==0 or tr.jetpt<jetpt_min or tr.jetpt>jetpt_max or tr.delta[0]<0.1:
        idx += 1
        continue

    weight_sum += tr.weight

    x.append(0)
    y.append(tr.lstm)
    weight_pythia.append(tr.weight) #name is pythia but actually is jewel vacuum
    idx+=1

for w in weight_pythia:
    weight.append(w/weight_sum)

#PbPb jets
tr = f2.Get('jet')
max = tr.GetEntriesFast()
idx=0
weight_sum = 0
weight_jewel = []
while idx<max:
    tr.GetEntry(idx)
    if tr.depth==0 or tr.jetpt<jetpt_min or tr.jetpt>jetpt_max or tr.delta[0]<0.1:
        idx += 1
        continue

    weight_sum += tr.weight

    x.append(1)
    y.append(tr.lstm)
    weight_jewel.append(tr.weight)
    idx+=1

for w in weight_jewel:
    weight.append(w/weight_sum)


fpr, tpr, thresholds = metrics.roc_curve(x, y, sample_weight=weight, pos_label=1)

# threshold with tpr=0.4
fpr_select = 0
tpr_select = 0
threshold = 0
d_max = 1


for i in range(len(thresholds)):
    d = pow(0.4-tpr[i], 2)
    if d<d_max:
        d_max = d
        fpr_select = fpr[i]
        tpr_select = tpr[i]
        threshold = thresholds[i]

print("TPR: %0.2f, FPR: %0.2f, Threshold: %0.4f" % (tpr_select, fpr_select, threshold))

auc = metrics.roc_auc_score(x, y,sample_weight=weight)

plt.figure()
lw = 2
plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
plt.plot(fpr, tpr, color="darkorange", lw=lw, label="ROC Curve (AUC=%0.3f)" % auc)
plt.plot([fpr_select], [tpr_select], 'ro', label=r"TPR=%0.2f, FPR=%0.2f" % (tpr_select, fpr_select))

plt.xlim([-0.05, 1.05])
plt.ylim([-0.15, 1.05])
plt.xlabel("False Positive Rate (FPR)", fontsize=30)
plt.ylabel("True Positive Rate (TPR)", fontsize=30)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
# plt.title("Receiver Operating Characteristic (ROC)", fontsize=18)
plt.legend(loc="lower right", fontsize=26)

plt.subplots_adjust(left=0.16, right=0.98, top=0.98, bottom=0.16)
plt.gcf().set_size_inches(8, 6)
plt.savefig("roc.pdf")

######################################################################################################
# Calculation of the jet fragmentation function
######################################################################################################

def constituent_phi(phi1, phi2):
    pi = 3.1415926
    cphi = phi1 + phi2
    if cphi > pi:
        cphi -= 2*pi
    if cphi < -pi:
        cphi += 2*pi
    return cphi

def magnitude(vector):
    return sqrt(sum(pow(element, 2) for element in vector))
  
from math import cos, sin, tan, exp

#pp jets from jewel vaccum

tr = f1.Get('jet')
cpx_pp=0
cpy_pp=0
cpz_pp=0
a_pp=[0,0,0]
b_pp=[0,0,0]
z_pp=[]
count_pp=0

for entry in tr:
    if entry.depth==0 or entry.jetpt<jetpt_min or entry.jetpt>jetpt_max or entry.delta[0]<0.1: #or abs(entry.eta)<0.3:
        continue
    count_pp = count_pp + 1
    b_pp = np.array([entry.jetpt*cos(entry.phi),entry.jetpt*sin(entry.phi),entry.jetpt/(2*exp(entry.eta)/(1-exp(entry.eta)**2))])
    for i in range(tr.cn):
        if entry.cpt[i] < 1: 
            continue
        cpx_pp=entry.cpt[i]*cos(constituent_phi(entry.cdphi[i],entry.phi))
        cpy_pp=entry.cpt[i]*sin(constituent_phi(entry.cdphi[i],entry.phi))
        cpz_pp=entry.cpt[i]/(2*exp(entry.cdeta[i]+entry.eta)/(1-exp(entry.cdeta[i]+entry.eta)**2))
        a_pp = np.array([cpx_pp,cpy_pp,cpz_pp])
        z_pp.append(abs(np.dot(a_pp,b_pp))/((magnitude(b_pp))**2))
#Plot the pp jet fragmentation function

jet_fragmentation = TH1D("jet_fragmentation", "jet_fragmentation", 10, 0, 5);

for i in range(len(z_pp)):
    jet_fragmentation.Fill(log(1./z_pp[i]))

jet_fragmentation.Scale(1./count_pp)
c1 = TCanvas("c1", "c1", 700, 800)
c1.cd()
c1.SetLogy()
jet_fragmentation.Draw()
c1.Draw()

#PbPb Jets from Jewel medium

tr = f2.Get('jet')

cpx_PbPb_1=0
cpy_PbPb_1=0
cpz_PbPb_1=0
a_PbPb_1=[0,0,0]
b_PbPb_1=[0,0,0]
z_PbPb_1=[]
count_PbPb_1=0

cpx_PbPb_2=0
cpy_PbPb_2=0
cpz_PbPb_2=0
a_PbPb_2=[0,0,0]
b_PbPb_2=[0,0,0]
z_PbPb_2=[]
count_PbPb_2=0

for entry in tr:
    if entry.depth==0 or entry.jetpt<jetpt_min or entry.jetpt>jetpt_max or entry.delta[0]<0.1:# or abs(entry.eta)<0.3:
        continue
    if tr.lstm>threshold: #Top 40% PbPb jets
        count_PbPb_1 = count_PbPb_1 + 1
        b_PbPb_1 = np.array([entry.jetpt*cos(entry.phi),entry.jetpt*sin(entry.phi),entry.jetpt/(2*exp(entry.eta)/(1-exp(entry.eta)**2))])
        for i in range(tr.cn):
            if entry.cpt[i] < 1: 
                continue
            cpx_PbPb_1=entry.cpt[i]*cos(constituent_phi(entry.cdphi[i],entry.phi))
            cpy_PbPb_1=entry.cpt[i]*sin(constituent_phi(entry.cdphi[i],entry.phi))
            cpz_PbPb_1=entry.cpt[i]/(2*exp(entry.cdeta[i]+entry.eta)/(1-exp(entry.cdeta[i]+entry.eta)**2))
            a_PbPb_1 = np.array([cpx_PbPb_1,cpy_PbPb_1,cpz_PbPb_1])
            z_PbPb_1.append(abs(np.dot(a_PbPb_1,b_PbPb_1))/((magnitude(b_PbPb_1))**2))
    
    else: #Bottom 60% PbPb jets
        count_PbPb_2 = count_PbPb_2 + 1
        b_PbPb_2 = np.array([entry.jetpt*cos(entry.phi),entry.jetpt*sin(entry.phi),entry.jetpt/(2*exp(entry.eta)/(1-exp(entry.eta)**2))])
        for i in range(tr.cn):
            if entry.cpt[i] < 1: 
                continue
            cpx_PbPb_2=entry.cpt[i]*cos(constituent_phi(entry.cdphi[i],entry.phi))
            cpy_PbPb_2=entry.cpt[i]*sin(constituent_phi(entry.cdphi[i],entry.phi))
            cpz_PbPb_2=entry.cpt[i]/(2*exp(entry.cdeta[i]+entry.eta)/(1-exp(entry.cdeta[i]+entry.eta)**2))
            a_PbPb_2 = np.array([cpx_PbPb_2,cpy_PbPb_2,cpz_PbPb_2])
            z_PbPb_2.append(abs(np.dot(a_PbPb_2,b_PbPb_2))/((magnitude(b_PbPb_2))**2))

# Top 40% PbPb jets

jet_fragmentation_PbPb_a = TH1D("jet_fragmentation_PbPb_a", "jet_fragmentation_PbPb_a", 10, 0, 5);
#jet_shape_PbPb_a_1.SetStats(False)

for i in range(len(z_PbPb_1)):
    jet_fragmentation_PbPb_a.Fill(log(1./z_PbPb_1[i]))
    #jet_shape_PbPb_a_1.SetBinError(i, sqrt(1/count_1))
jet_fragmentation_PbPb_a.Scale(1./count_PbPb_1)

c1 = TCanvas("c1", "c1", 700, 800)
c1.cd()
c1.SetLogy()
jet_fragmentation_PbPb_a.Draw()
c1.Draw()

# Bottom 60% PbPb jets

jet_fragmentation_PbPb_b = TH1D("jet_fragmentation_PbPb_b", "jet_fragmentation_PbPb_b", 10, 0, 5);
#jet_shape_PbPb_b_1.SetStats(False)

for i in range(len(z_PbPb_2)):
    jet_fragmentation_PbPb_b.Fill(log(1./z_PbPb_2[i]))
    #jet_shape_PbPb_b_1.SetBinError(i, sqrt(1/count_1))
jet_fragmentation_PbPb_b.Scale(1./count_PbPb_2)

c1 = TCanvas("c1", "c1", 700, 800)
c1.cd()
c1.SetLogy()
jet_fragmentation_PbPb_b.Draw()
c1.Draw()

######################################################################################################
# Fragmetation function ratio of PbPb to pp splitting into two classes: 40% vs 60% PbPb jets
######################################################################################################
PbPb_to_pp_ratio_a = jet_fragmentation_PbPb_a.Clone()
PbPb_to_pp_ratio_a.Divide(jet_fragmentation)
PbPb_to_pp_ratio_a.SetStats(False)

PbPb_to_pp_ratio_b = jet_fragmentation_PbPb_b.Clone()
PbPb_to_pp_ratio_b.Divide(jet_fragmentation)
PbPb_to_pp_ratio_b.SetStats(False)

def style_frame(frame):
    frame.GetYaxis().SetLabelFont(43)
    frame.GetYaxis().SetTitleFont(43)
    frame.GetYaxis().SetLabelSize(28)
    frame.GetYaxis().SetTitleSize(28)
    frame.GetYaxis().SetTitleOffset(1.5)
    frame.GetYaxis().SetNdivisions(505)
    
    frame.GetXaxis().SetLabelFont(43)
    frame.GetXaxis().SetTitleFont(43)
    frame.GetXaxis().SetLabelSize(28)
    frame.GetXaxis().SetTitleSize(40)
    frame.GetXaxis().SetTitleOffset(1.0)
    frame.GetXaxis().SetNdivisions(505)

ci = TColor.GetFreeColorIndex()
color = TColor(ci, 1.,0.4,0.4,"",1.)

SetMarkerStyle(PbPb_to_pp_ratio_a, 20, ci, 1, 1.3)
SetLineStyle(PbPb_to_pp_ratio_a, 1, ci, 1, 1)

SetMarkerStyle(PbPb_to_pp_ratio_b, 20, 9, 1, 1.3)
SetLineStyle(PbPb_to_pp_ratio_b, 1, 9, 1, 1)

c1 = TCanvas("c1", "c1", 800, 800)
c1.cd()
gPad.SetLeftMargin(0.12)
gPad.SetRightMargin(0.12)
gPad.SetBottomMargin(0.12)
gPad.SetTopMargin(0.02)

title = ";\Xi = ln(1/z);Ratio\,\,of\,\,PbPb/pp\,\,(1/N_{jet}dN_{Track} d \Xi)"
frame1 = DrawFrame(0, 5, 0, 4.2, title, False)
style_frame(frame1)
frame1.GetXaxis().SetTitleSize(39)

Tl = TLatex()
s1 = "Centrality 0-10%"
s2 = "anti-k_{T} R = 0.4, p_{T,jet}#in [%.0f,%.0f] GeV" % (jetpt_min, jetpt_max)
s3 = "p_{T}^{track} > 1GeV/c, Tracks in cone #Delta R < 0.4"
Tl.SetNDC()
Tl.SetTextFont(43)
Tl.SetTextSize(25)
Tl.DrawLatex(0.15,0.82, s1)
Tl.DrawLatex(0.15,0.76, s2)
Tl.DrawLatex(0.15,0.695, s3)

lg = TLegend(0.45, 0.83, 0.7, 0.95)
lg.AddEntry(PbPb_to_pp_ratio_a, "Jewel (Top 40%)/ Jewel-vac", "lep")
lg.AddEntry(PbPb_to_pp_ratio_b, "Jewel (bot 60%)/ Jewel-vac", "lep")
lg.SetBorderSize(0)
lg.SetTextSize(0.03)
lg.Draw("same")

PbPb_to_pp_ratio_a.Draw("same")
PbPb_to_pp_ratio_b.Draw("same")

c1.Draw()
