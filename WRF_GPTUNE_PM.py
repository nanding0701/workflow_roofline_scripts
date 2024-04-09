import numpy as np
import matplotlib.pyplot as plt
import sys




########################### SYSTEM INPUTS ###########################
CPU_HARDWARE=3072
PEAK_NODE_CPU_BW=204.8*2# in GB/s
RANKS_PER_NODE=128
PEAK_FILE_SYSTEM=4800 # GB/s
#####################################################################


########################### META DATA ###########################
time=[553,227.9,19.08] #batch, RCI, projected
#####################################################################

########################### WORKFLOW INPUTS ###########################
TOTAL_TASKS=1
PARALLEL_TASKS=1
NNZ=(135654*8)/1e3
FILE_VOL=128
ITER=40
########################### INPUTS ENDS ###########################
font = { 'size'   : 15}
plt.rc('font', **font)

colors = ['k','blue','red','green','m','c','y','k','crimson']
styles = ['o','s','D','v','^',">","<","*","h","H","+","1","2","3","4","8","p","d","|","_",".",","]

fig = plt.figure(1,figsize=(8,8))
plt.clf()
ax = fig.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Number of Parallel Tasks')
ax.set_ylabel('Throughput [#tasks/sec]')
nx = 1000
xmin = -2
xmax = 4
ymin = 0.001
ymax = 1000000
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

ax.plot(TOTAL_TASKS, 1/time[0],c='darkred',marker='o',markersize=10)
ax.plot(TOTAL_TASKS, 1/time[1],c='darkred',marker='o',markersize=10)
ax.plot(TOTAL_TASKS, 1/time[2],markeredgecolor='darkred',marker='o',markerfacecolor="None",lw=2,markersize=10)

system_plot=1
if system_plot==1:
    smemroofs=[]
    scomproofs=[]
    scomp_x_elbow=[]
    scomp_ix_elbow=[]


    PARA_LIMIT=CPU_HARDWARE/1

    for ab in range(0,len(time)):
        smemroofs=[]
        scomproofs=[]
        scomp_x_elbow=[]
        scomp_ix_elbow=[]
        smem_x_elbow=[]
        smem_ix_elbow=[]

        ## node KB RCI ####
        data_tot=((FILE_VOL+NNZ))/1e6+835/1e3 ## make it GB
        latency=(data_tot/(208.4/4))
        smemroofs.append(latency)

        scomproofs.append(1/(( ITER*((NNZ)/1e6) )/(PEAK_FILE_SYSTEM))  )
        scomproofs.append( 1/( (ITER*((FILE_VOL+NNZ)/1e6) )/PEAK_FILE_SYSTEM) )

        for roof in scomproofs:
            for ix in range(1,nx):
                if (x[ix])/smemroofs[0] >= roof and (x[ix-1])/smemroofs[0] < roof:
                    scomp_x_elbow.append(x[ix-1])
                    scomp_ix_elbow.append(ix-1)
                    break

        for roof in smemroofs:
            for ix in range(1,nx):
                if (scomproofs[0] <= (x[ix])/roof) and (scomproofs[0] > ( x[ix-1])/roof):
                    smem_x_elbow.append(x[ix-1])
                    smem_ix_elbow.append(ix-1)
                    break

        for i in range(0,len(scomproofs)):
            roof = scomproofs[i]
            y = np.ones(len(x)) * roof / scalingFactorForRoofs
            ax.plot(x[scomp_ix_elbow[i]:],y[scomp_ix_elbow[i]:],c='k',ls='-',lw='2')

        for i in range(0,len(smemroofs)):
            roof = smemroofs[i]
            y = ((x)/roof) / scalingFactorForRoofs
            ax.plot(x[:smem_ix_elbow[i]+1],y[:smem_ix_elbow[i]+1],c=colors[i],ls='-',lw='2')



para_plot=1
if para_plot==1:
    plt.vlines(x = PARA_LIMIT, ymin = ymin, ymax = ymax,color='k',ls='-',lw=2)




ax.grid(True)
marker_handles = list()

plt.savefig('WRF_GPTUNE_PM.pdf')
