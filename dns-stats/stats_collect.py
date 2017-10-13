import numpy             as np
import os

# Initialize figure
a = 1.66; ny= 500;
databis = np.zeros([(ny+3)*5+1] , dtype=np.float64)
direct = range(2,7)
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
      databis += data
    os.chdir('../')
databis = databis/(num*len(direct))
statist = open('stat.dat', "wb")
statist.write(bytes(databis))
