from matplotlib import pyplot as plt
import numpy as np

from matplotlib.ticker import MultipleLocator
import pandas as pd
import sys,os,glob


###
### This script aims to replicate figure 15 from: A generalized photon tracking approach to simulate spectral snow
###                                                     albedo and transmittance using X-ray microtomography and
###                                                     geometric optics.
###
###  This script will take 1-3 seconds or so to run on a standard computer.  I apologize for typos / misspellings in the comments.

## first need to to set up some figure plotting options.
fig = plt.figure(constrained_layout=True,figsize=(10,9))
## this uses the grid_spec subplot layout function to set the subplots for each variable
spec = fig.add_gridspec(ncols=6, nrows=1)
gs00 = fig.add_subplot(spec[:,:2])
EXT = fig.add_subplot(spec[:,2])
FICE = fig.add_subplot(spec[:,3])
DENS = fig.add_subplot(spec[:,4])
SSA = fig.add_subplot(spec[:,5])


depth=34 ## note that depth here is in centimeters. #

## hard coded snow pit stratigraphy information from field observation.
layerTops=[34,31,19,14,13,9,8,0] ## Tops of each layer.
LayerTypes=['DF','RG','F','CR','F','CR','F'] ## Grain form of each layer.

## Help orient the color / label for each gin form.
TypeDict={'DF':['New Snow','#a6cee3'],
          'RG':['Mixed Rounded Grains','#1f78b4'],
          'F':['Facets','#b2df8a'],
          'CR':['Crust','#33a02c']}


cwd = os.getcwd()
PitDepthFile=os.path.join(cwd,'SampleData/SnowPitData/UVD_Depths.csv')
PitDataFile=os.path.join(cwd,'SampleData/SnowPitData/ALLSAMPLES.csv')

## Read in each file -->
pitDepths = pd.read_csv(PitDepthFile)
PitData=pd.read_csv(PitDataFile)
## Get the data associated with each file.
pitDnames = pitDepths['PitName'].values
pitSnames = PitData['FileName'].values

## set initial lists that will contain the data.
SampleDepths=[]
SampleDens=[]
SampleSSA=[]
SampleKext=[]
SampleFice=[]
SampleB=[]

for sdx, s in enumerate(pitSnames):  ## loop through each sample name
     for ddx, d in enumerate(pitDnames): ## Loop through each depth
        ## basically, if this microCT sample was collected within this depth range, then grab it!
        if d in s: #Then these match!
            ## add the data to the list.
            PitDataC=PitData[PitData['FileName'] == s]
            SampleDepths.append(pitDepths[pitDepths['PitName'] == d]['Depth'].values[0])
            SampleDens.append(PitDataC['Mesh Density'].values[0])
            SampleSSA.append(PitDataC['Mesh SSA'].values[0])
            SampleKext.append(PitDataC['K_ext'].values[0])
            SampleFice.append(PitDataC['F_ice'].values[0])
            SampleB.append(PitDataC['B'].values[0])

## redefine the lists as numpy arrays.
SampleB=np.array(SampleB)
SampleSSA=np.array(SampleSSA)
SampleFice=np.array(SampleFice)
SampleKext=np.array(SampleKext)
SampleDepths=np.array(SampleDepths)
SampleDens=np.array(SampleDens)

### this handles the plotting for each layer.
for ldx , l in enumerate(layerTops[:-1]): ## loop through each layer

    ## first colorfill the layer to give it a background.
    gs00.fill_between([0,1],layerTops[ldx+1],l,color=TypeDict[LayerTypes[ldx]][1])
    gs00.text(0.02,l-0.05,TypeDict[LayerTypes[ldx]][0],ha='left',va='top',fontsize=12)
    gs00.plot([0,1],[l,l],color='k',lw=0.6,ls='--')

    ## Only select microCT data that falls within the layer.
    SSABOX = SampleSSA[np.where((SampleDepths > layerTops[ldx+1]) & (SampleDepths <= l))]
    KextBOX = SampleKext[np.where((SampleDepths > layerTops[ldx+1]) & (SampleDepths <= l))]
    FiceBOX = SampleFice[np.where((SampleDepths > layerTops[ldx+1]) & (SampleDepths <= l))]
    DensBOX = SampleDens[np.where((SampleDepths > layerTops[ldx+1]) & (SampleDepths <= l))]

    ## if there is SOME microCT data there, then plot the violin plot. -> Extinction Coefficient
    if len(KextBOX) > 0:
        yLoc=(layerTops[ldx+1]+l)/2.
        parts=EXT.violinplot(KextBOX, vert=False, positions=[yLoc],widths=1.5)

        EXT.axhline(l,color='k',lw=0.6,ls='--')  # mark the layer separation.


        for pc in parts['bodies']:
            pc.set_facecolor(TypeDict[LayerTypes[ldx]][1])
            pc.set_edgecolor('black')
            pc.set_alpha(1)

        ## -> Density
        parts=DENS.violinplot(DensBOX, vert=False, positions=[yLoc],widths=1.5)
        DENS.axhline(l,color='k',lw=0.6,ls='--')

        for pc in parts['bodies']:
            pc.set_facecolor(TypeDict[LayerTypes[ldx]][1])
            pc.set_edgecolor('black')
            pc.set_alpha(1)


        ## -> F_ice
        parts=FICE.violinplot(FiceBOX, vert=False, positions=[yLoc],widths=1.5)
        FICE.axhline(l,color='k',lw=0.6,ls='--')
        for pc in parts['bodies']:
            pc.set_facecolor(TypeDict[LayerTypes[ldx]][1])
            pc.set_edgecolor('black')
            pc.set_alpha(1)

        ## -> SSA
        parts=SSA.violinplot(SSABOX, vert=False, positions=[yLoc],widths=1.5)
        SSA.axhline(l,color='k',lw=0.6,ls='--')

        for pc in parts['bodies']:
            pc.set_facecolor(TypeDict[LayerTypes[ldx]][1])
            pc.set_edgecolor('black')
            pc.set_alpha(1)

        ## just print out some information.
        print("Top %.1f | Bottom %.1f | Sample # %i"%(l,layerTops[ldx+1],len(FiceBOX)))
        print("Kext = %.3f | IQR %.3f"%(np.nanmean(KextBOX), np.subtract(*np.percentile(KextBOX, [75, 25]))))
        print("Fice = %.3f | IQR %.3f"%(np.nanmean(FiceBOX), np.subtract(*np.percentile(FiceBOX, [75, 25]))))

### Some plot styling.
gs00.set_xticks([])
gs00.set_yticks([0,5,10,15,20,25,30,34])
minorLocator = MultipleLocator(2.5)
gs00.yaxis.set_minor_locator(minorLocator)
gs00.set_ylim(0,35)
gs00.set_xlim(0,1)

## now that the violin plots have been made, we just scatter each individual value for each variable.
EXT.scatter(SampleKext,SampleDepths,s=10,edgecolor='k')
EXT.set_ylim(0,35)
EXT.set_yticklabels([])
EXT.set_xticks([0.5,1.0,1.5])
EXT.set_xlim(0.35,1.65)
EXT.yaxis.set_minor_locator(minorLocator)
EXT.set_title(r"$\gamma_{sca}$",loc='left',fontsize=16)
EXT.set_xlabel("(mm$^{-1}$)",fontsize=12)
EXT.set_yticks([0,5,10,15,20,25,30,34])


FICE.scatter(SampleFice,SampleDepths,s=10,edgecolor='k')
FICE.set_ylim(0,35)
FICE.set_yticklabels([])
FICE.set_xticks([0.3,0.4,0.5])
FICE.set_xlim(0.25,0.55)
FICE.yaxis.set_minor_locator(minorLocator)
FICE.set_title(r"$F_{ice}$",loc='left',fontsize=16)
FICE.set_xlabel("(-)",fontsize=12)
FICE.set_yticks([0,5,10,15,20,25,30,34])

DENS.scatter(SampleDens,SampleDepths,s=10,edgecolor='k')
DENS.set_ylim(0,35)
DENS.set_yticklabels([])
DENS.set_xticks([150,250,350])
DENS.set_xlim(120,350)
DENS.yaxis.set_minor_locator(minorLocator)
DENS.set_title(r"$\rho_s$",loc='left',fontsize=16)
DENS.set_xlabel("(kg m$^{-3}$)",fontsize=12)
DENS.set_yticks([0,5,10,15,20,25,30,34])

SSA.scatter(SampleSSA,SampleDepths,s=10,edgecolor='k')
SSA.set_ylim(0,35)
SSA.set_yticklabels([])
SSA.set_xticks([10,15,20,25,30])
SSA.set_xlim(8,30)
SSA.yaxis.set_minor_locator(minorLocator)
SSA.set_title("SSA",loc='left',fontsize=16)
SSA.set_xlabel(r"(m$^{2}$ kg$^{-1}$)",fontsize=12)
SSA.set_yticks([0,5,10,15,20,25,30,34])

plt.show()
