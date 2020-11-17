# -*- coding: utf-8 -*-
print '------> Setting Environment'

import sys
import math
from ROOT import *
import numpy as np
from array import *
from termcolor import colored
from ROOT import gROOT

print '------> Importing Root File'

## Configuration settings
MAX_EVT  = -1 ## Maximum number of events to process
PRT_EVT  = 10000 ## Print every Nth event
printouts=False

## ============== Event branches ================
evt_tree  = TChain('FlatNtupleMC/tree')

## ================ Read input files ======================
dir1 = '/uscms/home/mdecaro/nobackup/BDTGEM/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/'
file_name = dir1+"EMTF_MC_NTuple_Run3stubs.root"
print colored('Loading file: '+file_name, 'green')
evt_tree.Add(file_name)


## ================ Define histograms ======================
h_pt_denom = TH1D('h_pt_denom', '', 80, 1., 80.) ; h_pt_numer = TH1D('h_pt_numer', '', 80, 1., 80.)
h_eta_denom = TH1D('h_eta_denom', '', 128, -3., 3.) ; h_eta_numer = TH1D('h_eta_numer', '', 128, -3., 3.)
h_phi_denom = TH1D('h_phi_denom', '', 64, -180., 180.) ; h_phi_numer = TH1D('h_phi_numer', '', 64, -180., 180.)
h_2D_pt_eta_denom = TH2D('h_2D_pt_eta_denom', '', 128, -3, 3, 80, 1., 80.) ; h_2D_pt_eta_numer = TH2D('h_2D_pt_eta_numer', '', 128, -3, 3, 80, 1., 80.)


## ================ Printouts for debugging ======================
if printouts==True:
  for iEvt in range(100000):
    evt_tree.GetEntry(iEvt)

    if abs(evt_tree.mu_eta[0])<2.4 and abs(evt_tree.mu_eta[0])>2.3:
      if evt_tree.mu_pt[0]<30 and evt_tree.mu_pt[0]>20:
	for i in range(len(evt_tree.mu_pt)):
	  print "Gen muon",i, " pt, eta, phi: ", evt_tree.mu_pt[i], evt_tree.mu_eta[i], evt_tree.mu_phi[i]
	print '--------'
	for i in range(len(evt_tree.trk_pt)):
	  print "L1 muon",i, " pt, eta, phi, quality, nNeighbor: ", evt_tree.trk_pt[i], evt_tree.trk_eta[i], evt_tree.trk_phi[i], evt_tree.trk_qual[i], evt_tree.trk_nNeighbor[i]
	#for i in range(len(evt_tree.hit_phi)):
	  #if evt_tree.hit_station[i]==1: print evt_tree.hit_phi[i], evt_tree.hit_neighbor[i]
	print '------Next event------'


## ================ Event loop ======================
for iEvt in range(1000000):
#for iEvt in range(evt_tree.GetEntries()):
  if MAX_EVT > 0 and iEvt > MAX_EVT: break
  if iEvt % PRT_EVT is 0: print 'Event #', iEvt
  
  evt_tree.GetEntry(iEvt)

  for i in range(len(evt_tree.mu_pt)):
    #Fill histogram denominators
    if abs(evt_tree.mu_eta[i])>1.24 and abs(evt_tree.mu_eta[i])<2.4:
      h_pt_denom.Fill(evt_tree.mu_pt[i]) 
      h_2D_pt_eta_denom.Fill(evt_tree.mu_eta[i], evt_tree.mu_pt[i])

      if evt_tree.mu_pt[i]>20:
	h_eta_denom.Fill(evt_tree.mu_eta[i])
	h_phi_denom.Fill(evt_tree.mu_phi[i])
	

    #Fill histogram numerators by looking for a Level-1 match. (Same endcap as true muon, ignore duplicated L1 muons using nNeighbor==0)
    for j in range(len(evt_tree.trk_pt)):
      if evt_tree.trk_pt[j]>20. and abs(evt_tree.mu_eta[i])>1.24 and abs(evt_tree.mu_eta[i])<2.4 and evt_tree.mu_eta[i]*evt_tree.trk_eta[j]>0 and evt_tree.trk_nNeighbor[j]==0:
	h_pt_numer.Fill(evt_tree.mu_pt[i])
	h_2D_pt_eta_numer.Fill(evt_tree.mu_eta[i], evt_tree.mu_pt[i])

	if evt_tree.mu_pt[i]>20.:
	  h_eta_numer.Fill(evt_tree.mu_eta[i])
	  h_phi_numer.Fill(evt_tree.mu_phi[i])

	
## ================ Plot/save histograms ======================

c1 = TCanvas("c1")
h_2D_pt_eta_numer.Divide(h_2D_pt_eta_denom)
h_2D_pt_eta_numer.Draw("colz")
h_2D_pt_eta_numer.GetZaxis().SetRangeUser(0.,1.0)
h_2D_pt_eta_numer.SetTitle('Trigger efficiency 2D p_{T}^{GEN} vs #eta^{GEN} (p_{T}^{L1} > 20 GeV)')
h_2D_pt_eta_numer.GetXaxis().SetTitle('#eta^{GEN}') ; h_2D_pt_eta_numer.GetYaxis().SetTitle('p_{T}^{GEN}')
raw_input("Enter")
c1.Close()

'''
c1 = TCanvas("c1")
eff = TEfficiency(h_phi_numer, h_phi_denom)
eff.Draw()
eff.SetTitle('EMTF Trigger Efficiency vs #phi^{GEN} (p_{T}^{GEN}, p_{T}^{L1} > 20 GeV) (1.24 < #eta^{GEN} < 2.4) ; #phi^{GEN} ; Trigger Effieicny')
gPad.Update()
graph = eff.GetPaintedGraph()
graph.SetMinimum(0)
graph.SetMaximum(1)
c1.SaveAs('validation_november/eff_phi_pt20_1pt24eta2pt4.png')
raw_input("Enter")

c1 = TCanvas("c1")
eff = TEfficiency(h_pt_numer, h_pt_denom)
eff.Draw()
eff.SetTitle('EMTF Trigger Efficiency vs p_{T}^{GEN} (p_{T}^{L1} > 20 GeV) (1.24 < #eta^{GEN} < 2.4) ; p_{T}^{GEN} ; Trigger Effieicny')
gPad.Update()
graph = eff.GetPaintedGraph()
graph.SetMinimum(0)
graph.SetMaximum(1)
c1.SaveAs('validation_november/eff_pt20_1pt24eta2pt4.png')
raw_input("Enter")


c1 = TCanvas("c1")
eff = TEfficiency(h_eta_numer, h_eta_denom)
eff.Draw()
eff.SetTitle('EMTF Trigger Efficiency vs #eta^{GEN} (p_{T}^{GEN}, p_{T}^{L1} > 20 GeV) ; #eta^{GEN} ; Trigger Effieicny')
gPad.Update()
graph = eff.GetPaintedGraph()
graph.SetMinimum(0)
graph.SetMaximum(1)
c1.SaveAs('validation_november/eff_eta_pt20.png')
raw_input("Enter")
'''