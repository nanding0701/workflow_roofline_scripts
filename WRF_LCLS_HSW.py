import numpy as np
import matplotlib.pyplot as plt
import sys
import math

font = { 'size'   : 20}
plt.rc('font', **font)


colors = ['k','g','darkred','magenta','m','red','c']
styles = ['o','s','v','^','D',">","<","*","h","H","+","1","2","3","4","8","p","d","|","_",".",","]

fig = plt.figure(1,figsize=(8,6))
plt.clf()
ax = fig.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Number of Parallel Tasks')
ax.set_ylabel('Throughput [#tasks/sec]')


########################### SYSTEM INPUTS ###########################
PEAK_NODE_CPU_BW=129 # in GB/s
RANKS_PER_NODE=32
PEAK_FILE_SYSTEM=6.5*140
GOOD_DAYS=1 ## GB/s
BAD_DAYS=0.2  ## GB/s
CPU_HARDWARE=2388
#####################################################################

########################### WORKFLOW INPUTS ###########################
TOTAL_TASKS=6
PARALLEL_TASKS=5
RANKS_USED=1024 # MPI ranks
FILE_SYSTEM_VOL=1000  # GB
GOOD_DAYS_TIME=1024 ## sec
BAD_DAYS_TIME=5120 ## sec
TARGET_MAKESPAN=10*60
########################### INPUTS ENDS ###########################




nx = 1000
xmin = -4
xmax = 4
ymin = 0.0001
ymax = 10

scalingFactorForRoofs=1

ax.set_xlim(10**xmin, 10**xmax)
ax.set_ylim(ymin, ymax)

ixx = int(nx*0.02)
xlim = ax.get_xlim()
ylim = ax.get_ylim()

scomp_x_elbow = []
scomp_ix_elbow = []
smem_x_elbow = []
smem_ix_elbow = []

x = np.logspace(xmin,xmax,nx)
y=x/(TARGET_MAKESPAN)
ax.plot(x,y,ls='--',c='k')
plt.axhline(y = TOTAL_TASKS/(TARGET_MAKESPAN) , color = 'k',ls='--')


system_plot=1
if system_plot==1:
    achieved_bandwidth=[((RANKS_USED/RANKS_PER_NODE)/(PEAK_NODE_CPU_BW))]
    smemroofs=[]
    scomproofs=[]
    scomp_x_elbow=[]
    scomp_ix_elbow=[]


    PARA_LIMIT=math.floor(CPU_HARDWARE/(RANKS_USED/RANKS_PER_NODE))


    for ab in range(0,len(achieved_bandwidth)):
        smemroofs=[]
        scomproofs=[]
        scomp_x_elbow=[]
        scomp_ix_elbow=[]
        smem_x_elbow=[]
        smem_ix_elbow=[]


        smemroofs.append(achieved_bandwidth[ab])

        scomproofs.append(TOTAL_TASKS/((PARALLEL_TASKS*FILE_SYSTEM_VOL)/(PEAK_FILE_SYSTEM)))
        scomproofs.append(TOTAL_TASKS/(FILE_SYSTEM_VOL/(GOOD_DAYS)))
        scomproofs.append(TOTAL_TASKS/(FILE_SYSTEM_VOL/(BAD_DAYS)))



        for roof in scomproofs:
            for ix in range(1,nx):
                if (x[ix])/smemroofs[0] >= roof and (x[ix-1])/smemroofs[0] < roof:
                    scomp_x_elbow.append(x[ix-1])
                    scomp_ix_elbow.append(ix-1)
                    break
        #print(scomp_x_elbow)
        #print(roof)
        #print(smemroofs[0])

        for roof in smemroofs:
            for ix in range(1,nx):
                if (scomproofs[0] <= (x[ix])/roof) and (scomproofs[0] > ( x[ix-1])/roof):
                    #if (MEM_NODE/roof <= (x[ix])/roof) and (MEM_NODE/roof > ( x[ix-1])/roof):
                    smem_x_elbow.append(x[ix-1])
                    smem_ix_elbow.append(ix-1)
                    break
            #print(scomp_x_elbow)

        for i in range(0,len(scomproofs)):
            roof = scomproofs[i]
            y = np.ones(len(x)) * roof / scalingFactorForRoofs
            ax.plot(x[scomp_ix_elbow[i]:],y[scomp_ix_elbow[i]:],c=colors[i],ls='-',lw='2')

        for i in range(0,len(smemroofs)):
            roof = smemroofs[i]
            y = ((x)/roof) / scalingFactorForRoofs
            ax.plot(x[:smem_ix_elbow[i]+1],y[:smem_ix_elbow[i]+1],c=colors[ab],ls='-',lw='2')



para_plot=1
if para_plot==1:
    plt.vlines(x = PARA_LIMIT, ymin = ymin, ymax =scomproofs[0] ,color='k',ls='-',lw=2)


ax.plot(TOTAL_TASKS,TOTAL_TASKS/(GOOD_DAYS_TIME),c='green',marker='o',markersize=10)
ax.plot(TOTAL_TASKS,TOTAL_TASKS/(BAD_DAYS_TIME),c='darkred',marker='o',markersize=10)

ax.grid(True)
marker_handles = list()
#plt.show()
plt.savefig('WRF_LCLS_HSW.pdf')

