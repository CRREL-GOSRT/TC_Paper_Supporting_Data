import numpy as np
from matplotlib import pyplot as plt
import glob,sys,os

###
### This script aims to replicate figures 9 and 8 from: A generalized photon tracking approach to simulate spectral snow
###                                                     albedo and transmittance using X-ray microtomography and
###                                                     geometric optics.
###
###  This script will take ~ 1hr or so to run on a standard computer.  I apologize for typos / misspellings in the comments.

## need to initially set up a couple of figures and plotting options.

def main():
    cwd = os.getcwd()
    FacetsFile = glob.glob(os.path.join(cwd,'SampleData/Facets/Facets_Output.txt'))[0]
    FineGrainFile = glob.glob(os.path.join(cwd,'SampleData/FineGrains/FineGrains*Output*.txt'))[0]

    print(FacetsFile)
    print(FineGrainFile)

    FineData=getSpectra(FineGrainFile)
    FacetsData=getSpectra(FacetsFile)

    plt.figure()
    ax=plt.subplot(111)
    plt.plot(FineData.WaveLength,FineData.Albedo,label='Fine Grain')
    plt.plot(FacetsData.WaveLength,FacetsData.Albedo,label='Facets')
    ax.grid()
    ax.set_title("Simulated Spectral Albedo (-)")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Albedo")
    ax.legend()
    plt.show()

def getSpectra(filename):
    import pandas as pd
    data = open(filename,'r')

    for ldx, l in enumerate(data.readlines()):
        if 'CSV Header Below this line' in l:
            hline=ldx+1
            break


    data.close()
    data = pd.read_csv(filename,header=hline)

    return data

if __name__ == '__main__':
    main()
