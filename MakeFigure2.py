## test photon track! ##
"""
This python script makes figure2 from the paper -> A generalized photon tracking:approach to
                                                  simulate spectral snow albedo and transmittance using X-ray
                                                    microtomography and geometric optics.

Note that the option to make a figure is simply called as part of the RayTracing_OpticalProperties subroutine.
"""
import os,glob
from crrelGOSRT import PhotonTrack
import matplotlib.pyplot as plt


cwd=os.getcwd()
SnowType = 'Facets'

parentPath=glob.glob(os.path.join(cwd,'SampleData/%s/*.vtk'%SnowType))[0] ## path to the microCT .vtk mesh file. -> MUST MAKE SURE THIS IS CORRECT
MaterialPath = '/path/to/Materials/' ## file where the ice-refractive index.csv file is stored.
WaveLength='1000nm' ## Wavelength
VoxelRes='19.88250um' ## Voxel resolution

OutputName=os.path.join(cwd,'OPTICAL_%s_example.txt'%SnowType)
## Call the below subroutine to compute the medium optical properties from ray-tracing. ##
## Many of the arguments are only used under certain conditions.  For example, the grain samples is not used if
## PF_fromSegmentedParticles = False.
## To reproduce the figure from the paper, we recommend the below options.
## Note the figure was generated from the -> optical properties.

## Basically, everything is handled in the photon track.  The output optical properties are saved to "OutputName"
## The figure is accessed and saved below.
fig=PhotonTrack.RayTracing_OpticalProperties(parentPath,GrainPath,OutputName,MaterialPath,WaveLength,VoxelRes,
                                         verbose=True,nPhotons=1200,GrainSamples=150,Advanced=True,
                                         maxBounce=150,phaseSmooth=0,PhaseBins=180,
                                         particlePhase=True,raylen='auto',PF_fromSegmentedParticles=False,
                                         MaxTIR=35,Tolerance=0.001)

fig.savefig(os.path.join(cwd,'%s_Example.png'%SnowType),dpi=120)
plt.show()
