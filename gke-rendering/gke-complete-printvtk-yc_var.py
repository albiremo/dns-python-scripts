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
# help to plot
def plotstreamlines(x,y,u,v,nx=500,ny=500,INTEGRATOR='RK4',density=3):
  xst,yst = np.linspace(x.min(),x.max(),nx), np.linspace(y.min(),y.max(),ny)
  gu,gv = interp2d(x,y,u), interp2d(x,y,v)
  plt.streamplot(xst,yst,gu(xst,yst),gv(xst,yst), density)





# ----------------
path = './'
nxc = 2*nxd
nzc = nzd

# I piani sono stati salvati completamente
# ----------------
rx = np.arange(0,nxc)*(pi/alfa0)/nxd
rz = np.arange(0,nzc)*(2*pi/beta0)/nzd
#dichiarazioni
extract_vtk=True
# Define type
FLUXVEC  = np.dtype([('xx', np.float64), ('yy', np.float64),   ('zz', np.float64)])
GKETERMS = np.dtype([('Phir', FLUXVEC),
                     ('Phic', 'float64'),
                     ('scaleENER', 'float64'), ('scalePROD', 'float64')])

# Load data
print('start_memap')
startpos = np.zeros(ny//2+3,dtype=int); startpos[1:] = np.cumsum(ny-2*np.arange(-1,ny//2+1)+1)
gke = np.memmap('gke-complete.bin',dtype=GKETERMS,mode='r',shape=(startpos[-1],nxc,nzc))
mean = np.memmap('phir_mean_der.bin',dtype=np.float64,mode='r',shape=(startpos[-1],nxc,nzc))
print('end_memap')
#------------------------------------------------------------------------------------------------------

if extract_vtk:
 print('azzero gkei2')
 gkei2 = np.zeros([ny//2,ny,nxc,nzc],dtype='float64')
# gkei2 = np.memmap('help.bin',dtype = np.float64, mode='w+', shape=(ny//2, ny, nxc, nzc))
 #yc-ry variables definition
 #-------------------------------------------------------------------------------------------------------------
 print('costruisco ry,yc')
 Y=np.zeros([startpos[-1],2]);
 for y1 in range(-1,ny//2+1):
     for y2 in range(y1,ny-y1+1):
          Y[startpos[iyd(y1)]+y2-y1,0]=0.5*(y[iyd(y1)]+y[iyd(y2)])
          Y[startpos[iyd(y1)]+y2-y1,1]=(y[iyd(y2)]-y[iyd(y1)])
 grid_Yc_pl=y[1:ny//2+1]
 grid_ry_pl=y[1:ny+1]
 grid_Yc, grid_ry = np.meshgrid(grid_Yc_pl,grid_ry_pl,indexing='ij')
 nyc=len(grid_Yc_pl)
 #---------------------------------------- GRID FILE----------------------------------------------------------
 print('costruisco i file con la griglia')
 for iyc in range(0,nyc):
  print(iyc,'/',len(grid_Yc_pl))
  with open(path+'ycgkeibis%d.vtk'%(iyc, ), "w") as vtkFile:
     print('# vtk DataFile Version 2.0',file=vtkFile)
     print('Gke_data',file=vtkFile)
     print('ASCII' , file=vtkFile)
     print('DATASET RECTILINEAR_GRID', file=vtkFile)
     print('DIMENSIONS',nxc//3,' ',nzc//3,' ',ny,file=vtkFile)
     print('X_COORDINATES',nxc//3,'float',file=vtkFile)
     for i in range(0,nxc,3):
       print( rx[i], file=vtkFile, sep=' ' )
     print('Y_COORDINATES',nzc//3,'float',file=vtkFile)
     for j in range(0,nzc,3):
       print( rz[j], file=vtkFile, sep=' ' )
     print('Z_COORDINATES',ny,'float',file=vtkFile)
     for k in range(0,ny):
       print( grid_ry_pl[k], file=vtkFile, sep=' ' )
     print('POINT_DATA ', (nxc//3)*(nzc//3)*(ny),file=vtkFile)
 #---------------------------------    SOURCE------------------------------------------------------------------------------
 print('interpolazione source')
 for iz in range(0,nzc,3):
     print(iz,'/',nzc)
     start_time=time.time()
     for ix in range(0,nxc,3):       
             print(iz,'-',ix,'/',nxc)      
             gkei2[:,:,ix,iz]=np.nan_to_num(sp.interpolate.griddata(Y,gke[:,ix,iz]['scalePROD']-mean[:,ix,iz], (grid_Yc, grid_ry), method='linear'))
     print(time.time()-start_time)
 
 
 print('appendo source ai file')
 for iyc in range(0,nyc):
      print(iyc,'/',len(grid_Yc_pl))
      with open(path+'ycgkeibis%d.vtk'%(iyc, ), "a") as vtkFile:
        print('SCALARS source float 1',file=vtkFile)
        print('LOOKUP_TABLE default',file=vtkFile)
        for (i,j,k) in [(i,j,k) for k in  range(0,ny) for j in range(0,nzc,3) for i in range(0,nxc,3) ]:
         print(gkei2[iyc,k,i,j], file=vtkFile, sep=' ' )
 print('fine source')
#------------------------------- phiry ---------------------------------------------------------------------------------
# gkei2 = np.zeros([ny//2,ny,nxc,nzc],dtype='float64')
 print('interpolazione phiry')
 for iz in range(0,nzc,3):
     print(iz,'/',nzc)
     start_time=time.time()
     for ix in range(0,nxc,3):
             print(iz,'-',ix,'/',nxc)
             gkei2[:,:,ix,iz]=np.nan_to_num(sp.interpolate.griddata(Y,gke[:,ix,iz]['Phir']['yy'], (grid_Yc, grid_ry), method='linear'))
              
     print(time.time()-start_time)
 print('appendo phiry ai file')
 for iyc in range(0,nyc):
      print(iyc,'/',len(grid_Yc_pl))
      with open(path+'ycgkeibis%d.vtk'%(iyc, ), "a") as vtkFile:
        print('SCALARS phiry float 1',file=vtkFile)
        print('LOOKUP_TABLE default',file=vtkFile)
        for (i,j,k) in [(i,j,k) for k in  range(0,ny) for j in range(0,nzc,3) for i in range(0,nxc,3) ]:
         print(gkei2[iyc,k,i,j], file=vtkFile, sep=' ' )
 print('fine phiry')
#-------------------------------------- PHIRX--------------------------------------------------------------------------------- 
 #gkei2 = np.zeros([ny//2,ny,nxc,nzc],dtype='float64')
 print('interpolazione phirx')
 for iz in range(0,nzc,3):
     print(iz,'/',nzc)
     start_time=time.time()
     for ix in range(0,nxc,3):
             print(iz,'-',ix,'/',nxc)
             gkei2[:,:,ix,iz] = np.nan_to_num(sp.interpolate.griddata(Y,gke[:,ix,iz]['Phir']['xx']-mean[:,ix,iz], (grid_Yc, grid_ry), method='linear')) 
     print(time.time()-start_time)
 print('appendo phirx ai file')
 for iyc in range(0,nyc):
      print(iyc,'/',len(grid_Yc_pl))
      with open(path+'ycgkeibis%d.vtk'%(iyc, ), "a") as vtkFile:
        print('SCALARS phirx float 1',file=vtkFile)
        print('LOOKUP_TABLE default',file=vtkFile)
        for (i,j,k) in [(i,j,k) for k in  range(0,ny) for j in range(0,nzc,3) for i in range(0,nxc,3) ]:
         print(gkei2[iyc,k,i,j], file=vtkFile, sep=' ' )
 print('fine phirx')
 #------------------------------- PHIRZ ----------------------------------------------------------------------------------
 #gkei2 = np.zeros([ny//2,ny,nxc,nzc],dtype='float64')
 print('interpolazione phirz')
 for iz in range(0,nzc,3):
     print(iz,'/',nzc)
     start_time=time.time()
     for ix in range(0,nxc,3):
             print(iz,'-',ix,'/',nxc)
             gkei2[:,:,ix,iz] = np.nan_to_num(sp.interpolate.griddata(Y,gke[:,ix,iz]['Phir']['zz'], (grid_Yc, grid_ry), method='linear')) 
     print(time.time()-start_time)
 print('appendo phirz ai file')
 for iyc in range(0,nyc):
      print(iyc,'/',len(grid_Yc_pl))
      with open(path+'ycgkeibis%d.vtk'%(iyc, ), "a") as vtkFile:
        print('SCALARS phirz float 1',file=vtkFile)
        print('LOOKUP_TABLE default',file=vtkFile)
        for (i,j,k) in [(i,j,k) for k in  range(0,ny) for j in range(0,nzc,3) for i in range(0,nxc,3) ]:
         print(gkei2[iyc,k,i,j], file=vtkFile, sep=' ' )
 print('fertig')

#------------------------ phir_mean-------------------------------------
 print('interpolazione mean')
 for iz in range(0,nzc,3):
     print(iz,'/',nzc)
     start_time=time.time()
     for ix in range(0,nxc,3):
             print(iz,'-',ix,'/',nxc)
             gkei2[:,:,ix,iz] = np.nan_to_num(sp.interpolate.griddata(Y,mean[:,ix,iz], (grid_Yc, grid_ry), method='linear'))
     print(time.time()-start_time)
 print('appendo phirz ai file')
 for iyc in range(0,nyc):
      print(iyc,'/',len(grid_Yc_pl))
      with open(path+'ycgkeibis%d.vtk'%(iyc, ), "a") as vtkFile:
        print('SCALARS mean float 1',file=vtkFile)
        print('LOOKUP_TABLE default',file=vtkFile)
        for (i,j,k) in [(i,j,k) for k in  range(0,ny) for j in range(0,nzc,3) for i in range(0,nxc,3) ]:
         print(gkei2[iyc,k,i,j], file=vtkFile, sep=' ' )
 print('fertig')
 
