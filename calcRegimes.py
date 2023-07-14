import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append('../')
simID=int(sys.argv[1])

#name='5'
name='5q100'
simnum='{0}'.format(simID)
filename='regime'+simnum+'p'+name+'.npy'
savefile='regData'+simnum+'p'+name+'.npy'

data = np.load(filename,allow_pickle=True)
#print(data.size)

yr=np.array(data[0])
tr=np.array(data[1])
dyr=np.array(data[2])
dtr=np.array(data[3])
yrp=np.array(data[4])
trp=np.array(data[5])

regR=[]
tlpR,tlzR=[],[]		#note regR=spin regime, tlpR=tidally-locked pi, tlzR=tidally-locked zero
chaR=[]

sign=np.zeros((2,4))


i=0

while (i<len(yr)):
#for i in range(len(yr)):
  if (i+5 >=len(yr)): break

  if (abs(yr[i])>=2. and ((abs(yr[i+1])>=2.) and (np.sign(yr[i]) != np.sign(yr[i+1]))) and ((abs(yr[i+2])>=2.) and (np.sign(yr[i+1]) != np.sign(yr[i+2]))) and ((abs(yr[i+3])>=2.) and (np.sign(yr[i+2]) != np.sign(yr[i+3]))) and ((abs(yr[i+4])>=2.) and (np.sign(yr[i+3]) != np.sign(yr[i+4]))) and ((abs(yr[i+5])>=2.) and (np.sign(yr[i+4]) != np.sign(yr[i+5])))):

    sign[0,0]=np.sign(yr[i])
    sign[1,0]=tr[i]

    sign[0,1]=np.sign(yr[i+1])
    sign[1,1]=tr[i+1]

    sign[0,2]=np.sign(yr[i+2])
    sign[1,2]=tr[i+2]

    sign[0,3]=np.sign(yr[i+3])
    sign[1,3]=tr[i+3]
    regR.append(sign[1,0])
    i+=4
    if (i>=len(yr)):
      regR.append(sign[1,3])
      break
    while ((abs(yr[i])>=2.) and (sign[0,3] != np.sign(yr[i]))):
      sign[0,3]=np.sign(yr[i])              
      sign[1,3]=tr[i]
      i+=1
      if (i>=len(yr)): break
    regR.append(sign[1,3])

  elif ((abs(yr[i])<=2.0) and (abs(yr[i+1])<=2.0) and (abs(yr[i+2])<=2.0) and ((abs(yr[i+3])<=2.0) and (abs(yr[i+4])<=2.0) and (abs(yr[i+5])<=2.0))):

    sign[0,0]=np.sign(yr[i])
    sign[1,0]=tr[i]

    sign[0,1]=np.sign(yr[i+1])
    sign[1,1]=tr[i+1]

    sign[0,2]=np.sign(yr[i+2])
    sign[1,2]=tr[i+2]

    sign[0,3]=np.sign(yr[i+3])
    sign[1,3]=tr[i+3]
    tlzR.append(sign[1,0])
    i+=4
    if (i>=len(yr)):
      tlzR.append(sign[1,3])
      break
    while ((abs(yr[i])<=2.0)):	# and (sign[0,3] != np.sign(yr[i]))
      sign[0,3]=np.sign(yr[i])              
      sign[1,3]=tr[i]
      i+=1
      if (i>=len(yr)): break
    tlzR.append(sign[1,3])

  else:
    i+=1
  if (i>=len(yr)): break


######################################################################## pi regime

i=0

while (i<len(yrp)):
#for i in range(len(yrp)):
  if (i+5 >=len(yrp)): break

  if ((abs(yrp[i])>=np.pi-2. and abs(yrp[i])<=np.pi+2.) and (abs(yrp[i+1])>=np.pi-2. and abs(yrp[i+1])<=np.pi+2.) and (abs(yrp[i+2])>=np.pi-2. and abs(yrp[i+2])<=np.pi+2.) and (abs(yrp[i+3])>=np.pi-2. and abs(yrp[i+3])<=np.pi+2.) and (abs(yrp[i+4])>=np.pi-2. and abs(yrp[i+4])<=np.pi+2.) and (abs(yrp[i+5])>=np.pi-2. and abs(yrp[i+5])<=np.pi+2.)):
    sign[0,0]=np.sign(yrp[i])
    sign[1,0]=trp[i]

    sign[0,1]=np.sign(yrp[i+1])
    sign[1,1]=trp[i+1]

    sign[0,2]=np.sign(yrp[i+2])
    sign[1,2]=trp[i+2]

    sign[0,3]=np.sign(yrp[i+3])
    sign[1,3]=trp[i+3]
    tlpR.append(sign[1,0])
    i+=4
    if (i>=len(yrp)):
      tlpR.append(sign[1,3])
      break
    
    while (abs(yrp[i])>=np.pi-2. and abs(yrp[i])<=np.pi+2.):
      sign[0,3]=np.sign(yrp[i])              
      sign[1,3]=trp[i]
      i+=1
      if (i>=len(yrp)): break

    tlpR.append(sign[1,3])


  else:
    i+=1
  if (i>=len(yrp)): break

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO tidally-locked zero

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO tidally-locked pi stitch (useless now?)
"""
j=0

while ((j+1)<=(len(tlpR)-1)):
  if ((tlpR[j+1]-tlpR[j])<=2.0):
    tlpR=np.delete(tlpR,[j,j+1],None)
    j=j-1
  j+=1
"""
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO In-between calc (chaotic)

regR=np.array(regR)
tlzR=np.array(tlzR)
tlpR=np.array(tlpR)

oddS=np.arange(1,int(len(regR)/2)+1)*2-1
oddP=np.arange(1,int(len(tlpR)/2)+1)*2-1
oddZ=np.arange(1,int(len(tlzR)/2)+1)*2-1

evenS=np.arange(0,int(len(regR)/2))*2
evenP=np.arange(0,int(len(tlpR)/2))*2
evenZ=np.arange(0,int(len(tlzR)/2))*2

prioZ=np.zeros(int(len(tlzR)/2))
prioZ=prioZ+2

if (len(regR)>1):
  order=np.array([np.concatenate((regR[evenS],tlpR[evenP],tlzR[evenZ])),np.concatenate((regR[oddS],tlpR[oddP],tlzR[oddZ])),np.concatenate((np.ones(int(len(regR)/2)),np.zeros(int(len(tlpR)/2)),prioZ))])
  print(order.shape)
  inds=order[0].argsort()
  print(inds.shape)
  order[0]=order[0,inds]
  order[1]=order[1,inds]
  order[2]=order[2,inds]

  delidx=[]
  minreg=10.0

  for i in range(0,len(order[0])):		#remove regimes <minreg (yr) (they will be chaotic)
    if (order[1,i]-order[0,i]<minreg):
      delidx.append(i)

  delidx=np.array(delidx)
  order=np.delete(order,delidx,1)
  
  for i in range(0,len(order[0])-1):		#trim overlapping regimes based off priority
    if (order[1,i]>order[0,i+1]):
      print('###Overlap###',order[2,i],order[2,i+1])
      if (order[2,i]<order[2,i+1]):
        order[0,i+1]=order[1,i]
      else:
        order[1,i]=order[0,i+1]

  delidx=[]

  for i in range(0,len(order[0])):		#remove smaller regimes again because of trimming
    if (order[1,i]-order[0,i]<minreg):
      delidx.append(i)

  delidx=np.array(delidx)

  if (len(delidx)>0):
    order=np.delete(order,delidx,1)

  for i in range(0,len(order[0])-1):		#anything >0.2 between regimes is chaotic
    if (order[1,i]<(order[0,i+1]-0.2)):
      chaR.append(order[1,i])
      chaR.append(order[0,i+1])
  chaR=np.array(chaR)

  regR=np.sort(np.concatenate((order[0,np.where(order[2]==1)],order[1,np.where(order[2]==1)]),axis=None))
  tlpR=np.sort(np.concatenate((order[0,np.where(order[2]==0)],order[1,np.where(order[2]==0)]),axis=None))
  tlzR=np.sort(np.concatenate((order[0,np.where(order[2]==2)],order[1,np.where(order[2]==2)]),axis=None))

chaR=np.array(chaR)
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO Regime Length Calc

spinN=np.zeros(int(len(regR)/2))
tlzN=np.zeros(int(len(tlzR)/2))
tlpN=np.zeros(int(len(tlpR)/2))
chaN=np.zeros(int(len(chaR)/2))


for i in range(0,int(len(regR)/2)):
  spinN[i]=regR[2*i+1]-regR[2*i]
for i in range(0,int(len(tlzR)/2)):
  tlzN[i]=tlzR[2*i+1]-tlzR[2*i]
for i in range(0,int(len(tlpR)/2)):
  tlpN[i]=tlpR[2*i+1]-tlpR[2*i]
for i in range(0,int(len(chaR)/2)):
  chaN[i]=chaR[2*i+1]-chaR[2*i]

"""
print('========================================')
print('Mean Spin Regime Length (yrs):',np.mean(spinN))
print('Medi Spin Regime Length (yrs):',np.median(spinN))
print('========================================')
print('========================================')
print('Mean TL0 Regime Length (yrs):',np.mean(tlzN))
print('Medi TL0 Regime Length (yrs):',np.median(tlzN))
print('========================================')
print('========================================')
print('Mean TLpi Regime Length (yrs):',np.mean(tlpN))
print('Medi TLpi Regime Length (yrs):',np.median(tlpN))
"""
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO Copypasta
print('===================CopypastaREGIME',simnum,'p',name,'=====================')
if (len(spinN)>=1):
  print(np.mean(spinN))
  print(np.std(spinN))
  print(np.median(spinN))
  print(np.quantile(spinN,0.25))
  print(np.quantile(spinN,0.75))
  print(np.min(spinN))
  print(np.max(spinN))
else:
  print('!!!No spin!!!')
if (len(tlzN)>=1):
  print(np.mean(tlzN))
  print(np.std(tlzN))
  print(np.median(tlzN))
  print(np.quantile(tlzN,0.25))
  print(np.quantile(tlzN,0.75))
  print(np.min(tlzN))
  print(np.max(tlzN))
else:
  print('!!!No TL 0!!!')
if (len(tlpN)>=1):
  print(np.mean(tlpN))
  print(np.std(tlpN))
  print(np.median(tlpN))
  print(np.quantile(tlpN,0.25))
  print(np.quantile(tlpN,0.75))
  print(np.min(tlpN))
  print(np.max(tlpN))
else:
  print('!!!No TL 3.14!!!')
if (len(chaN)>=1):
  print(np.mean(chaN))
  print(np.std(chaN))
  print(np.median(chaN))
  print(np.quantile(chaN,0.25))
  print(np.quantile(chaN,0.75))
  print(np.min(chaN))
  print(np.max(chaN))
else:
  print('!!!No Chaotic!!!')
#"""

#OOOOOOOOOOO saving



index=np.arange(30)
#print(tlpR[index])
#print(regR.size,tlzR.size,tlpR.size)

np.save(savefile,np.array([regR,tlzR,tlpR,chaR]))



