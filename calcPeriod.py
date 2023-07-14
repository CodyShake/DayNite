import numpy as np
import sys
import matplotlib.pyplot as plt

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

name='5'
#name='5q100'
simnum='{0}'.format(simID)
filename='spin'+simnum+'p'+name+'.npy'
file2='regData'+simnum+'p'+name+'.npy'
savefile='perData'+simnum+'p'+name+'.npy'

Rdata= np.load(file2,allow_pickle=True)
Rdata= np.array(Rdata)
data = np.load(filename)
data = np.array(data)

years=10000.

"""
endind=int((years*365.25)/40)+1
ind=np.arange(0,endind,1)

yr=data[0,ind]
dyr=data[1,ind]
tr=data[2,ind]
"""
yr=data[0,:]				#spin data
yrT=data[0,:]
tr=data[2,:]
#"""
tr=(tr-tr[0])/365.25

tlzR=Rdata[1]		#some only do this
spinR=Rdata[0]				#regime data
tlpR=Rdata[2]

iZ=[]
iS=[]
iP=[]

yr=np.array(yr)
yrT=np.array(yrT)
yrT=yrT%(2*np.pi)

for ii in range(len(yrT)):
  yrT[ii] = wrapPi(yrT[ii])

print('Wrapped!!!')

jZ=0							#these are just a double check
jS=0
jP=0

Spin=0
print(len(spinR))
print(len(tlzR))
if (len(spinR>1)):
  Spin=1
  for i in range(len(tr)):				#find the spin times that correspond to
    if (jZ<len(tlzR) and tr[i]==tlzR[jZ]):		# regime start or end
      iZ.append(i)
      jZ+=1
    if (jS<len(spinR) and tr[i]==spinR[jS]):
      iS.append(i)
      jS+=1
    if (jP<len(tlpR) and tr[i]==tlpR[jP]):
      iP.append(i)
      jP+=1
  iZ=np.array(iZ)
  iS=np.array(iS)
  iP=np.array(iP)
else:
  for i in range(len(tr)):
    if (jZ<len(tlzR) and tr[i]==tlzR[jZ]):
      iZ.append(i)
      jZ+=1
  iZ=np.array(iZ)

TperZ=[]
TperS=[]
TperP=[]

if (Spin==1):
  for j in range(int(len(tlzR)/2)):			#if I start and end these with a obvi number,
    TperZ.append(1.2345)
    for i in range(iZ[2*j],iZ[2*j+1]):			#I can ignore the gaps with those numbers below 
      if (yrT[i]*yrT[i+1]<=0.):
        TperZ.append(tr[i])				#find roots to use for period
    TperZ.append(1.2345)
  for j in range(int(len(spinR)/2)):
    TperS.append(1.2345)
    for i in range(iS[2*j],iS[2*j+1]):
      if (yrT[i]*yrT[i+1]<=0.):
        TperS.append(tr[i])				#"" ""
    TperS.append(1.2345)
  print('Wrapping...')

  yrT=yr%(2*np.pi)

  print('Wrapped!!!')
  for j in range(int(len(tlpR)/2)):
    TperP.append(1.2345)
    for i in range(iP[2*j],iP[2*j+1]):
      if ((yrT[i]-np.pi)*(yrT[i+1]-np.pi)<=0.):
        TperP.append(tr[i])				#"" ""
    TperP.append(1.2345)
else:
  for j in range(int(len(tlzR)/2)):
    TperZ.append(1.2345)
    for i in range(iZ[2*j],iZ[2*j+1]):
      if (yrT[i]*yrT[i+1]<=0.):
        TperZ.append(tr[i])				#"" ""
    TperZ.append(1.2345)


perZ=[]
perS=[]
perP=[]

maxP=20.

for i in range(len(TperZ)-1):	
  if (TperZ[i+1]==1.2345 or TperZ[i]==1.2345):		#cutoff periods >10yr cuz those aren't real
#    print(TperZ[i],TperZ[i+1])
    continue
  if ((TperZ[i+1]-TperZ[i])>10.):
    print('Time:',TperZ[i])
  perZ.append(TperZ[i+1]-TperZ[i])	#find time between roots

if (Spin==1):
  for i in range(len(TperS)-1):
    if (TperS[i+1]==1.2345 or TperS[i]==1.2345):
      continue
    perS.append(TperS[i+1]-TperS[i])	#find time between roots
  for i in range(len(TperP)-1):
    if (TperP[i+1]==1.2345 or TperP[i]==1.2345):
      continue
    perP.append(TperP[i+1]-TperP[i])	#find time between roots


perZ=np.array(perZ)
perS=np.array(perS)
perP=np.array(perP)

perZ=perZ*2.0					#These were half periods
perS=perS*2.0
perP=perP*2.0

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO Copypasta
print('===================CopyPERIODpasta',simnum,'p',name,'=====================')


if (Spin==1):
  print(np.mean(perS))
  print(np.std(perS))
  print(np.median(perS))
  print(np.quantile(perS,0.25))
  print(np.quantile(perS,0.75))
  print(np.min(perS))
  print(np.max(perS))
  if (len(tlzR)>1):
    print(np.mean(perZ))
    print(np.std(perZ))
    print(np.median(perZ))
    print(np.quantile(perZ,0.25))
    print(np.quantile(perZ,0.75))
    print(np.min(perZ))
    print(np.max(perZ))
  else:
    print('!!!No TL Zero!!!')
  print(np.mean(perP))
  print(np.std(perP))
  print(np.median(perP))
  print(np.quantile(perP,0.25))
  print(np.quantile(perP,0.75))
  print(np.min(perP))
  print(np.max(perP))
else:
  print('!!!No spin!!!')
  print(np.mean(perZ))
  print(np.std(perZ))
  print(np.median(perZ))
  print(np.quantile(perZ,0.25))
  print(np.quantile(perZ,0.75))
  print(np.min(perZ))
  print(np.max(perZ))
  print('!!!No TL 3.14!!!')

np.save(savefile,np.array([perS,perZ,perP]))

#"""
print('Plotting...')

fig, axs = plt.subplots(1,1)

binw=1

ax=axs
ax.hist([perS,perZ,perP],bins=range(0, 100, binw),ec='k',color=['red','blue','green'],label=['Spinning','T.L. Zero','T.L. Pi'])
#ax.hist(regTL,bins=100,ec='k',label='T.L. or Chaotic')
#ax.set_ylim(-2.5,2.5)

#ax.set_xlim(1,2000)
#ax.set_xticks(np.arange(0,2050,50), minor=True)

#ax.set_xlim(-25,375)
#ax.set_ylim(-6,6)
ax.set_ylabel('Occurances',fontsize=20)
ax.set_xlabel('Period (yrs)',fontsize=20)
ax.set_yscale('log')
#ax.set_xscale('log')
ax.legend()
plt.show()
#"""


