import numpy as np
import matplotlib.pyplot as plt
import sys

			#Wrap -pi,pi
def wrapPi(val):
    while val < -np.pi:
        val += 2.*np.pi
    while val > np.pi:
        val -= 2.*np.pi
    return val

def wrapPi2(val):
    while val < -np.pi:
        val += 2.*np.pi
    while val > np.pi:
        val -= 2.*np.pi
    return val

			#Wrap 0,2pi
def wrap02(val):
    while val < 0.:
        val += 2.*np.pi
    while val > 2.*np.pi:
        val -= 2.*np.pi
    return val


sys.path.append('../')
simID=int(sys.argv[1])

#sims of interest:	#p5 169, 157, 152, 
			#p4 
#name='5'
name='5q100'
simnum='{0}'.format(simID)
filename='spin'+simnum+'p'+name+'.npy'
savefile='regime'+simnum+'p'+name+'.npy'

data = np.load(filename)
data = np.array(data)
print(data.size)

"""
years=10    #10000
endind=int((years*365.25)/80.268968408381913)+1

ind=np.arange(10000,10000+endind,1)

yr=data[0,ind]
pyr=data[0,ind]
dyr=data[1,ind]
tr=data[2,ind]
trp=data[2,ind]

testy=data[0,ind]
"""

yr=data[0,:]
pyr=data[0,:]
dyr=data[1,:]
tr=data[2,:]
trp=data[2,:]
#"""

extY,extT,extDy,extDt=[],[],[],[]
extYp,extTp=[],[]

print(yr.size)
print(tr.size)

tr=(tr-tr[0])/365.25
trp=(trp-trp[0])/365.25
dyr=dyr*365.25

print('Units converted!')

yr=yr%(2*np.pi)

for ii in range(len(yr)):
    yr[ii] = wrapPi(yr[ii])

pyr=pyr%(2*np.pi)


print('Wrapped!')

sign=0
signNew=0
signD=0
signDNew=0

sign=np.sign(yr[1]-yr[0])    
signD=np.sign(dyr[1]-dyr[0]) 

for ii in range(len(yr)):
    if (ii>=2):
        signNew=np.sign(yr[ii]-yr[ii-1])    
        signDNew=np.sign(dyr[ii]-dyr[ii-1]) 
        if (signNew != sign):
            extY.append(yr[ii-1])
            extT.append(tr[ii-1])
        if (signDNew != signD):
            extDy.append(dyr[ii-1])
            extDt.append(tr[ii-1])
        sign=signNew
        signD=signDNew
    if (sign==0 or signD==0):
        print('Whoopsie!')

################################################## pi

sign=0
signNew=0

sign=np.sign(pyr[1]-pyr[0])    

for ii in range(len(pyr)):
    if (ii>=2):
        signNew=np.sign(pyr[ii]-pyr[ii-1])    
        if (signNew != sign):
            extYp.append(pyr[ii-1])
            extTp.append(trp[ii-1])
        sign=signNew
    if (sign==0):
        print('Whoopsie!')
np.save(savefile,np.array([extY,extT,extDy,extDt,extYp,extTp]))

"""
print('Plotting...')


fig, axs = plt.subplots(2,1)
ax=axs[0]
ax.scatter(extT,extY,s=5)
#ax.set_ylim(0,2*3.14)
#ax.set_ylim(-3.14,3.14)
#ax.set_xlim(1000,1100)
#ax.set_xlim(-25,375)
ax.set_ylabel(r'$\gamma$',fontsize=20)
ax.set_xlabel('',fontsize=20)


ax=axs[1]
ax.scatter(extDt,extDy,s=5)
#ax.set_ylim(-2.5,2.5)
#ax.set_xlim(1000,1100)
#ax.set_xlim(-25,375)
#ax.set_ylim(-6,6)
ax.set_ylabel(r'$\dot \gamma$',fontsize=20)
ax.set_xlabel('Time (yrs)',fontsize=20)


plt.show()
#fig.savefig("SpinMED0_0-350.jpg")
#fig.savefig("SpinMED_S.jpg")
#fig.savefig("SpinMED_new.jpg")

savefile='extrema'+simnum+'p'+name+'.jpg'
fig.savefig(savefile)
"""



