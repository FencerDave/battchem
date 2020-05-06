# -*- coding: utf-8 -*-
"""
Created on Sat May 18 09:49:25 2019
@author: fencerdave

Library reference of Curves to use in the Nernst SOC model.
I hate that you can't draw on functions / libraries that you make further down in a script.
I understand why (to a point), but it's a major annoyance...

"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import copy #Used for copy.deepcopy, to NOT DAMAGE THE RAW LIBRARIES.


""" CATHODES """        #All V refer to Li/Li+ Reference in 1Molar solutions

E=dict() #Dictionary of Electrodes! That's the Pythonic way (I think!) to use Strings as Variables!
E["LFP"]    ={1:{"V0":3.20, "1/Z":0.5, "Q":53.},
              2:{"V0":3.21, "1/Z":0.5, "Q":53.}}                    #NOT REAL. Research Needed. Cite Sources
E["LMO"]    ={1:{"V0":3.99, "1/Z":1.0, "Q":53.},
              2:{"V0":4.15, "1/Z":1.0, "Q":53.}}                    #Fit to Data from Ref(2) (And Personal research)
E["LCO"]    ={1:{"V0":3.91, "1/Z":1.0, "Q":25.},
              2:{"V0":4.10, "1/Z":6.0, "Q":25.}} #Research Needed. This is ROUGH EST from Ref(2)
E["LNO"]    =0 #Research Needed. Cite Sources
E["NCA"]    =0 #Research Needed. Cite Sources
E["NMC111"] =0#Research needed. Can I CREATE this as a mix of LMO, LCO, and LNO??
E["GRA_Br"] =0 #Include from 2019 Army Research?!? And/or Kinoshita on Carbon

""" ANODES """          #All V refer to Li/Li+ Reference in 1Molar solutions

E["GRA_Li"] ={1:{"V0":0.050, "1/Z":0.1, "Q":186.},  #C    -->LiC36 (infinite sub-stages, all smeared together)
              2:{"V0":0.090, "1/Z":1.0, "Q":62.},   #LiC36-->LiC18
              3:{"V0":0.25,  "1/Z":2.0, "Q":62.},   #LiC18-->LiC12
              4:{"V0":0.30,  "1/Z":0.5, "Q":31.}}
              #5:{"V0":1.5,   "1/Z":10., "Q":15.}}   #LiC12-->LiC6     #Fit to Data from Ref(2)
E["NTP"]    = 0 # Proprietary? Consult Tom.
E["TPO"]    = 0 # Research Needed


""" Reference Electrodes """          #All V refer to Li/Li+ in 1Molar solutions
#COMMON KNOWN REFERENCES
Refs=dict()
Refs["Li"]   = 0.00      #Lithium Baseline Reference. (Li+ -> Li in 1M LiPF6 Organic E'lyte)
Refs["SCE"]  = 3.292     #Saturated Calomel Electrode (Hg+ -> Hg in Hg in Saturated KCL Solution )
Refs["NCE"]  = 3.331     #NORMAL Calomel Electrode    (1M KCL)
Refs["AgCl"] = 3.337     #Silver Chloride Electrode   (Ag+ -> Ag in Saturated AgCl Aqueous Solution)
Refs["MSE"]  = 3.702     #Mercurous Sulfate (sat)     (Hg+ -> Hg in Saturated K2SO4)
Refs["SHE"]  = 3.534     #Standard Hydrogen Electrode (2H+ -> H2 in Nernst "A=1" (1.13M HCL, 1.02M HF?)
Refs["NHE"]  = 3.534     #NORMAL Hydrogen Electrode   (2H+ -> H2 in 1 Molar HCL. Essentially the SAME thing.)
Refs["AgSO"] = 3.732     #Silver Sulfate Electrode    (Ag+ -> Ag in 1 Molar AgSO4 Aqueous Solution)



def Choose_Electrodes(Ano,Cat,Ref):

    AData=copy.deepcopy(E[Ano])
    CData=copy.deepcopy(E[Cat])
    RE=copy.deepcopy(Refs[Ref])

    #ADJUST VOLTAGE FOR REFERENCE ELECTRODE (and -Q for Anodes)
    for D in AData:
        AData[D]["V0"]=AData[D]["V0"]-RE    #Adjust V for Ref
        AData[D]["Q"] =-1*abs(AData[D]["Q"])#Anodes use "Negative Q!"
    for D in CData:
        CData[D]["V0"]=CData[D]["V0"]-RE    #Adjust V for Ref
        CData[D]["Q"] =abs(CData[D]["Q"])   #Cathodes use pos Q. Just Check.
    return AData, CData


""" Program copied/modified from SOC Model"""
def Show_Curves(Data,AC): #"Data" is Dictionary of Curve info. "AC" is +1 for Cathode, -1 for Anode.
    Curv = dict()
    for i in Data: # Generate each Electron-Transfer-Reaction step
        Vo = Data[i]["V0"]
        Z = Data[i]["1/Z"] #Fix this later. JUST USE ZZZZ
        Q = Data[i]["Q"]
        vlen = 60000 # How many Voltage steps to examine
        Curv[i] = {"V": np.linspace(-5.*AC,5.*AC,vlen),
                  "Q": np.zeros(vlen)
                  }
        Curv[i]["Q"] = Q / (1+np.exp(-1/(0.02569*Z)*(Curv[i]["V"]-Vo))) #Nernst Equation

        Qtot = np.zeros(vlen)
    for i in Curv:
        Qtot = Qtot + Curv[i]["Q"]
    #For Anode, Qtot is counting towards negative Capacity as V increases!
    #Next Slide it down, so that Qtot [0] is at Zero.
    Qmin = np.min(Qtot)
    Qtot = Qtot - Qmin
    Vtot = Curv[1]["V"]

    V=[0,0]
    VRange=[0,0]
    t=0#set trigger
    q1=(max(Qtot)*0.001)
    q2=(max(Qtot)*0.999)
    for i,q in enumerate(Qtot):                              #Set Voltage Window
        if  q>q1 and t==0:    #find V at Q=0.2%SOC
            t=1#advance trigger
            V[0]=Vtot[i]
        elif q>q2 and t==1:  #find V at Q=99.5%SOC
            t=3#return trigger
            V[1]=Vtot[i]
    VRange[0]=min(V)
    VRange[1]=max(V)

    if PlotQ==1:
        """ PLOT THE DATAS"""
        plt.figure()
        for i in Curv:
            plt.plot(Curv[i]["V"],abs(Curv[i]["Q"]))
            plt.draw()
            axes = plt.gca()
            axes.set_xlim(VRange)
            axes.set_title("Individual Charge Transfers:")
            axes.set_xlabel("Voltage (V)")
            axes.set_ylabel("Charge Transfer Q (mAh/g)")

        plt.figure()
        plt.plot(Qtot, Vtot)
        axes = plt.gca()
        axes.set_ylim(VRange)
        axes.set_title("Half Cell Curve:")
        axes.set_ylabel("Voltage (V)")
        axes.set_xlabel("Half-Cell Q (mAh/g)")
        plt.draw()

    return Qtot, Vtot, VRange

# Testing Cell with Graphite and LCO default electrodes, vs Li+
PlotQ=1 #1 to plot data, 0 to skip
Ano,Cat=Choose_Electrodes("GRA_Li","LCO","Li")
Q,T,VRange=Show_Curves(Cat,1)





""" RESEARCH REFERENCES:"""
#Like a good little scientist, here are a list of places that I got my Data
#(Also to prove I'm not using anything proprietary)
"""
(1) Tables of Common Reference Electrodes (w/ more Refs)
    Constltrsr.net/Resources/ref

(2) Common Li-Ion Cathode Curve Estimates
    Advanced Materials for Lithium-Ion Batteries (2012)
    Textbook by Hariharan, Editor: Springer

(3) Electrochemical Info on Graphite/Lithium
    Kinoshita on Carbon (1988)
    Textbook by Kim Kinoshita, Editor: Wiley

"""
#Note Research Constltrsr.net/Resources/ref: AgCl is -0.045 vs SCE (SCE is +0.242 vs NHE while AgCl is +0.197) (Also. Li is -3.05 vs NHE)
# LIST OF REFS FROM ^, all Vs SCE
#Ref_SCE  = 0         #Saturated Calomel Electrode (Hg+ -> Hg in Saturated KCL Solution )
#Ref_NCE  = 0.0389    #NORMAL Calomel Electrode    (Hg+ -> Hg in 1 MOLAR   KCL Solution )
#Ref_AgCl =-0.045     #Silver Chloride Electrode   (Ag+ -> Ag in Saturated AgCl Aqueous Solution)
#Ref_MSE  = 0.41      #Mercurous Sulfate           (Hg+ -> Hg in Saturated K2SO4)
#Ref_SHE  =-0.242     #Standard Hydrogen Electrode (2H+ -> H2 in Nernst "A=1" (1.13M HCL, 1.02M HF?)
#Ref_NHE  =-0.242     #NORMAL Hydrogen Electrode   (2H+ -> H2 in 1 Molar HCL. Essentially the SAME thing.)
#Ref_AgSO = 0.44      #Silver Sulfate Electrode    (Ag+ -> Ag in 1 Molar AgSO4 Aqueous Solution)
#Ref_Li   =-3.292     #Lithium Baseline Reference. (Li+ -> Li in 1M LiPF6 Organic E'lyte)
