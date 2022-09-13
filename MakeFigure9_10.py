import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import glob as glob,sys,os
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from crrelGOSRT import SlabModel, RTcode, Utilities

###
### This script aims to replicate figures 9 and 8 from: A generalized photon tracking approach to simulate spectral snow
###                                                     albedo and transmittance using X-ray microtomography and
###                                                     geometric optics.
###
###  This script will take ~ 1hr or so to run on a standard computer.  I apologize for typos / misspellings in the comments.

## need to initially set up a couple of figures and plotting options.
axes=[]
subplots=(5,4)

fig1=plt.figure(figsize=(12,10)) ## this is the BRDF polar plot figure
fig2=plt.figure(figsize=(10,7)) ## this is the albedo vs. zenith angle plot figure

## add a subplot to figure 2.
ax=fig2.add_subplot(111)
ax.tick_params(axis='x', labelsize=11)
ax.tick_params(axis='y', labelsize=11)
######

## set a few wavelengths to use.
WaveLengths=[650,800,1000,1300] ## in nanometers.
Zenith = np.arange(5,90,5) ## in degrees
Azi=0.0 ## in degrees.
nPhotons = 10000 ## number of photons used in the slab model.

cwd = os.getcwd() ## Get current working directory, assumes folder structure as though you are running these out of the GitHub.

## sets up some colors
colors=['#D81B60','#1E88E5','#FFC107','#004D40']

## Here we append the axes list with subplots for each zenith angle.
for zdx, z in enumerate(Zenith):
    axes.append(fig1.add_subplot(*subplots,zdx+1,projection='polar'))

axes.append(fig1.add_subplot(*subplots,zdx+1,projection='polar'))

##Now that the plot axes are set, we initialize the slab model.
Slab=SlabModel.SlabModel(namelist='namelist_figure8.txt') ## Start with the same config as figure_8.
Slab.namelistDict['DiffuseFraction']=0.0 ## Since we're looking at the direct reflectance, set diffuse fraction to 0.
Slab.namelistDict['MasterPath']=os.path.join(cwd,'SampleData/FineGrains/') ## Set the path and file name to point to the fine grain file.
Slab.namelistDict['PropFileNames'] = ['FineGrain_Optical.txt']
Slab.Initialize() ## initialize the model with the namelist values applied.


## run the model, looping through all the WaveLengths in the list of WaveLengths
for wdx, WaveLength in enumerate(WaveLengths):
    Albs=[] ## list of "albedos" specific to this wavelength for albedo vs. zenith angle comparison.
    for zdx, z in enumerate(Zenith): ## loop through all zenith angles.

        ## Run the BRDF model.
        BRDFArray,BRAziBins,BRZenBins,albedo,absorbed,transmiss = Slab.RunBRDF(WaveLength,z,Azi,nPhotons=nPhotons,binSize=10.0)

        ## Compute the albedo as the hemispherically integrated BRDF -> HDRF.
        dTheta=np.abs(np.radians(BRZenBins[1])-np.radians(BRZenBins[0]))
        ZenZen=np.radians(np.tile(BRZenBins, (len(BRAziBins), 1)))
        Albedo=np.sum(BRDFArray*np.cos(ZenZen)*np.sin(ZenZen))*dTheta**2/nPhotons

        if WaveLength == 800: ## IF this is the 800nm wavelength, then we output the polar BRDF contourfill plot.
            ## Choose the axes associated with the current zenith angle....
            Z=axes[zdx].contourf(np.radians(BRAziBins),BRZenBins,np.transpose(BRDFArray)/(nPhotons),cmap='jet',levels=np.linspace(0,1.5,41),extend='both')
            axes[zdx].set_title(r"$\theta$ = %.1f $^{\circ}$"%(z))
            axes[zdx].set_xticklabels([])

        print("Zenith Angle = %.1f | Albedo = %.2f"%(z,Albedo))


        Albs.append(Albedo) ## append to albedo list.

    ## once out of the zenith angle loop, then plot the albedo vs. zenith comparison.
    ax.plot(Zenith,Albs,label='$\lambda$ = %1.f nm'%WaveLength,color=colors[wdx],lw=2.0)

## some plotting associated with the zenith angle.
ax.set_xlabel("Zenith Angle (degrees)",fontsize=16)
ax.set_ylabel("Albedo", fontsize=16)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.legend(ncol=2,fontsize=14)
ax.grid()

## save each figure!
fig2.savefig(os.path.join(cwd,'Albedo_v_zenith.png'),dpi=120)
fig1.savefig(os.path.join(cwd,'BRDF_FINEGRAIN.png'),dpi=120)

## also show the figure (optional)
plt.show()
