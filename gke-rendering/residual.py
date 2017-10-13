#/usr/bin/env python3
# ----------------
#%matplotlib inline
from dnsdata import *
#streamlines plot
from  scipy.interpolate import interp2d
# MATPLOTLIB 3D
#from pyevtk.hl import gridToVTK 
#import vtk
#from vtk import *
import time
# --------------
# Inputs
path = './'
nxc = 2*nxd
nzc = nzd

# I piani sono stati salvati completamente
# ----------------
rx = np.arange(0,nxc)*(pi/alfa0)/nxd
rz = np.arange(0,nzc)*(2*pi/beta0)/nzd
#dichiarazioni
extract_vtk=False
extract_tec=True
# Define type
FLUXVEC  = np.dtype([('xx', np.float64), ('yy', np.float64),   ('zz', np.float64)])
GKETERMS = np.dtype([('Phir', FLUXVEC),
                     ('Phic', 'float64'),
                     ('scaleENER', 'float64'), ('scalePROD', 'float64')])

# Load data
print('start_memap')
startpos = np.zeros(ny//2+3,dtype=int); startpos[1:] = np.cumsum(ny-2*np.arange(-1,ny//2+1)+1)
residual = np.memmap('residual.bin',dtype='float64',mode='r',shape=(ny//2+2,nxc,nzc))
dissipation = np.memmap('epsilon.bin',dtype=np.float64,mode='r',shape=(startpos[-1],nxc,nzc))
print('end_memap')

#extract case ry=0 for dissipation

diss = np.zeros([ny//2+1,nxc,nzc])
for iy in range(1,ny//2+2):
 diss[iy-1]=dissipation[startpos[iy]]

if extract_vtk:
 print('salvo')
 with open(path+'residual.vtk', "w") as vtkFile:
    print('# vtk DataFile Version 2.0',file=vtkFile)
    print('Gke_data',file=vtkFile)
    print('ASCII' , file=vtkFile)
    print('DATASET RECTILINEAR_GRID', file=vtkFile)
    print('DIMENSIONS',nxc,' ',nzc,' ',ny//2+1,file=vtkFile)
    print('X_COORDINATES',nxc,'float',file=vtkFile)
    for i in range(0,nxc):
      print( rx[i], file=vtkFile, sep=' ' )
    print('Y_COORDINATES',nzc,'float',file=vtkFile)
    for j in range(0,nzc):
      print( rz[j], file=vtkFile, sep=' ' )
    print('Z_COORDINATES',ny//2+1,'float',file=vtkFile)
    for k in range(1,ny//2+2):
      print( y[k], file=vtkFile, sep=' ' )
    print('POINT_DATA ', (nxc)*(nzc)*(ny//2+1),file=vtkFile)
    print('SCALARS residual float 1',file=vtkFile)
    print('LOOKUP_TABLE default',file=vtkFile)
    for (i,j,k) in [(i,j,k) for k in  range(1,ny//2+2) for j in range(0,nzc) for i in range(0,nxc) ]:
      print(residual[k,i,j], file=vtkFile, sep=' ' )
    print('SCALARS dissipation float 1',file=vtkFile)
    print('LOOKUP_TABLE default',file=vtkFile)
    for (i,j,k) in [(i,j,k) for k in  range(0,ny//2+1) for j in range(0,nzc) for i in range(0,nxc) ]:
      print(diss[k,i,j], file=vtkFile, sep=' ' )

 print('Fertig')

if extract_tec:
   print('estraggo tec')
   with open(path+'residual.dat', "w") as tecFile:
    print('VARIABLES="rx" "rz" "Yc" "residual" "dissipation"' , file=tecFile)
    print('ZONE I=',nxc,',J=',nzc,',K=',ny//2+1,' F=POINT', file=tecFile)
    for (i,j,k) in [(i,j,k) for k in  range(0,ny//2+1) for j in range(0,nzc) for i in range(0,nxc) ]:
      print(i)
      print(rx[i],rz[j],y[k+1],residual[k+1,i,j],diss[k,i,j], file=tecFile, sep=' ')
   print('fertig')

