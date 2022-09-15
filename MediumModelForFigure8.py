# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 16:04:42 2021

@author: RDCRLJTP
"""
import sys,os,glob
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from crrelGOSRT import SlabModel

SnowType='Facets'

WaveLength=np.arange(400,1600,20)  # input for GetSpectralAlbedo function
Slab=SlabModel.SlabModel(namelist='namelist_figure8.txt')

cwd = os.getcwd()
if SnowType == 'Facets':
    Slab.namelistDict['MasterPath']=os.path.join(cwd,'SampleData/Facets/')
    Slab.namelistDict['PropFileNames'] = ['Facets_Optical.txt']
else:
    Slab.namelistDict['MasterPath']=os.path.join(cwd,'SampleData/FineGrains/')
    Slab.namelistDict['PropFileNames'] = ['FineGrain_Optical.txt']

Slab.Initialize()
Azi,Zenith=1,1
nPhotons=20000
#
Albedo,Absorption,Transmiss,transmissionDict=Slab.GetSpectralAlbedo(WaveLength,Zenith,Azi,nPhotons=nPhotons)
plt.figure()
plt.plot(WaveLength,Albedo,lw='2',color='b',label="Photon Tracking Simple")
plt.show()

Slab.WriteSpectralToFile(os.getcwd()+'/SampleData/%s/%s_Output.txt'%(SnowType,SnowType),
    nPhotons,Zenith,Azi,WaveLength,Albedo,Absorption,Transmiss,filename='Sample, 100% diffuse')
