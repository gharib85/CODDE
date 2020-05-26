#!/usr/bin/env python

import sys
sys.path.append('./scripts')

import json
import numpy as np
import armadillo as arma
import syst
import bath
from math import sqrt
import subprocess as sub
import os


if __name__ == '__main__':

    with open('default.json') as f:
        ini = json.load(f)
    
	nmod = 1
	# bath
	ini['bath']['temp'] = 0.5
    ini['bath']['nmod'] = nmod
    ini['bath']['jomg'] = [{"jdru":[(0.05,0.5)]} for i in xrange(nmod)]
    ini['bath']['pade'] = 1
    ini['bath']['npsd'] = 3
    bath.init (ini['bath'])

    # syst
    hams = np.zeros((2,2),dtype=complex)
    hams[0,0] = 0.5
    hams[1,1] = -0.5
    #hams[0,1]=hams[1,0]=0.5

    qmds = np.zeros((nmod,2,2),dtype=complex)
    qmds[0,0,1] = 1.0
    qmds[0,1,0] = 1.0

    arma.save (hams,ini['syst']['hamsFile'])
    arma.save (qmds,ini['syst']['qmdsFile'])
    
    # hidx
    ini['hidx']['trun'] = 0
    ini['hidx']['lmax'] = 12
    ini['hidx']['nmax'] = 100000
    ini['hidx']['ferr'] = 1.0e-10

    #proprho
    jsonInit = {"deom":ini,
                "rhot":{
                    "dt": 0.005,
                    "nt": 8000,
                    "nk": 1,
					"inistate":1,
					"xpflag": 1,
					"staticErr": 1.0e-10,
                    "sdipFile": "inp_sdip.mat",
                    "pdipFile": "inp_pdip.mat",
					"bdipFile": "inp_bdip.mat"
                },
            }

    sdip = np.zeros((2,2),dtype=float)
    sdip[0,1]=sdip[1,0]=1.0
    arma.save(sdip,'inp_sdip.mat')

    pdip = np.zeros((nmod,2,2),dtype=float)
    pdip[0,0,0] = pdip[0,1,1] = 1.0
    arma.save(pdip,'inp_pdip.mat')

    bdip = np.zeros(4,dtype=float)
    bdip[0]=0.0
    bdip[1]=0.0
    bdip[2]=0.0
    bdip[3]=0.0
    arma.save(bdip,'inp_bdip.mat')

    with open('input.json','w') as f:
        json.dump(jsonInit,f,indent=4) 
