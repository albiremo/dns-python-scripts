import numpy             as np
import os

# Initialize figure
count=0
a = 1.66; ny= 500;
utau=1.00242507175;
y_ret = np.tanh(a*(2*np.arange(-1,ny+2)/(1.0*ny)-1))/np.tanh(a)+1
yplus=y_ret*1000.0*utau;
databis = np.zeros([(ny+3)*5+1] , dtype=np.float64)
datatemp = np.zeros([(ny+3)*5+1] , dtype=np.float64)
direct = range(2,9)
for i in direct:
    h = str(i)
    os.chdir(h)
    if os.path.isfile('Runtimedata'):
     os.remove('Runtimedata')
     os.remove('Powerdata')
    os.chdir('../')
    print(h)
    files = os.listdir(path = h)
    num = len(files)
#se ci sono cartelle vuote non le conto nella media
    if num != 0:
      count += 1
      os.chdir(h)
      print(os.getcwd())
      for i in range(num):
      # Read data
       print(files[i])
       data = np.fromfile(files[i],count=((ny+3)*5+1))
       datatemp += data
      datatemp = datatemp / num
      databis += datatemp
      datatemp = np.zeros([(ny+3)*5+1], dtype=np.float64)
      os.chdir('../')
print(count)
databis = databis / count
statist = open('stat_bin.dat', "wb")
statist.write(bytes(databis))
data_temp = databis[1:].reshape(5,ny+3)
data_temp2 = data_temp[:,::-1] #dati al contrario in modo da essere sommati
data_save = 0.5*(data_temp[:,1:ny//2+1]+data_temp2[:,1:ny//2+1]) #data2 da 1 perchè lo 0 è il nodo in più  
with open('stat_ASCII.dat',"w") as stat_file:
    for (j) in [(j) for j in  range(0,ny//2)]: #alla fine c'è
         print(y_ret[j+1],yplus[j+1],data_save[0,j], data_save[1,j], data_save[2,j], data_save[3,j], data_save[4,j], file=stat_file, sep=' ' )
    #print(y_ret[ny//2-1],yplus[ny//2-1],data_temp[0,ny//2+1], data_temp[1,ny//2+1], data_temp[2,ny//2+1], data_temp[3,ny//2+1], data_temp[4,ny//2+1], file=stat_file, sep=' ' )
