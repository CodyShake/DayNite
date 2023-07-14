import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.optimize import curve_fit

def func_powerlaw(x, m, c):		#define the function (power law) that i wil fit later
    return x**m * c

simNames=['152p5','152p5q100','157p5','157p5q100','169p5','169p5q100','17p4','152p4','157p4','169p4','17p4q100','132p4q100','152p4q100','157p4q100','169p4q100','182p4q100','132p3','152p3','169p3','132p3q100','152p3q100','169p3q100','132p2','152p2','169p2','132p2q100','152p2q100','169p2q100']

spinR,tlzR,tlpR,chaR=[],[],[],[]

for i in range(0,len(simNames)):
  filename='regData'+simNames[i]+'.npy'
  data = np.load(filename,allow_pickle=True)
  spinR.extend(data[0])
  tlzR.extend(data[1])
  tlpR.extend(data[2])
  chaR.extend(data[3])


"""
for i in range(0,int(len(spinR)/2)-1):
  spinN[i]=spinR[2*i+1]-spinR[2*i]

filename='regData'+simnum+'p'+name+q+'.npy'

data = np.load(filename,allow_pickle=True)
spinR=np.array(data[0])
tlzR=np.array(data[1])
tlpR=np.array(data[2])
chaR=np.array(data[3])
"""

spinR=np.array(spinR)
tlzR=np.array(tlzR)
tlpR=np.array(tlpR)
chaR=np.array(chaR)

print(spinR.shape)

spinN=np.zeros(int(len(spinR)/2))
tlzN=np.zeros(int(len(tlzR)/2))
tlpN=np.zeros(int(len(tlpR)/2))
chaN=np.zeros(int(len(chaR)/2))

#regCH=np.zeros(int(len(regR)/2))

print('Length  spinN:',len(spinN))

for i in range(0,int(len(spinR)/2)-1):
  spinN[i]=spinR[2*i+1]-spinR[2*i]
for i in range(0,int(len(tlzR)/2)-1):
  tlzN[i]=tlzR[2*i+1]-tlzR[2*i]
for i in range(0,int(len(tlpR)/2)-1):
  tlpN[i]=tlpR[2*i+1]-tlpR[2*i]
for i in range(0,int(len(chaR)/2)):
  chaN[i]=chaR[2*i+1]-chaR[2*i]

print('========================================')
print('Mean Spin Regime Length (yrs):',np.mean(spinN))
print('StdDev Spin Regime Length (yrs):',np.std(spinN))
print('Medi Spin Regime Length (yrs):',np.median(spinN))
print('25th Spin Regime Length (yrs):',np.quantile(spinN,0.25))
print('75th Spin Regime Length (yrs):',np.quantile(spinN,0.75))
print('========================================')
print('========================================')
print('Mean TL0  Regime Length (yrs):',np.mean(tlzN))
print('StdDev TL0 Regime Length (yrs):',np.std(tlzN))
print('Medi TL0  Regime Length (yrs):',np.median(tlzN))
print('25th TL0  Regime Length (yrs):',np.quantile(tlzN,0.25))
print('75th TL0  Regime Length (yrs):',np.quantile(tlzN,0.75))
print('========================================')
print('========================================')
print('Mean TLpi Regime Length (yrs):',np.mean(tlpN))
print('StdDev TLpi Regime Length (yrs):',np.std(tlpN))
print('Medi TLpi Regime Length (yrs):',np.median(tlpN))
print('25th TLpi Regime Length (yrs):',np.quantile(tlpN,0.25))
print('75th TLpi Regime Length (yrs):',np.quantile(tlpN,0.75))
print('========================================')
print('Mean Chao Regime Length (yrs):',np.mean(chaN))
print('StdDev Chao Regime Length (yrs):',np.std(chaN))
print('Medi Chao Regime Length (yrs):',np.median(chaN))
print('25th Chao Regime Length (yrs):',np.quantile(chaN,0.25))
print('75th Chao Regime Length (yrs):',np.quantile(chaN,0.75))
print('========================================')

quasiR=[]

regSort=np.sort(np.concatenate((spinN,tlzN,tlpN,chaN)))
total=np.sum(regSort)
quasi=0.0
for i in range(np.max(np.where(regSort < 900))+1,len(regSort)-1):
  quasi=quasi+regSort[i]
quasiR.append(quasi/total*100)

quasiR=np.array(quasiR)

print('========================================')
print('Quasi Perc. (yrs):',quasiR)
print('========================================')

print('Plotting...')


b=10	#b=10 is normal

regSort=regSort[np.where(regSort>0.0)]
logbins = np.logspace(np.log10(np.min(regSort))/np.log10(b),np.log10(np.max(regSort))/np.log10(b),40)
logxR = (logbins[np.arange(1,len(logbins))]+logbins[np.arange(len(logbins)-1)])/2.
logxR1=logxR

binLx=np.zeros(2*len(logbins))
binLy=np.zeros(2*len(logbins))

for i in range(0,len(binLx)):
  binLx[i]=logbins[int(i/2)]

for i in range(0,int(len(binLx)/4)):
  binLy[4*i]=0.0001
  binLy[4*i+1]=100000
  binLy[4*i+2]=100000
  binLy[4*i+3]=0.0001

#print(binLx)
#print(binLy)

cutB=15		#11,20   15 is Main cutoff
cutT=len(logxR)		#29,58

tlpH=np.histogram(tlpN,logbins)
tlpH=tlpH[0]
logxR=logxR[np.arange(cutB,cutT)]	#2,19
tlpH=tlpH[np.arange(cutB,cutT)]
logxP=logxR[np.where(tlpH>0.0)]
tlpH=tlpH[np.where(tlpH>0.0)]

tlzH=np.histogram(tlzN,logbins)
tlzH=tlzH[0]
tlzH=tlzH[np.arange(cutB,cutT)]
logxZ=logxR[np.where(tlzH>0.0)]
tlzH=tlzH[np.where(tlzH>0.0)]

spinH=np.histogram(spinN,logbins)
spinH=spinH[0]
spinH=spinH[np.arange(cutB,cutT)]
logxS=logxR[np.where(spinH>0.0)]
spinH=spinH[np.where(spinH>0.0)]

target_func = func_powerlaw
poptP, pcovP = curve_fit(func_powerlaw, logxP, tlpH,maxfev=2000,sigma=np.sqrt(tlpH), p0 = np.asarray([-1,10**5]))
poptZ, pcovZ = curve_fit(func_powerlaw, logxZ, tlzH,maxfev=2000,sigma=np.sqrt(tlzH), p0 = np.asarray([-1,10**5]))
poptS, pcovS = curve_fit(func_powerlaw, logxS, spinH,maxfev=2000,sigma=np.sqrt(spinH), p0 = np.asarray([-1,10**5]))

perrP=np.sqrt(np.diag(pcovP))
perrZ=np.sqrt(np.diag(pcovZ))
perrS=np.sqrt(np.diag(pcovS))

print('=======  Pi Fit======= m,a')
print(poptP)
#print(pcovP)
print(perrP)
print('=======Zero Fit======= m,a')
print(poptZ)
#print(pcovZ)
print(perrZ)
print('=======Spin Fit======= m,a')
print(poptS)
#print(pcovS)
print(perrS)

myfont=14

fig, axs = plt.subplots(1,1)

ax=axs

ax.hist([chaN,tlpN,tlzN,spinN],bins=logbins,linewidth=0.5,ec='k',color=['red','whitesmoke','dimgray','black'],label=['PTB','T.L. Pi','T.L. Zero','Spinning'])
#ax.scatter(logxR,tlpH)
ax.plot(logxR1, target_func(logxR1, *poptP), lw=0.0,marker='o',color='whitesmoke',markersize=3,markeredgewidth=0.5,markeredgecolor='black',label=r'T.L. Pi fit:      $a=%4.0f \pm %3.0f$, $m=%5.2f \pm %5.2f$' % tuple([poptP[1],perrP[1],poptP[0],perrP[0]]))
#ax.plot(logxR,target_func(logxR, poptP[0]+perrP[0],poptP[1]+perrP[1]))
#ax.plot(logxR,target_func(logxR, poptP[0]-perrP[0],poptP[1]-perrP[1]))
ax.plot(logxR1, target_func(logxR1, *poptZ), '-',color='dimgray',label=r'T.L. Zero fit: $a=%4.0f \pm %3.0f$, $m=%5.2f \pm %5.2f$' % tuple([poptZ[1],perrZ[1],poptZ[0],perrZ[0]]))
ax.plot(logxR1, target_func(logxR1, *poptS), '--',color='black',label=r'Spinning fit: $a=%4.0f \pm %3.0f$, $m=%5.2f \pm %5.2f$' % tuple([poptS[1],perrS[1],poptS[0],perrS[0]]))

ax.plot(binLx,binLy,ls='dotted')

samplecolor='lightcyan'	#whitesmoke
ax.fill_between([logbins[cutB],logbins[cutB],logbins[cutT],logbins[cutT]],[0.0001,100000,100000,0.0001],color=samplecolor,edgecolor=samplecolor)

(lines, labels) = plt.gca().get_legend_handles_labels()
lines.insert(0, plt.Line2D(logxR1, target_func(logxR1, *poptS), linestyle='none'))
labels.insert(0,r'f(x)=$ax^m$')

ax.set_ylim(0.6,40000)
ax.set_xlim(0.15,400000)
#ax.set_xticks(np.arange(0,top+200,200))
#ax.set_xticks(np.arange(0,top,binw),minor=True)

ax.set_ylabel('Occurrences',fontsize=20)
ax.set_xlabel('Regime Length (yrs)',fontsize=20)
ax.set_yscale('log')
ax.set_xscale('log')
#ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
ax.tick_params(axis="y", left=True, right=True, labelleft=True, labelright=False)

ax.tick_params(axis='both', which='major',labelsize=myfont)

#ax.set_xticks(np.array([22000,42000,62000,82000,102000,122000,142000,162000,182000]))
#ax.set_xticks(np.arange(2000,182000,5000),minor=True)
#ax.set_xticklabels(['22k','42k','62k','82k','102k','122k','142k','162k','182k'])
#ax.xaxis.set_label_coords(0, -0.06)
"""
widleg=8
widline=0.5
leg=[Line2D([0], [0], marker='s', ls='',markeredgewidth=widline, markerfacecolor='black', color='k', markersize=widleg, label='Spinning'),
	Line2D([0], [0], marker='s', ls='',markeredgewidth=widline, markerfacecolor='dimgray', color='k', markersize=widleg, label='T.L. Zero'),
	Line2D([0], [0], marker='s', ls='',markeredgewidth=widline, markerfacecolor='whitesmoke', color='k', markersize=widleg, label='T.L. Pi'),
	Line2D([0], [0], marker='s', ls='',markeredgewidth=widline, markerfacecolor='red', color='k', markersize=widleg, label='PTB')]

ax.legend(handles=leg)
"""
ax.legend(lines,labels,ncol=2,handleheight=2.4)
fig.subplots_adjust(wspace=0, hspace=0)
plt.show()


savefile='regimeHistFIT40funcMain.pdf'
fig.savefig(savefile,bbox_inches='tight')