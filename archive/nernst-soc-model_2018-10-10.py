#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 11:01:09 2018
@author: fencerdave

Properly getting into python code, to manually (or at request for future GUI Model) set Parameters
and then generate cell curves. 

I have not been able to solve for multiple curves (double sigmoid function), so we will generate data via miliVolt step changes (large sets).
"""
#Import Global ? Libraries?
from matplotlib import pyplot as plt
#import scipy as sp
import numpy as np
import pandas as pd
import tkinter
import Nernst_Reference as NR
#from ttkSimpleDialog import ttkSimpleDialog as Ask

""" OUTPUTS """
#"PLT", "PNG", "CSV" and what datasets to plot
OUT = {"PLT":0,"PNG":0,"CSV":0} #Types of Output
OUT["FULL"]=1
OUT["HALF"]=0
OUT["QV"]=1
OUT["IC"]=0


#Dataset - for each curve, V0, 1/Z, Q
Cathode = {1: [3.58, 1, 53.], 2:[3.8,1, 53.]} #LMO
LMO={1:{"V0":3.58, "1/Z":1.0, "Q":53.0}, 2:{"V0":3.8, "1/Z":1.0, "Q":53.0}}
Anode = {1:[.09,.1,-186], 2:[.122,.1,-62.], 3:[.14,.1,-62.], 4:[.2,3.,-31.],5:[.3,1.,-31.] }#Graphite-Lithium

Build = {"C/A" : 1.2, "Q":56, "Offset":-10}     # These will be the INITIAL Build Parameters
if Build["C/A"]>=1.0:                           # The built Anode and Cathode Q can Change/Fade
    Build["Qa"] = Build["Q"]
    Build["Qc"] = Build["Q"] * Build["C/A"]
else:
    Build["Qa"] = Build["Q"] / Build["C/A"]
    Build["Qc"] = Build["Q"]

# Write Program to generate a nernst curve dataset from a set of input Parameters
"""
def Nernst(Steps):
    #for now, use Vars as a number of steps to execute. Eventually will hard-code or allow to change
    root = tkinter.Tk()
    root.withdraw()
    V = np.zeros(Steps)
    z = np.zeros(Steps)
    Q = np.zeros(Steps)
    for i in range(Steps):
        V[i] = Ask.askfloat('Voltage','V'+str(i))
        z[i] = Ask.askfloat('Flatness','Z'+str(i))
        Q[i]=  Ask.askfloat('Capacity','Q'+str(i))
"""

def Curves(Data):
    i=0
    Curv = dict()
    for i in Data: # Generate each Electron-Transfer-Reaction step
        Vo = Data[i][0]
        Z = Data[i][1]
        Q = Data[i][2]
        vlen = 60000 # How many Voltage steps to examine
        Curv[i] = {"V": np.linspace(-1.,5.,vlen),
                  "Q": np.zeros(vlen)
                  }
        Curv[i]["Q"] = Q / (1+np.exp(-1/(0.02569*Z)*(Curv[i]["V"]-Vo))) #Nernst Equation
        
        Qtot = np.zeros(vlen)
    for i in Curv:
        Qtot = Qtot + Curv[i]["Q"]
    #For Anode, Qtot is counting towards negative Capacity as V increases!
    #Slide it down, so that Qtot [0] is at Zero
    Qmin = np.min(Qtot)
    Qtot = Qtot - Qmin
    Vtot = Curv[1]["V"]
    '''
    Qreturn = np.linspace(0., np.max(Qtot), int(np.max(Qtot)*10)-1) #Lookup Q->V in 0.1mAh increments
    Vreturn = np.zeros(len(Qreturn))
    if Qmin <= -10: #If Anode
        for i, q in enumerate(Qreturn):
            for I, Q in reversed(list(enumerate(Qtot))):
                if Q > q:
                    Vreturn[i]=Vtot[I] # grab the voltage of that Q
                    break
    else:
        for i, q in enumerate(Qreturn):
            for I, Q in enumerate(Qtot):
                if Q >= q:
                    Vreturn[i]=Vtot[I] # grab the voltage of that Q
                    break
                    '''
    return Qtot, Vtot

def Combine (A, C, Build):
    Qa = Build["Qa"]     #Cathode Over-Capacity Ratio
    Qc = Build["Qc"]        #Total Q of Limiting Electrode
    Off = Build["Offset"] #Offset. NEGATIVE is Anode-Discharging, POSITIVE is Cathode-Discharging
    Ano = pd.DataFrame({"Q":A[0],"V":A[1]}) #Q, V
    Cat = pd.DataFrame({"Q":C[0],"V":C[1]}) #Q, V
    
    #SCALE Curves for Electrode Capacities
    Ano['Q'] = Ano['Q'] / np.max(Ano['Q']) * Qa
    Cat['Q'] = Cat['Q'] / np.max(Cat['Q']) * Qc
    
    #SHIFT curves for capacity offset
    if Off<=0:
        Ano['Q'] = Ano["Q"] + Off
    else:
        Cat['Q'] = Cat['Q'] - Off
    
    '''plt.plot(Ano["Q"],Ano["V"])'''
    '''plt.plot(Cat["Q"],Cat["V"])'''
    
    Qmax = np.min([np.max(Ano["Q"]), np.max(Cat["Q"])])
    Full = {'Q': np.linspace(0,Qmax,500), "V": np.zeros(500)}
    
    for i, theQ in enumerate(Full['Q']):
        for iA, qA in reversed(list(enumerate(Ano['Q']))):
            if qA >= theQ:
                VA = Ano['V'][iA]
                break
        for iC, qC in enumerate(Cat['Q']):
            if qC >= theQ:
                VC = Cat['V'][iC]
                break
        Full['V'][i] = VC - VA

    return Full

def dQdV (Full):
    L = len(Full["Q"])
    IC= np.zeros([L,2])
    for q in range(5,L-5):
        IC[q-4][1]=np.gradient([Full["Q"][q-4:q+4], Full["V"][q-4:q+4]])
        IC[q-4][2]=Full["V"][q]
    return IC



A = Curves(Anode)
C = Curves(Cathode)

Curve = Combine (A,C,Build)

plt.figure()
plt.plot(Curve["Q"], Curve["V"])
#plt.axes()
plt.draw()

#IC=dQdV(Curve)