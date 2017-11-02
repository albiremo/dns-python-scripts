import numpy             as np
import os

# Initialize figure
a = 1.66; ny= 500;
utau=1.00101;
y_ret = np.tanh(a*(2*np.arange(-1,ny+2)/(1.0*ny)-1))/np.tanh(a)+1
yplus=y_ret*1000.0*utau;
databis = np.zeros([(ny+3)*5+1] , dtype=np.float64)
datatemp = np.zeros([(ny+3)*5+1] , dtype=np.float64)
direct = range(2,15)
for i in direct:
    h = str(i)
    print(h)
    files = os.listdir(path = h)
    num = len(files)
    os.chdir(h)
    print(os.getcwd())
    for i in range(len(files)):
      # Read data
      print(files[i])
      data = np.fromfile(files[i],count=((ny+3)*5+1))
      datatemp += data
    datatemp = datatemp / num
    databis += datatemp
    datatemp = np.zeros([(ny+3)*5+1], dtype=np.float64)
    os.chdir('../')
databis = databis / len(direct)
statist = open('stat_bin.dat', "wb")
statist.write(bytes(databis))
data_save = databis[1:].reshape(5,ny+3)
with open('stat_ASCII.dat',"w") as stat_file:
    for (i,j) in [(i,j) for j in  range(0,ny+3)]:
         print(y_ret[j],yplus[j],data_save[0,j], data_save[1,j], data_save[2,j], data_save[3,j], data_save[4,j], file=stat_file, sep=' ' )

