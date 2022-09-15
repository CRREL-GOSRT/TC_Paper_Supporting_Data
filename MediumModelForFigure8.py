"""
This script is a supporting script to make figure 8 from: A generalized photon tracking approach to simulate spectral snow
                                                     albedo and transmittance using X-ray microtomography and
                                                     geometric optics.
"""
import sys
import os
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from crrelGOSRT import SlabModel

SnowType='Facets'

WaveLength=np.arange(400,1600,20)  # input for GetSpectralAlbedo function
Slab=SlabModel.SlabModel(namelist='namelist_figure8.txt')

if SnowType == 'Facets':
    Slab.namelistDict['MasterPath']='/Users/rdcrltwl/Desktop/CRRELRTM/PaperPythonScripts/SampleData/Facets/'
    Slab.namelistDict['PropFileNames'] = ['Facets_Optical.txt']
else:
    Slab.namelistDict['MasterPath']='/Users/rdcrltwl/Desktop/CRRELRTM/PaperPythonScripts/SampleData/FineGrains/'
    Slab.namelistDict['PropFileNames'] = ['FineGrain_Optical.txt']

print(Slab.namelistDict)

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
