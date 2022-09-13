## Compare snow to ASD! ##
import sys
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

import glob,os,sys

def main():
    ## Set paths to data here ->
    ## The "sim" and "ModelParentPath" input paths assume that there is a parent folder that contains several sub-folders
    ## specific to different simulations. Each sub-folder (set by variable "sim") has an arbitrary spectral output files
    ## the spectral output files would have to have a "depth" value that distinguishes them from one another in this script.

    cwd = os.getcwd()
    sim = 'UVD_Spectral/' ## sub path to model spectral output specific to this set of simulations -> Must be within ModelParentPath
    ModelParentPath=os.path.join(cwd,'SampleData/') ## Path to parent model output folder.

    ASDFolder=os.path.join(cwd,'SampleData/UVD_FEB12_ASD/') ## Folder where ASD post processed text data is output.

    # List of depths corresponding to the number of files used in the comparison.
    # Each depth will correspond to a different ASD input and model input file.
    depths=[340.0,45.0,25.0] ## Depth is in mm.

    ReferenceReflect = 0.965 ## User "tunable" value for assumed reference panel reflectance.  Should be close to 0.98
    # A value of 0.965 was chosen here because values any higher led to albedos > 1 for a number of scans.


    ## First the file numbers corresponding to the ASD scans are hard coded into a dictionary that maps
    ## the depth to scan number. -> Numbers can be found in accompanying metadata file.

    ## Numbers used for this scan!
        ## 0 = Virgin Snow, no panels!
        ## 28 = Black Panel, 9 cm from top!
        ## 35 = Black Panel, 4.75 cm from top!
        ## 42 = Black Panel  2.5 cm from top!


    ## These dictionaries specify which ASD file number is associated with which depth,
    ## determines which reference scan to use (or averages them "-1")

    scanNumber={25.0:42,45.0:35,90.0:28,340.0:0} ## maps depth to ASD file number
    RefNums={25.0:1,45.0:0,90.0:-1,340.0:-1} ## Determines which scan to use (0,1,-1) -> -1 is average of the two.
    labels={25.0:'Panel 2.5cm',340.0:'Virgin Snow',90.0:'Panel 9cm',45.0:'Panel 4.5cm'} # Sets labels for legend.
    colors={340:'#2c7bb6',25.0:'#d7191c',45.0:'#fdae61',90.0:'#abd9e9'} # Sets color for lines.

    ## Creates figure.
    fig=plt.figure(figsize=(9,8))
    ax=plt.subplot(111)

    ## loops through each depth
    for ddx, d in enumerate(depths):
        path=os.path.join(ModelParentPath,sim,'*%s*.txt'%(d)) ## Locate the model file.
        modfile=glob.glob(path)[0] ## Load filepath.

        ## Use GetASDAlb function to get the data from the ASD.
        wavelength,albedo,RefData,ScanData=GetASDAlb(ASDFolder,scanNumber[d],5,ReferenceReflect,refNum=RefNums[d])

        ###############################################################
        #  This block of code simply pulls the simulated albedo data. #
        ###############################################################
        data=open(modfile,'r')
        lines=data.readlines()
        hline=0
        for ldx, l in enumerate(lines):
            if l.strip() == '':
                continue
            if 'CSV Header Below this line' in l:
                break
            hline+=1
        cdata=pd.read_csv(modfile,header=hline+1)
        modAlb=cdata['Albedo'].values
        modWavelength=cdata['WaveLength'].values
        ###############################################################
        #                                                             #
        ###############################################################

        ## Plot the data on the figure !!
        ax.plot(wavelength,np.nanmean(albedo,axis=0),label=labels[d],lw=1.5,color=colors[d]) ## Plot observations as a solid line!
        ax.fill_between(wavelength,np.nanpercentile(albedo,25,axis=0),np.nanpercentile(albedo,75,axis=0),color=colors[d],alpha=0.3)  ## colorfill observation variance
        ax.plot(modWavelength,modAlb,lw=0.34,marker='o',color=colors[d],ls='--') ## plot model as a thin dashed line with markers.

        ## Do some interpolation so RMSE can be computed.
        modObs=np.interp(modWavelength,wavelength,np.nanmean(albedo,axis=0))
        RMSE=np.sqrt(np.nanmean((modAlb-modObs)**2.))
        ## print the RMSE
        print(RMSE)

    ## finished looping through different depths.
    ## Add some general styling to the figure.
    ax.grid()
    ax.set_ylabel("Albedo",fontsize=14)
    ax.set_xlabel("WaveLength (nm)",fontsize=14)
    ax.legend(fontsize=12)
    ax.tick_params(axis='both', labelsize=11 )
    ax.set_ylim(0.0,1.1)
    ax.set_xlim(modWavelength[0],1600)

    plt.show()
    ####

    ### finished.


def GetASDAlb(filepath,sampleNum,NumSamples,scale=0.98,refNum=0):
    """ This function use used to find the appropriate ASD files in a specified folder.
        It is assumed that the "sampleNum" corresponds to the specific reference scan
        collected prior to the snow samples.
        Scan order assumes ->
            Reference Scan (0)
            - Samples * NumSamples
            Reference Scan (1)

        Inputs -
            - filepath (string): path to ASD sample files
            - sample num (int): file number corresponding to initial reference scan
            - NumSamples (int): number of samples collected between reference scans
            - scale (float): assumed wavelength independent reflectance of the reference panel
            - refNum (int 0,1,-1): Which reference panel to use.  A value of -1 averages the two panels.
    """
    ASDfiles=sorted(glob.glob(filepath+'*.asd.*'))

    fileIDs=[int(i.split('/')[-1].split('.')[0][-4:]) for i in ASDfiles] ## Load all the file numbers into a list

    RefIndices=[fileIDs.index(sampleNum),fileIDs.index(sampleNum+NumSamples+1)] ## Pick out reference panel indicies
    RefFiles=[ASDfiles[i] for i in RefIndices] ## Get the reference files!

    ScanIndices=[fileIDs.index(sampleNum+i+1) for i in range(NumSamples)]  ## get the sample indicies
    ScanFiles=[ASDfiles[i] for i in ScanIndices] ## get the sample files!

    WL,RefData=ReadDataFiles(RefFiles)  #read the data reference data
    WL1,ScanData=ReadDataFiles(ScanFiles) #read teh sample data
    if refNum == -1:
        albedo=ScanData/(np.nanmean(RefData,axis=0)/scale)  ## average the reference panels
    else:
        albedo=ScanData/(RefData[refNum]/scale) ## User specified reference panel.


    return WL,albedo,RefData,ScanData

def ReadDataFiles(RefFiles):
    for idx,rFile in enumerate(RefFiles):
        cdata=pd.read_csv(rFile)
        dataHeader=".".join(rFile.split('/')[-1].split('.')[0:2])
        interp=False
        if idx == 0:  #get a baseline wavelength (they should all be the same, but just in case!)
            wavelength=cdata['Wavelength'].values
            RefData=np.zeros([len(RefFiles),len(wavelength)])  ## set the reflectance data array
        else:
            wv1=cdata['Wavelength'].values

            if wv1.all() != wavelength.all(): ## check to ensure the wavelengths from this scan are equal to the baseline
                print("WARNING, Wavelength not equal to reference wavelength, interpolating!")
                interp=True ## if they aren't, then I guess we'll interpolate.  I'll at least throw a warning though!

        rawData=cdata[dataHeader].values ## Get the reflectance data.
        if interp == True:
            rawData=np.interp(wavelength,wv1,rawData)
        RefData[idx,:]=rawData[:]

    return wavelength,RefData  # return the data!


if __name__=='__main__':
    main()
