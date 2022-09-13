## Continuous Medium Photon-Tracking Model ##
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import os,glob,sys

###
### This script aims to replicate figure 11 from: A generalized photon tracking approach to simulate spectral snow
###                                                     albedo and transmittance using X-ray microtomography and
###                                                     geometric optics.
###
###  This script will take ~ 1-2 seconds or so to run on a standard computer.  I apologize for typos / misspellings in the comments.

## first set up some paths.
Pits=['Fine_Grain','Coarse_Grain']
PitLabs=['Fine Grain','Coarse Grain']

cwd = os.getcwd()
Tpath=os.path.join(cwd,'SampleData/Transmission_Compare/')

WaveLength=np.arange(380,1620,20)

Depths=[0.5,1.0,2.0,3.0,4.0,5.0,6.0,7.0,9.0,11.0,13.0,16.0,20.0,25.0,60.0]

## set up an array corresponding to the number of pits, wavelengths, and depths, used.
Transmiss=np.zeros([len(Pits),len(WaveLength),len(Depths)]) ## for transmission
SpecAlb=np.zeros_like(Transmiss) ## Make another array for albedo


## loop though each pit and each depth
for pdx, p in enumerate(Pits):
    for tdx, t in enumerate(Depths):

        ## pull out the spectral model output for each value.
        files=sorted(glob.glob(Tpath +"*%s/*%scm*"%(p,t)))

        ## Awkward way to help separate instances that return multiple files.
        if len(files) > 1:
            ## find exact match!
            for fdx ,f in enumerate(files):
                exactDepth=float(os.path.basename(f).split('_')[0].split('cm')[0])
                if t == exactDepth:
                    files=[f]
                    break

        ## Read the data, but skip all the header information
        data=open(files[0],'r')
        lines=data.readlines()
        hline=0
        for ldx, l in enumerate(lines):
            if l.strip() == '':
                continue

            if 'CSV Header Below this line' in l:
                break

            hline+=1

        cdata=pd.read_csv(files[0],header=hline+1)

        ## simply load the transmissivity data from the model output into the transmission array.
        Transmiss[pdx,:,tdx]=cdata['Transmissivty'].values

        ## sure, do the same thing with albedo.
        Alb=cdata['Albedo'].values
        SpecAlb[pdx,:,tdx]=Alb


## Then plot the data as a contour fill plot
fig=plt.figure(figsize=(7,9))
fig.subplots_adjust(top=0.94,bottom=0.06)

## first use pit-index = 0 (i.e., fine grain)
ax1=plt.subplot(2,1,1)
Z=ax1.contourf(WaveLength,Depths,np.transpose(Transmiss[0,:]),cmap='RdYlBu_r',levels=np.linspace(0,0.4,31),extend='both')
ax1.contour(WaveLength,Depths,np.transpose(Transmiss[0,:]),levels=[0.05,1],colors='k',linewidths=2)
ax1.set_ylabel("Depth (cm)",fontsize=15)
ax1.tick_params(axis='both', labelsize=11 )
ax1.set_ylim(25,0.5)
ax1.set_xlim(np.min(WaveLength),1450)

pos1=ax1.get_position()


cbarAx=fig.add_axes([pos1.x0+pos1.width/2.,pos1.y0+0.05,pos1.width/2.2,0.015])
cbar1=plt.colorbar(Z,cax=cbarAx,orientation='horizontal',ticks=[0,0.1,0.2,0.35],format='%d')
cbar1.ax.set_xticklabels(cbar1.ax.get_xticks(),fontsize=14,rotation=20)

## first use pit-index = 1 (i.e., coarse grain)
ax=plt.subplot(2,1,2)
Z=ax.contourf(WaveLength,Depths,np.transpose(Transmiss[1,:]),cmap='RdYlBu_r',levels=np.linspace(0,0.4,31),extend='both')
ax.contour(WaveLength,Depths,np.transpose(Transmiss[1,:]),levels=[0.05,1],colors='k',linewidths=2,label='Facets')
ax.set_xlabel("Wavelength (nm)",fontsize=15)
ax.set_ylabel("Depth (cm)",fontsize=15)
ax.set_ylim(25,0.5)
ax.tick_params(axis='both', labelsize=11 )
pos1=ax.get_position()
ax.set_xlim(np.min(WaveLength),1450)

cbarAx=fig.add_axes([pos1.x0+pos1.width/2.,pos1.y0+0.05,pos1.width/2.2,0.015])
cbar2=plt.colorbar(Z,cax=cbarAx,orientation='horizontal',ticks=[0,0.1,0.2,0.35],format='%0.1f')
cbar2.ax.set_xticklabels(cbar1.ax.get_xticks(),fontsize=14,rotation=20)


plt.show()
