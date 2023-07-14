import numpy as np
import matplotlib.pyplot as plt

name='4'
simnum='169'
q='q100'
filename='regData'+simnum+'p'+name+q+'.npy'

data = np.load(filename,allow_pickle=True)
regR=np.array(data[0])
regTLz=np.array(data[1])
regTLp=np.array(data[2])
chaR=np.array(data[3])


regN=np.zeros(int(len(regR)/2))
regTLzN=np.zeros(int(len(regTLz)/2))
regTLpN=np.zeros(int(len(regTLp)/2))
chaN=np.zeros(int(len(chaR)/2))

print('Length  regN:',len(regN))

for i in range(0,int(len(regR)/2)):
  regN[i]=regR[2*i+1]-regR[2*i]

for i in range(0,int(len(regTLz)/2)):
  regTLzN[i]=regTLz[2*i+1]-regTLz[2*i]

for i in range(0,int(len(regTLp)/2)):
  regTLpN[i]=regTLp[2*i+1]-regTLp[2*i]

for i in range(0,int(len(chaR)/2)):
  chaN[i]=chaR[2*i+1]-chaR[2*i]


yr=np.zeros(len(regN))
yr=yr+1


#chaot=0.0
short=0.0
medi=0.0
long=0.0
quasi=0.0

regSort=np.sort(np.concatenate((regN,regTLzN,regTLpN,chaN)))
print('Total med/mean:')
print(np.median(regSort))
print(np.mean(regSort))
total=np.sum(np.concatenate((regN,regTLzN,regTLpN)))

#for i in range(0,np.max(np.where(regSort < 10))):
#  chaot=chaot+regSort[i]

for i in range(0,np.max(np.where(regSort < 100))):
  short=short+regSort[i]

for i in range(np.max(np.where(regSort < 100))+1,np.max(np.where(regSort < 500))):
  medi=medi+regSort[i]

for i in range(np.max(np.where(regSort < 500))+1,np.max(np.where(regSort < 900))):
  long=long+regSort[i]

for i in range(np.max(np.where(regSort < 900))+1,len(regSort)-1):
  quasi=quasi+regSort[i]


print('Last Chaotic: ',np.max(np.where(regSort < 10)))	#Chaotic      - <10			
print('Last Short: ',np.max(np.where(regSort < 100)))	#Short	      - [10-100)
print('Last Med: ',np.max(np.where(regSort < 500)))	#Medium       - 100-500
print('Last Long: ',np.max(np.where(regSort < 900)))	#Long	      - [500-900)
print('1st Quasi: ',np.min(np.where(regSort >= 900)))	#Quasi-stable - >=900


print('========================================')
print('Mean Regime Length (yrs):',np.mean(regSort))
print('Medi Regime Length (yrs):',np.median(regSort))
print('========================================')
print('1st Percentile:',np.nanquantile(regSort,0.01))
print('40th Percentile:',np.nanquantile(regSort,0.40))
print('95th Percentile:',np.nanquantile(regSort,0.95))
print('99th Percentile:',np.nanquantile(regSort,0.99))
print('========================================')

print('Plotting...')

"""
quasitxt=r'$\geq$900yrs'

fig, axs = plt.subplots(1,1)
ax=axs
labels = 'Short\n<100yrs', 'Medium\n[100yrs-500yrs)', 'Long\n[500yrs-900yrs)', 'Quasi-Stable\n'+quasitxt
sizes = [short/total*100., medi/total*100., long/total*100., quasi/total*100]
ax.pie(sizes,labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 18})
ax.axis('equal')

plt.show()
savefile='regimePIE'+simnum+'p'+name+q+'v1.svg'
"""
fig, axs = plt.subplots(1,1)
ax=axs
labels = 'Spinning','T.L. Zero', 'T.L. Pi','Chaotic'
sizes = [np.sum(regN)/total*100., np.sum(regTLzN)/total*100., np.sum(regTLpN)/total*100.,np.sum(chaN)/total*100.]
colors = 'dimgray','lightgray','whitesmoke','pink'
ax.pie(sizes,labels=labels,colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 20})
ax.axis('equal')

plt.show()
savefile='regimePIE'+simnum+'p'+name+q+'v2.svg'
#"""

fig.savefig(savefile)