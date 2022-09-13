import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import glob, sys, os

###
### This script aims to replicate figure 14 from: A generalized photon tracking approach to simulate spectral snow
###                                                     albedo and transmittance using X-ray microtomography and
###                                                     geometric optics.
###
###  This script uses existing output to run, and takes 2-3 seconds  I apologize for typos / misspellings in the comments.

## need to initially set up a couple of figures and plotting options.
cwd = os.getcwd()
path=os.path.join(cwd,'SampleData/Transmission_Compare')## set path to where transmission compare output is.

## set a couple of variables the help direct this script where to pull comparison data from.
exts=['KEXT_MIN','KEXT_MAX']
fice='0.47'

fices=['min','mean','max']
FiceNames=['0.31','0.47','0.75']


## set up the figure and plotting options.
fig=plt.figure(figsize=(7,8))

pfx='$F_{ice}$='
ax=fig.add_subplot(1,1,1)
lstyles=['-','--']

## this list of depths corresponds to the different Medium model output files to look for.
Depths=[0.5,1.0,2.0,3.0,4.0,5.0,6.0,7.0,9.0,11.0,13.0,16.0,20.0,25.0]

## loop through each extinction coefficient  folder.
for sdx, s in enumerate(exts):
    colors=['#1b9e77','#d95f02','#7570b3']
    labels=[]
    proxy=[]
    for fdx,f in enumerate(fices):
        ## loop through each f_ice value.
        for ddx, d in enumerate(Depths):
            ## Loop through each depth.
            ## find files associated with it.
            files=sorted(glob.glob('%s/%s/Fice_%s/%s*.txt'%(path,s,f,d)))
            if len(files) > 1: ## this check handles the fact that there are multiple files returned for the "1" prefix...probably could be coded better.
                ## find exact match!
                for fdx ,f in enumerate(files):
                    exactDepth=float(os.path.basename(f).split('cm')[0])
                    if d == exactDepth:
                        files=[f]
                        break

            ### load the file, skip all the header information and load the actual data.
            fname=os.path.basename(files[0])
            data=open(files[0],'r')
            lines=data.readlines()
            hline=0
            for ldx, l in enumerate(lines):
                if l.strip() == '':
                    continue
                if 'CSV Header Below this line' in l:
                    break

                hline+=1

            ## load the data into a pandas dataframe.
            cdata=pd.read_csv(files[0],header=hline+1)

            Transmiss=cdata['Transmissivty'].values ## pull the transmissivity

            # Critically, it is expected that all these files have the same wavelength.
            if ddx == 0: ## if this is the first depth, set the wavelength.
                Wavelen=cdata['WaveLength'].values
                TotalTrans=np.zeros([len(Depths),len(Wavelen)])


            TotalTrans[ddx,:]=Transmiss[:]

        ## Technically, this is a contour plot of transmissivy as a function of depth and wavelength.
        CS=ax.contour(Wavelen,Depths,TotalTrans,levels=[0.05],colors=colors[fdx],linestyles=lstyles[sdx])

        ## everything else here is just plot stylying.
        if sdx == 0:
            div_pos = plt.Line2D((0, 1), (0, 0), color=colors[fdx], linestyle='-', linewidth=2)
            proxy=proxy+[div_pos]
            labels.append('%s %.2f'%(pfx,float(FiceNames[fdx])))

    if sdx == 0:
        ax.legend(proxy,labels,loc=4,fontsize=14)
    if sdx == 1:
        ax.set_xlabel("Wavelength (nm)",fontsize=14)

    ax.set_ylabel("Depth (cm)",fontsize=14)
    ax.set_ylim(np.max(25),np.min(0.5))
    ax.set_xlim(400,1500)
ax.grid()
plt.show()
