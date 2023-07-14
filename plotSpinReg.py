import numpy as np
import matplotlib.pyplot as plt
import sys

#"""			#Wrap -pi,pi
def wrapPi(val):
    while val < -np.pi:
        val += 2.*np.pi
    while val > np.pi:
        val -= 2.*np.pi
    return val
#"""			#Wrap 0,2pi
def wrap02(val):
  while val < 0.:
      val += 2.*np.pi
  while val > 2.*np.pi:
      val -= 2.*np.pi
  return val
#"""

sys.path.append('../')
simID=int(sys.argv[1])

#name='4'
name='4q100'
simnum='{0}'.format(simID)
filename='spin'+simnum+'p'+name+'.npy'
file2='regData'+simnum+'p'+name+'.npy'
file3='regime'+simnum+'p'+name+'.npy'

data = np.load(filename)
data = np.array(data)

years=50000
endind=int((years*365.25)/80.268968408381913)+1		#4.2 because saved every 10

startT=130000
startT=int((startT*365.25)/80.268968408381913)+1
ind=np.arange(startT,startT+endind,1)
"""
yr=data[0,ind]
dyr=data[1,ind]
tr=data[2,ind]
"""
yr=data[0,:]
dyr=data[1,:]
tr=data[2,:]
#"""
tr=(tr-data[2,0])/365.25
dyr=dyr*365.25


data3=np.load(file3,allow_pickle=True)
data3=np.array(data3)

yrx=data3[0]
trx=data3[1]
#yrx=data3[4]
#trx=data3[5]


yr=np.array(yr)
yrx=np.array(yrx)

yr=yr%(2*np.pi)
yrx=yrx%(2*np.pi)
#"""
for ii in range(len(yr)):
    yr[ii] = wrapPi(yr[ii])

for ii in range(len(yrx)):
    yrx[ii] = wrapPi(yrx[ii])
#"""

pos = np.where(np.abs(np.diff(yr)) >= 3.14)[0]+1
tr1 = np.insert(tr, pos, np.nan)
yr = np.insert(yr, pos, np.nan)

data2 = np.load(file2,allow_pickle=True)
data2=np.array(data2)

spinR=data2[0]
tlzR=data2[1]
tlpR=data2[2]
chaR=data2[3]

idxS=np.arange(int(len(spinR)/2))
idxS=2*idxS
idxZ=np.arange(int(len(tlzR)/2))
idxZ=2*idxZ
idxP=np.arange(int(len(tlpR)/2))
idxP=2*idxP
idxC=np.arange(int(len(chaR)/2))
idxC=2*idxC

yS=np.zeros(len(spinR))
yS=yS-3.5
yZ=np.zeros(len(tlzR))
yP=np.zeros(len(tlpR))
yP=yP+3.5
yC=np.zeros(len(chaR))
yC=yC+1.7

spinR = np.insert(spinR, idxS, np.nan)
tlzR = np.insert(tlzR, idxZ, np.nan)
tlpR = np.insert(tlpR, idxP, np.nan)
chaR = np.insert(chaR, idxC, np.nan)

yS=np.insert(yS,idxS,np.nan)
yZ=np.insert(yZ,idxZ,np.nan)
yP=np.insert(yP,idxP,np.nan)
yC=np.insert(yC,idxC,np.nan)

print('Plotting...')

myfont=15

fig, axs = plt.subplots(1,1)
ax=axs
ax.plot(tr1,yr)
ax.plot(spinR,yS,label='Spinning',color='k',lw=5)
ax.plot(tlzR,yZ,label='T.L. Zero',color='dimgray',lw=5)
ax.plot(tlpR,yP,label='T.L. Pi',color='lightgray',lw=5)
ax.plot(chaR,yC,label='PTB',color='red',lw=5)
#ax.scatter(trx,yrx,s=5,color='blue')
#ax.set_ylim(0,2*3.14)
ax.set_ylim(-3.85,3.85)
#ax.set_xlim(1050,1550)
#ax.set_xlim(0,30000)
ax.set_ylabel('Substellar Longitude',fontsize=myfont)
ax.set_xlabel('Time (yrs)',fontsize=myfont)
ax.legend(fontsize=myfont)

"""
ax=axs[1]
ax.scatter(extDt,extDy,s=5)
#ax.set_ylim(-2.5,2.5)
#ax.set_xlim(1000,1100)
#ax.set_xlim(-25,375)
#ax.set_ylim(-6,6)
ax.set_ylabel('Substellar Longitude',fontsize=20)
ax.set_xlabel('Time (yrs)',fontsize=20)
"""

plt.show()


savefile='extremaTreg'+simnum+'p'+name+'NEW.pdf'
fig.savefig(savefile,bbox_inches='tight')
