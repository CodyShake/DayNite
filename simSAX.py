import rebound
import reboundx
import numpy as np
import sys

sys.path.append('../')
simID=int(sys.argv[1])

x=5
			#This looks at planet X which is 2,3,4, or 5
dir='/home/cjshake/Rebound/'
file="SAfinal{0}.bin".format(simID)
savefile="final{0}mme".format(simID)+str(x)+".npy" #Mean Motion Eccentricity

print(x,file)

sim = rebound.Simulation(dir+file)

Nout=10000000
ps = sim.particles
pmax=20.

times= np.linspace(sim.t,sim.t+ps[x].P*Nout,10*Nout)	#ps[3].P=4.268968408381913 (days)

print("Time after loading simulation %.1f" %sim.t) 	#returns 91300000.0 (days)

eX,nX = np.zeros(len(times)),np.zeros(len(times))
Period=ps[x].P
Mass=ps[x].m
Semi=ps[x].a
StartT=sim.t

for i, time in enumerate(times):
  sim.integrate(time, exact_finish_time=0)
  eX[i] = ps[x].e
  nX[i] = ps[x].n
  if ps[1].e < 0. or ps[1].e > 0.999 or ps[2].e < 0. or ps[2].e > 0.999 or ps[3].e < 0. or ps[3].e > 0.999 or ps[4].e < 0. or ps[4].e > 0.999 or  ps[5].e < 0. or ps[5].e > 0.999 or ps[6].e < 0. or ps[6].e > 0.999 or  ps[1].P < 0. or ps[1].P > pmax or ps[2].P < 0. or ps[2].P > pmax or ps[3].P < 0. or ps[3].P > pmax or ps[4].P < 0. or ps[4].P > pmax or ps[5].P < 0. or ps[5].P > pmax or ps[6].P < 0. or ps[6].P > pmax:
    print("Went Unstable at: %.1f" %sim.t)
    exit()

print("Time after sim %.1f" %sim.t)

data=np.array([np.array(eX),np.array(nX),Period,Mass,Semi,StartT])
np.save(dir+savefile,data)
