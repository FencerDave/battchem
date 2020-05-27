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
E["HMnO2"] = {1:{"V0":3.650, "1/Z":1.0, "Q":155.},
              2:{"V0":3.728, "1/Z":0.2, "Q":020.}, #Research Needed. This is ROUGH EST from Ref(2)
              3:{"V0":3.878, "1/Z":2.0, "Q":100.}}

""" ANODES """          #All V refer to Li/Li+ Reference in 1Molar solutions

E["GRA_Li"] ={1:{"V0":0.050, "1/Z":0.1, "Q":186.},  #LiC12-->LiC6
              2:{"V0":0.090, "1/Z":1.0, "Q":62.},   #LiC18-->LiC12
              3:{"V0":0.25,  "1/Z":2.0, "Q":62.},   #LiC36-->LiC18
              4:{"V0":0.30,  "1/Z":0.5, "Q":31.}}   #C    -->LiC36
E["NTP"]    = 0 # Proprietary? Consult Tom.
E["TPO"]    = 0 # Research Needed
E["Zn_M"]    = {1:{"V0":2.278, "1/Z":0.1, "Q":819.}}   # Zinc Metal
E["Li_M"]    = {1:{"V0":0.005, "1/Z":0.1, "Q":3862.}}  # Lithium Metal
E["Pb_M"]    = {1:{"V0":2.460, "1/Z":0.1, "Q":259.}}   # Lead Metal


""" Reference Electrodes """          #All V refer to Li/Li+ in 1Molar solutions
#COMMON KNOWN REFERENCES
Refs=dict()
Refs["Li"]   = 0.00      #Lithium Baseline Reference. (Li+ -> Li in 1M LiPF6 Organic E'lyte)
Refs["Zn"]   = 2.278     # Zinc metal electrode
Refs["Pb"]   = 2.460     # Lead metal electrode

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
def Show_Curves(Data, AC, plotting=0): #"Data" is Dictionary of Curve info. "AC" is +1 for Cathode, -1 for Anode.
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

    if plotting==1:
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


def combine_curves(Ano, anode_m, Cat, cathode_m, SOC_mAh=-100):
    """
    Here we'll combine the curves to get the full Nernst voltage'

    QV Curves are in units of mAh/g (also A*hrs per kg),
        so units can be entered in g or kg, and will simply have
        the appropriate scale of units.
        (For Calculations, We assume mAh and g units)
    """
    Ano_QV = [Ano[0]*anode_m, Ano[1]]    # mAh/g*g, Volts
    Cat_QV = [Cat[0]*cathode_m, Cat[1]]  # mAh/g*g, Volts

    # Adjust SOC values based on mAh imbalance.
    # POSITIVE SOC shift means Cathode is Over-Charged
    #   (Corresponding to Subtracting Cathode Q on this plot)
    if SOC_mAh > 0:
        Cat_QV[0] += (-abs(SOC_mAh))
    else:
        Ano_QV[0] += (-abs(SOC_mAh))

    Qmax = min(max(Cat_QV[0]), max(Ano_QV[0]))
    Q_range = np.linspace(0, Qmax, 1000)
    V_range = Q_range*0
    print(Qmax)
    cat_loc = 0
    ano_loc = 0
    Cell_QV = []
    for i, Q in enumerate(Q_range):
        # for a given Q, Loop through both electrodes to find their
        #   voltage at that Q
        while Cat_QV[0][cat_loc] < Q and cat_loc < len(Cat_QV[0]):
            cat_loc += 1
        else:
            cat_v = Cat_QV[1][cat_loc]

        while Ano_QV[0][ano_loc] < Q and ano_loc < len(Ano_QV[0]):
            ano_loc += 1
        else:
            ano_v = Ano_QV[1][ano_loc]

        V_range[i] = cat_v - ano_v

    Cell_QV = [Q_range, V_range]
    return Ano_QV, Cat_QV, Cell_QV

def OCV_Build(Ano_Chem, Cat_Chem, Ref="SHE",
              anode_m=1, cathode_m=1, SOC_mAh=0,
              fig=None, ax=None, plot=True):
    '''
    Full wrapper to generate OCV curves for half cells and full cells

    '''
    Ano, Cat = Choose_Electrodes(Ano_Chem, Cat_Chem, Ref)
    PlotQ = 0
    Cat_mAhg = Show_Curves(Cat, 1)
    Ano_mAhg = Show_Curves(Ano, -1)
    Ano_QV, Cat_QV, Cell_QV = combine_curves(
        Ano_mAhg, anode_m, Cat_mAhg, cathode_m, SOC_mAh)

    if plot and not ax:
        fig, ax = plt.subplots()
    else:
        pass

    if plot:
        y_range = _yrange(0.001,0.99,Cell_QV)
        ax.plot(Cell_QV[0],Cell_QV[1])
        ax.set_ylim(y_range)
    else:
        pass

    return Ano_QV, Cat_QV, Cell_QV, ax

def _yrange(minQ, maxQ, Cell_QV):
    Q_01 = minQ * max(Cell_QV[0])
    Q_99 = maxQ * max(Cell_QV[0])
    y_range = [None,None]
    for i in range(len(Cell_QV[0])):
        if Cell_QV[0][i] > Q_01 and not y_range[0]:
            y_range[0] = Cell_QV[1][i]
        elif Cell_QV[0][i] > Q_99 and not y_range[1]:
            y_range[1] = Cell_QV[1][i]
        else:
            pass

    if not y_range[0] or not y_range[1]:
        raise AssertionError("Y Range Not Found")

    return y_range

def CC_Cycle_RZ(Cell_QV, R=0.5, Z_Ch=1, Z_Dc=1,
                I_Ch=1, I_Dc=1, Dc_flip=True):
    """
    Quick-Estimate of Constant-Current Cycling curves
    Using "Rough" Empirical Parameters:

        "R"     : Overall "Ohmic" R baseline (not function of SOC)

        "Z_Ch"  : Charge Exponential parameter

        "Z_Dc"  : Discharge Exponential parameter

    Calculation of Impedance:
        R
    """


R=0.5
Z_Ch=0.5
Z_Dc=0.5

Cell_Q=np.linspace(0,100,1000)
Ch_R = Cell_Q*0
Dc_R = Cell_Q*0
Qmax = max(Cell_Q)

for i in range(len(Cell_Q)):
    Ch_R[i] = R * (1 + Z_Ch*np.exp((Cell_Q[i]/Qmax)))
    Dc_R[i] = R * (1 + Z_Dc*np.exp((1-Cell_Q[i]/Qmax)))

fig, ax = plt.subplots()
ax.plot(Cell_Q,Ch_R)
ax.plot(Cell_Q,Dc_R)


test = 0
if test == 1:
    # Testing Cell with Graphite and LCO default electrodes, vs Li+
    PlotQ = 0  # 1 to plot data, 0 to skip
    fig, ax = plt.subplots()
    A, C, Cell, ax = OCV_Build("Zn_M", "HMnO2", "Zn",
                               1, 1, 0, ax=ax)
else:
    pass


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
#Ref_SCE  = 0         # Saturated Calomel Electrode (Hg+ -> Hg in Saturated KCL Solution )
#Ref_NCE  = 0.0389    # NORMAL Calomel Electrode    (Hg+ -> Hg in 1 MOLAR   KCL Solution )
#Ref_AgCl =-0.045     # Silver Chloride Electrode   (Ag+ -> Ag in Saturated AgCl Aqueous Solution)
#Ref_MSE  = 0.410     # Mercurous Sulfate           (Hg+ -> Hg in Saturated K2SO4)
#Ref_SHE  =-0.242     # Standard Hydrogen Electrode (2H+ -> H2 in Nernst "A=1" (1.13M HCL, 1.02M HF?)
#Ref_NHE  =-0.242     # NORMAL Hydrogen Electrode   (2H+ -> H2 in 1 Molar HCL. Essentially the SAME thing.)
#Ref_AgSO = 0.440     # Silver Sulfate Electrode    (Ag+ -> Ag in 1 Molar AgSO4 Aqueous Solution)
#Ref_Li   =-3.282     # Lithium Baseline Reference. (Li+ -> Li in 1M LiPF6 Organic E'lyte)

# Metals REF vs SHE (See Wikipedia Data page)
#Ref_Pb   =-0.580   # Lead in 1N Sulfuric acid?
#Ref_Zn   =-0.762   # Zinc in 1M ZnSO4
#Ref_Li   =-3.040   # Lithium baseline (agrees with SCE Data)