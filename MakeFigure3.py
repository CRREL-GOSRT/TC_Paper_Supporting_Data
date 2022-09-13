## Continuous Medium Photon-Tracking Model ##
import numpy as np
from matplotlib import pyplot as plt
import glob as glob,os,sys
from matplotlib import cm
from crrelGOSRT import SlabModel, RTcode, Utilities
###
### This example shows how to make figure 3 from
###     A generalized photon tracking approach to simulate spectral snow albedo and
###     transmittance using X-ray microtomography and
###     geometric optics.
###
### This script will take ~60-120 seconds to run based on your specific inputs.
### NOTE -> because of the random-walk nature of the model, this will not exactly replicate the figure, but rather something that is similar to it.

## Get the namelist and set the model depths.
cwd = os.getcwd()
Slab=SlabModel.SlabModel(namelist=os.path.join(cwd,'namelist_figure3.txt'))
Slab.namelistDict['LayerTops']=[200,130,0]
Slab.namelistDict['MasterPath']=os.path.join(cwd,'SampleData/') ## Set the path and file name to point to the fine grain file.

## intialize the model based on the namelist value.
Slab.Initialize()

## some information for the figure.
layerLabs=['Coarse Grain','Fine Grain']

breakout=False

wv = 850 ## Wave length.  Should be < 1000nm for optimal results.
Zenith = 0.0 ## Zenith Angle.  Recommended 0.0 for this example, but can be set to something else.
Azi = 100 ## Azimuth angle, does not matter much.
TracePhotons = 2  ## how many photons to track.  Must be at least 2 due to model architecture.

while breakout == False:
    ## Note, this may take a while to for a minimum depth value to approach 50mm.  You can change this by setting the
    ## min value to a shallower depth.
    albedo,abso,transmiss,Xout,Yout,Zout,PowerOut=Slab.PhotonTrace(wv,Zenith,Azi,TracePhotons,verbose = False)

    if np.min(Zout) < 50:
        breakout = True
        break

### Below this line is all code to support the plotting. ####
#
#############################################################
layerfill=['k','k']
alphas=[0.1,0.25]

fig=plt.figure(figsize=(9,9))
ax=plt.subplot(111)
fig.subplots_adjust(top=0.95,right=0.90,left=0.08,bottom=0.08)

for i in range(len(Xout)):
    Z=ax.scatter(Xout[i],Zout[i],c=PowerOut[i],cmap='jet',vmin=0,vmax=1,s=7,marker='s',alpha=1.0,zorder=6)

for ldx,l in enumerate(Slab.namelistDict['LayerTops'][::-1][:-1]):
    ax.fill_between([-80,80],l,Slab.namelistDict['LayerTops'][::-1][ldx+1],color=layerfill[ldx],alpha=alphas[ldx])
    ax.text(-78,Slab.namelistDict['LayerTops'][::-1][ldx+1]-5,layerLabs[ldx],ha='left',fontsize=12)

pos=ax.get_position()

plt.ylim(0,np.max(Slab.namelistDict['LayerTops']))
ax.set_ylabel("(mm)",fontsize=15)
ax.set_xlim(-80,80)
ax.set_xlabel("(mm)",fontsize=15)

cbarAX=fig.add_axes([pos.x1+0.01,pos.y0,0.015,pos.height])
cbar=plt.colorbar(Z,ticks=np.arange(0,1.1,0.1),cax=cbarAX)
cbar.ax.set_ylabel("Power")

plt.show()
