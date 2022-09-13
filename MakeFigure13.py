import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
from sklearn import linear_model

import glob as glob
import sys
import os

###
### This script aims to replicate figure 13 from: A generalized photon tracking approach to simulate spectral snow
###                                                     albedo and transmittance using X-ray microtomography and
###                                                     geometric optics.
###
###  This script will take ~ 2-3 seconds or so to run on a standard computer.  I apologize for typos / misspellings in the comments.



def main():
    formDict={'N':['New Snow','1','#66c2a5'],'R':['Rounded','o','#fc8d62'],
              'F':['Facets','v','#8da0cb'],'M':['Mixed','s','#e78ac3'],
              'MF':['Refrozen','d','#a6d854'],'C':['Crust','X','#ffd92f']}

    cwd=os.getcwd()
    ## Get the path to the properties file.
    ## Note this file is just a .csv file with all of the optical properties from various optics files condensed into one place

    PropsPath = os.path.join(cwd,'SampleData/SnowPitData/ALLSAMPLES.csv')

    csvfile=glob.glob(PropsPath)[0]
    csvdata=pd.read_csv(csvfile,header=0)

    ## Pull relevant data.
    MeshDens=pd.to_numeric(csvdata['Mesh Density'].values)
    MeshSSA=pd.to_numeric(csvdata['Mesh SSA'].values)
    MeshExt=pd.to_numeric(csvdata['K_ext'].values)
    MeshFice=pd.to_numeric(csvdata['F_ice'].values)

    print("FICE | max = %.3f | min = %.3f, mean = %.3f"%(np.max(MeshFice),np.min(MeshFice),np.mean(MeshFice)))
    print("Kext | max = %.3f | min = %.3f, mean = %.3f"%(np.max(MeshExt),np.min(MeshExt),np.mean(MeshExt)))

    ## set up regression varibles from the csv file.
    X=csvdata[['Rho*SSA']]
    Y=csvdata['K_ext']
    B=csvdata['B']

    regr = linear_model.LinearRegression()
    regr.fit(X, Y)

    print("Ext Range :%.2f,%.2f,%.2f"%(np.nanmin(MeshExt),np.nanmean(MeshExt),np.nanmax(MeshExt)))
    print("F_ice Range :%.2f,%.2f,%.2f"%(np.nanmin(MeshFice),np.nanmean(MeshFice),np.nanmax(MeshFice)))

    print("Multi Regress for predicted K_ext")
    print(regr.score(X, Y)**2.)
    print(regr.coef_)
    print(regr.intercept_)

    m=regr.coef_[0]
    b=regr.intercept_


    X=csvdata[['Mesh Density']]
    Y=csvdata['F_ice']

    regr = linear_model.LinearRegression()
    regr.fit(X, Y)

    print("Lin Regress for predicted F_ice")
    print(regr.score(X, Y)**2.)
    print(regr.coef_)
    print(regr.intercept_)

    ## the rest of the script is dedicated to plot styling.
    fig=plt.figure(figsize=(5,9))

    fig.subplots_adjust(left=0.15,top=0.95,bottom=0.08,right=0.92)

    ax=plt.subplot(211) ## this is the f_ice plot.

    for fdx, f in enumerate(formDict.keys()): ## loop through each plotting gain form and plot with appropriate color
        FormData=csvdata[csvdata['SnowType']==f]

        ax.scatter(FormData['Mesh Density'].values,FormData['F_ice'].values,
            marker=formDict[f][1],color=formDict[f][2],label=formDict[f][0],edgecolor='k')

    ax.plot([125,600],regr.intercept_+regr.coef_[0]*np.array([125,600]),color='k',ls='--',lw=2.)

    ax.set_xlabel("Mesh Density (kg m$^{-3}$)")
    ax.set_ylabel("$F_{ice}$ (-)")
    ax.set_xlim(100,800)
    ax.set_ylim(0.2,0.8)
    ax.grid()
    ax.legend(ncol=2,fontsize=12)

    ax=plt.subplot(212) # this is the rho*ssa vs. K_ext plot.
    for fdx, f in enumerate(formDict.keys()):
        FormData=csvdata[csvdata['SnowType']==f]

        ax.scatter(FormData['Rho*SSA'].values,FormData['K_ext'].values,
            marker=formDict[f][1],color=formDict[f][2],label=formDict[f][0],edgecolor='k')

    ax.plot([2.4,6.35],b+m*np.array([2.4,6.35]),color='k',ls='--',lw=2.)

    ax.set_xlabel(r"$\rho_s$*SSA")
    ax.set_ylabel("$\gamma_{sca}$ (mm$^{-1}$)")
    ax.set_ylim(0.3,1.7)
    ax.set_yticks([0.5,0.75,1.0,1.25,1.5])
    ax.grid()


    ## here you can plot the histogram of the "B" Parameter as an inset
    pos=ax.get_position()
    axsub=fig.add_axes([pos.x1-0.35,pos.y0+0.03,0.34,0.08])

    print("MEAN B PARAMETER! = %.2f"%np.nanmean(csvdata['B'].values))
    axsub.hist(csvdata['B'].values,edgecolor='k')
    axsub.axvline(np.nanmean(csvdata['B'].values),ls='--',color='r')
    axsub.text(1.04,6.2,'$B$ param',ha='left')
    axsub.set_yticklabels([])
    axsub.set_xticks([1.1,1.3,1.5,1.7,1.9])
    axsub.set_xlim(1.0,2.0)


    plt.show()





if __name__ == '__main__':
    main()
