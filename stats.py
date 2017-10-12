import numpy             as np
import matplotlib.pyplot as plt

# Initialize figure
f, ax = plt.subplots(2,1,sharex=True)

# Input (to be set manually) XXX TODO read dns.in
a = 1.66; ny= 500;
files = ['stat.dat']
linet = ['-']
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

utau=1.00101;
# Grid
y = np.tanh(a*(2*np.arange(-1,ny+2)/(1.0*ny)-1))/np.tanh(a)+1
yplus=y*1000.0*utau;
for i in range(len(files)):

  # Read data
  istat = np.fromfile(files[i],count=1,dtype=np.int64);
  data = np.fromfile(files[i],count=((ny+3)*5+1))[1:].reshape(5,ny+3)

  # Remove mean from uu
  data[1,:] -= data[0,:]**2

  # Plot data
  ax[0].plot(yplus[1:-1],data[0,1:-1],linet[i])
  ax[0].set_xlim([yplus[1],1000.0*utau])
  ax[0].set_ylabel('$U^+$')
  uu,=ax[1].plot(yplus[1:-1],data[1,1:-1],linet[i],label='$<u^2>$')
  vv,=ax[1].plot(yplus[1:-1],data[2,1:-1],linet[i],label='$<v^2>$')
  ww,=ax[1].plot(yplus[1:-1],data[3,1:-1],linet[i],label='$<w^2>$')
  uv,=ax[1].plot(yplus[1:-1],-data[4,1:-1],linet[i],label='$-<uv>$')
  ax[1].set_xlabel('$y^+$')
  ax[1].legend(handles=[uu,vv,ww,uv])
  #ax[1].set_xlim([yplus[1],30])
  #ax[0].set_xscale('log')
  #legend()

#print(istat)
plt.savefig('stats')
plt.show()
