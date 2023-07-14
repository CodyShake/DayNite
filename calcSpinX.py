import numpy as np
from scipy import interpolate
import time
import sys



def f(t, y, eps):
    f=np.zeros(2)
    Enew = interpolate.splev(t, tck, der=0)		#EValutuate the ecc spline f'n at this point
    Nnew = interpolate.splev(t, tck2, der=0)		#EValutuate the MM spline f'n at this point
    Nder = interpolate.splev(t, tck2, der=1)		#EValutuate the MM spline f'n deriv. here
    ws=3*Nnew*Nnew*1e-5*abs(1.0-5*Enew*Enew/2+13*Enew*Enew*Enew*Enew/16)    #p=1, Goldreich & Peale, 1966	
							#'ws^2' power series of ecc ** was 1+e+e^+e^3
    f[0]=y[1]						#gamma dot
    f[1]=-(0.5*ws*np.sin(2*y[0])+Nder+eps*y[1])		#gamma ddot
    return f

			#I think this is appropriate since gamma (y[0]) is the only unknown

def rk4(t, h, y):
    k1 = np.zeros(2)
    k2 = np.zeros(2)
    k3 = np.zeros(2)
    k4 = np.zeros(2)
    k1=h*f(t,y,eps)
    k2=h*f(t+0.5*h,y+0.5*k1,eps)
    k3=h*f(t+0.5*h,y+0.5*k2,eps)
    k4=h*f(t+h,y+k3,eps)          
    y+=(k1+2*k2+2*k3+k4)/6.
    return y

start_time = time.time()

sys.path.append('../')
simID=int(sys.argv[1])

x=4-2
			#This looks at planet X which is 2,3,4, or 5 (minus 2 because 2 is first/0)

dir='/home/cjshake/Rebound/'
file='final{0}mme'.format(simID)
filename=file+str(x+2)+".npy"
print(filename)
data = np.load(dir+filename)
#data = np.load("final169mmeMED.npy")
#data = np.load("final169mmeMED_S.npy")
#data = np.load("final169mmeSMALL.npy")

data = np.array(data)					#This will eventually need to be narrowed for 

							# the specific planet being spinCalced.
print('Total loaded size:')
print(data.size)

#I want the stuff below to do it by itself

Nout=10000000
#Nout=100000
#Nout=30000
#Nout=2000					#4.268968408381913 is the period of planet3 ('d') at start

Nsp=10000		#length of cubic spline interpolation

ind=np.arange(0,10*Nsp,1)
#P=np.array([2.54523629287309,4.268968408381913,6.456926008213765,9.736325599838025])

							#CALC INITIAL TIMES
eX=data[0]
nX=data[1]
P=data[2]
mass=data[3]
semi=data[4]
start=data[5]

times= np.linspace(start,start+P*Nout,10*Nout) #This h needs to change with planet

#print('---Times---')
#print(times[10*Nsp-1]-times[0])
#print(times[10*Nsp-10]-times[0])
#print('---Times---')

print('Input variable sizes:')
print(times.size)
print(eX.size)
print('Period:',P)
print('Mass:',mass)
print('Semi:',semi)
print('Start Time:',start)

Tsp=times[ind]							#GET SPLINE TIMES
							#CALC INITIAL SPLINES
tck = interpolate.splrep(Tsp, eX[ind], s=0)		#calc the spline function for ecc
tck2 = interpolate.splrep(Tsp, nX[ind], s=0)		#calc the spline function for mean motion

print("Interpolated Successfully!")
print("--- %s seconds ---" % (time.time() - start_time))


					#Things to try: -Q=100 (unlikely)
					#		-Do small interpolations (that overlap a few
					#		 points to be identical on evaluated points.)
					#		 How do I make a loop do this? (for faster int.) DID THIS! :)
					#		-I assume "a" is const., it varies though and I
					#		 should incude that in the future. (so save 
					#		 'a' during simSA and calc eps in 'def f()').
					#		 This requires another spline though so maybe not.

G=0.497912832			#m^3/kg/day^2
ms=0.08*2.e30

mass=mass*2.e30		#kg
semi=semi*1.496e11	#meters
Rad=np.array([1.056,0.772,0.918,1.045])	#Gillon et al. 2017
Rad=Rad*6378000.	#meters

#Changes with planet
mp=mass
a=semi
R=Rad[x]
h=P*0.1	

Q=100
Om=2*np.pi			#rad/day

sig=G/(2*Q*Om*R**5)
eps=(15*ms)/(2*mp)*(R/a)**6*ms*R**2*sig

y=[0.0*np.pi,0.]			#initial substeller, initial spin rate
#h=0.4268968408381913			#dt=0.42*day for RK4 integration (slightly less than 10%, i.e. 
					#the sampling rate used in simSA.py and by Vinson et al. 2019.
tend=times[10*Nout-1]
t=times[0]

tr,yr,dyr = [],[],[]

c=1
i=0
print("--- %s seconds ---" % (time.time() - start_time))


while(t<tend):
    if((t+h)>tend):
        h=tend-t
    y = rk4(t,h,y)
    t = t+h
    if (i+1) % 100 == 0:
#        yr[i] = y[0]
#        dyr[i] = y[1]
#        tr[i] = t
        yr.append(y[0])
        dyr.append(y[1])
        tr.append(t)
#    if (i+1) % 10000 == 0:
#        print("i = ",i)
#        print("--- %s seconds ---" % (time.time() - start_time))
    if (i+1) % (10*Nsp-100) == 0:
        NspT=(10*Nsp)+1					#NspT is the size of the next chunk
        if(((10*Nsp-100)*(c+1))>10*Nout):		# Added '+1' because +10 is actually +0-9 (i.e. 10 new points but ends at 9)
            NspT=10*Nout-(10*Nsp-100)*c
        print("New Spline: i=",i,', c=',c)
        print("--- %s seconds ---" % (time.time() - start_time))
#        ind=np.arange(ind[(len(ind)-10)-1],ind[len(ind)-1]+NspT,1)
        ind=np.arange(i-100,i+NspT,1)
#        print('ind size= ',ind.size)
#        print(ind[0],' / ',ind[len(ind)-1])
#        print('First time= ',times[ind[0]],', Last= ',times[ind[len(ind)-1]])
#        print('Current time= ',t)
        Tsp= times[ind]
        tck = interpolate.splrep(Tsp, eX[ind], s=0)			#calc the splines for next chunk
        tck2 = interpolate.splrep(Tsp, nX[ind], s=0)
        c=c+1

    i=i+1

yr=np.array(yr)
dyr=np.array(dyr)
tr=np.array(tr)

print("--- %s seconds ---" % (time.time() - start_time))

#savefilename = dir+'spin{0}p'.format(simID)+str(x+2)+'.npy'
savefilename = dir+'spin{0}p'.format(simID)+str(x+2)+'q100.npy'

#savefilename = 'spin169MED_newNEW100.npy'
#savefilename = 'spin169MED_SnewNEW.npy'
#savefilename = 'spin169SMALL.npy'
np.save(savefilename,np.array([yr,dyr,tr]))
