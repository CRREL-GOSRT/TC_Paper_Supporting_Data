"""
This code produces Figure 5 in Letcher et al., 2021 (https://doi.org/10.5194/tc-2021-310)
This figure is a horizontal slice of a binarized microCT snow sample
image overlayed by the corresponding mesh boundary created using the ImageSeg.py script. The figure provides
a useful comparison for determining how well the mesh represents the snow sample.

Requirements:
    VTK
    pyvista
    numpy
    os
    matplotlib
"""

import vtk
from matplotlib import pyplot as plt
import pyvista as pv
import numpy as np
import os


def slice_plot(path,MeshFilename,MicroCTFilename,pltidx,voxelRes,save=True):
    """
    Inputs:
        path - (string) path to the data directory
        MeshFilename - (string) name of VTK file ('__.vtk')
        MicroCTFilename - (string) name of saved microCT data numpy array file ('__.npy')
        pltidx - (int) the horizontal slice number, 0 is the bottom of the image stack
        voxelRes - (float) voxel resolution of the microCT data, provided in microCT log file
        save - (bool) option to save figure to a PNG. The default is True.

    """
    
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(os.path.join(path,MeshFilename))
    reader.Update()
    shell = reader.GetOutput()
    
    snowbin = np.load(os.path.join(path,MicroCTFilename))
    
    ## Plot a slice of the mesh to compare with microCT scan binary image
    m = pv.PolyData(shell)
    plt.figure(figsize=(12,9))
    ax=plt.subplot(1,1,1)
    slice_depth = m.bounds[4]+(pltidx)*voxelRes      
    ax.imshow(snowbin[:,:,pltidx][::-1],cmap='binary_r',extent=[m.bounds[0],m.bounds[1],m.bounds[2],m.bounds[3]])
    slices = m.slice(normal='z',origin=(m.center[0],m.center[1],slice_depth))
    pts = slices.points
    ax.plot(pts[:,0],pts[:,1],'.')
    plt.title('Mesh vs MicroCT at %.4f mm depth' % slice_depth)
    if save==True:
        plt.savefig(os.path.join(path,('mesh_compare_%.4f.png' % slice_depth)))
        
        
if __name__ == "__main__":
    pltidx = 10
    voxelRes = 19.88250/1000. ## in millimeters, given in microCT log file
    
    path = os.getcwd()   

    MeshFilename = 'MESH.vtk'
    MicroCTFilename = 'microCT_arr.npy'
    
    slice_plot(path,MeshFilename,MicroCTFilename,pltidx,voxelRes,save=True)