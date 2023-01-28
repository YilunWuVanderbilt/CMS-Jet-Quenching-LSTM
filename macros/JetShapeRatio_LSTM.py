from ROOT import TFile,TH1F,TH2F,TCanvas,gPad,TLatex,TLegend,TPad,TLine,THStack,TGraph
from ROOT import TColor
from math import sqrt,log
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt

mult = 7000

# input files
f1 = TFile('vac_particles_mse_mult7000.root', "READ") #Your pp jets
f2 = TFile('jewel_particles_mult7000.root', "READ") #Your PbPb jets

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

# pythia
tr = f1.Get('jet')
max = tr.GetEntriesFast()
idx=0
weight_sum = 0
weight_pythia = []
while idx<max:
    tr.GetEntry(idx)
    if tr.depth==0 or tr.jetpt<jetpt_min or tr.jetpt>jetpt_max or tr.delta[0]<0.1:
        idx += 1
        continue

    weight_sum += tr.weight

    x.append(0)
    y.append(tr.lstm)
    weight_pythia.append(tr.weight)
    idx+=1

for w in weight_pythia:
    weight.append(w/weight_sum)


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
# get jet momentum profile from top 40% PbPb jets & botttom 60% PbPb jets
######################################################################################################

count = 0
count_1 = 0
count_2 = 0
pt_charge_1 = np.zeros(16, dtype=float)
pt_charge_2 = np.zeros(16, dtype=float)

tr = f2.Get('jet')
for entry in tr:
    if entry.depth==0 or entry.jetpt<jetpt_min or entry.jetpt>jetpt_max  or entry.delta[0]<0.1:
        continue
    if tr.lstm>threshold:
        count_1 = count_1 + 1
        for i in range(tr.cn):
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.05 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.: 
                pt_charge_1[0] = pt_charge_1[0] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.1 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.05: 
                pt_charge_1[1] = pt_charge_1[1] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.15 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.1: 
                pt_charge_1[2] = pt_charge_1[2] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.2 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.15: 
                pt_charge_1[3] = pt_charge_1[3] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.25 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.2: 
                pt_charge_1[4] = pt_charge_1[4] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.3 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.25: 
                pt_charge_1[5] = pt_charge_1[5] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.35 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.3: 
                pt_charge_1[6] = pt_charge_1[6] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.4 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.35: 
                pt_charge_1[7] = pt_charge_1[7] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.45 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.4: 
                pt_charge_1[8] = pt_charge_1[8] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.5 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.45: 
                pt_charge_1[9] = pt_charge_1[9] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.55 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.5: 
                pt_charge_1[10] = pt_charge_1[10] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.6 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.55: 
                pt_charge_1[11] = pt_charge_1[11] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.65 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.6: 
                pt_charge_1[12] = pt_charge_1[12] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.7 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.65: 
                pt_charge_1[13] = pt_charge_1[13] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.75 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.7: 
                pt_charge_1[14] = pt_charge_1[14] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.8 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.75: 
                pt_charge_1[15] = pt_charge_1[15] + entry.cpt[i]
    else:
        count_2 = count_2 + 1
        for i in range(tr.cn):
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.05 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.: 
                pt_charge_2[0] = pt_charge_2[0] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.1 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.05: 
                pt_charge_2[1] = pt_charge_2[1] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.15 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.1: 
                pt_charge_2[2] = pt_charge_2[2] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.2 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.15: 
                pt_charge_2[3] = pt_charge_2[3] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.25 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.2: 
                pt_charge_2[4] = pt_charge_2[4] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.3 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.25: 
                pt_charge_2[5] = pt_charge_2[5] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.35 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.3: 
                pt_charge_2[6] = pt_charge_2[6] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.4 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.35: 
                pt_charge_2[7] = pt_charge_2[7] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.45 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.4: 
                pt_charge_2[8] = pt_charge_2[8] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.5 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.45: 
                pt_charge_2[9] = pt_charge_2[9] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.55 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.5: 
                pt_charge_2[10] = pt_charge_2[10] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.6 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.55: 
                pt_charge_2[11] = pt_charge_2[11] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.65 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.6: 
                pt_charge_2[12] = pt_charge_2[12] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.7 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.65: 
                pt_charge_2[13] = pt_charge_2[13] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.75 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.7: 
                pt_charge_2[14] = pt_charge_2[14] + entry.cpt[i]
            if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.8 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.75: 
                pt_charge_2[15] = pt_charge_2[15] + entry.cpt[i]
    count = count + 1

jet_shape_PbPb_1 = TH1D("jet_shape_PbPb_1", "jet_shape_PbPb_1", len(pt_charge_1), 0, 0.8);
jet_shape_PbPb_1.SetStats(False)
for i in range(len(pt_charge_1)):
    jet_shape_PbPb_1.SetBinContent(i+1,pt_charge_1[i]/count_1/0.05)
    #jet_shape_PbPb_1.SetBinError(i, sqrt(1/count_1))
    
c1 = TCanvas("c1", "c1", 700, 800)
c1.cd()
jet_shape_PbPb_1.Draw()
c1.Draw()

jet_shape_PbPb_2 = TH1D("jet_shape_PbPb_2", "jet_shape_PbPb_2", len(pt_charge_2), 0, 0.8);
jet_shape_PbPb_2.SetStats(False)
for i in range(len(pt_charge_2)):
    jet_shape_PbPb_2.SetBinContent(i+1,pt_charge_2[i]/count_2/0.05)
    #jet_shape_PbPb_1.SetBinError(i, sqrt(1/count_2))
    
c1 = TCanvas("c1", "c1", 700, 800)
c1.cd()
jet_shape_PbPb_2.Draw()
c1.Draw()

######################################################################################################
# Get jet momentum profile from pp jets
######################################################################################################

pt_charge_pp = np.zeros(16, dtype=float)
count_pp = 0

tr = f1.Get('jet')
for entry in tr:
    if entry.depth==0 or entry.jetpt<jetpt_min or entry.jetpt>jetpt_max  or entry.delta[0]<0.1:
        continue
    for i in range(tr.cn):
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.05 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.: 
            pt_charge_pp[0] = pt_charge_pp[0] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.1 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.05: 
            pt_charge_pp[1] = pt_charge_pp[1] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.15 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.1: 
            pt_charge_pp[2] = pt_charge_pp[2] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.2 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.15: 
            pt_charge_pp[3] = pt_charge_pp[3] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.25 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.2: 
            pt_charge_pp[4] = pt_charge_pp[4] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.3 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.25: 
            pt_charge_pp[5] = pt_charge_pp[5] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.35 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.3: 
            pt_charge_pp[6] = pt_charge_pp[6] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.4 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.35: 
            pt_charge_pp[7] = pt_charge_pp[7] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.45 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.4: 
            pt_charge_pp[8] = pt_charge_pp[8] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.5 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.45: 
            pt_charge_pp[9] = pt_charge_pp[9] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.55 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.5: 
            pt_charge_pp[10] = pt_charge_pp[10] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.6 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.55: 
            pt_charge_pp[11] = pt_charge_pp[11] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.65 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.6: 
            pt_charge_pp[12] = pt_charge_pp[12] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.7 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.65: 
            pt_charge_pp[13] = pt_charge_pp[13] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.75 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.7: 
            pt_charge_pp[14] = pt_charge_pp[14] + entry.cpt[i]
        if (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))<0.8 and (sqrt((entry.cdeta[i])**2+(entry.cdphi[i])**2))>0.75: 
            pt_charge_pp[15] = pt_charge_pp[15] + entry.cpt[i]
    count_pp = count_pp + 1

jet_shape_pp = TH1D("jet_shape_pp", "jet_shape_pp", len(pt_charge_pp), 0, 0.8);
jet_shape_pp.SetStats(False)
for i in range(len(pt_charge_pp)):
    jet_shape_pp.SetBinContent(i+1,pt_charge_pp[i]/count_pp/0.05)
    #jet_shape_PbPb_1.SetBinError(i, sqrt(1/count_pp))

c1 = TCanvas("c1", "c1", 700, 800)
c1.cd()
jet_shape_pp.Draw()
c1.Draw()

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

######################################################################################################
# Get the jet shape ratio (or jet momentum profile ratio, samething here) of PbPb to pp
######################################################################################################

PbPb_to_pp_ratio = jet_shape_PbPb_1.Clone()
PbPb_to_pp_ratio.Divide(jet_shape_pp)

PbPb_to_pp_ratio_2 = jet_shape_PbPb_2.Clone()
PbPb_to_pp_ratio_2.Divide(jet_shape_pp)

for i in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]:
    PbPb_to_pp_ratio.SetBinError(i, sqrt(1/count_1))
    PbPb_to_pp_ratio_2.SetBinError(i, sqrt(1/count_2))
    
SetMarkerStyle(PbPb_to_pp_ratio, 20, ci, 1, 1.3)
SetLineStyle(PbPb_to_pp_ratio, 1, ci, 1, 1)

SetMarkerStyle(PbPb_to_pp_ratio_2, 20, 9, 1, 1.3)
SetLineStyle(PbPb_to_pp_ratio_2, 1, 9, 1, 1)

c1 = TCanvas("c1", "c1", 800, 800)
c1.cd()
gPad.SetLeftMargin(0.12)
gPad.SetRightMargin(0.12)
gPad.SetBottomMargin(0.12)
gPad.SetTopMargin(0.02)

title = ";\Delta r;P(\Delta r)_{PbPb}/P(\Delta r)_{pp}"
frame1 = DrawFrame(0, 0.4, 0, 4.8, title, False)
style_frame(frame1)
frame1.GetXaxis().SetTitleSize(39)

Tl = TLatex()
s1 = "Centrality 0-10%"
s2 = "anti-k_{T} R = 0.4, p_{T,jet}#in [%.0f,%.0f] GeV" % (jetpt_min, jetpt_max)

Tl.SetNDC()
Tl.SetTextFont(43)
Tl.SetTextSize(25)
Tl.DrawLatex(0.15,0.82, s1)
Tl.DrawLatex(0.15,0.76, s2)
Tl.DrawLatex(0.15,0.695, s3)

lg = TLegend(0.5, 0.83, 0.7, 0.95)
lg.AddEntry(PbPb_to_pp_ratio, "Jewel (Top 40%)/ Jewel-vac", "lep")
lg.AddEntry(PbPb_to_pp_ratio_2, "Jewel (Bot 60%)/ Jewel-vac", "lep")
lg.SetBorderSize(0)
lg.SetTextSize(0.03)
lg.Draw("same")

PbPb_to_pp_ratio.Draw("same")
PbPb_to_pp_ratio_2.Draw("same")

c1.Draw()
