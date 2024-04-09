import numpy as np
import matplotlib.pyplot as plt
import sys
import math



########################### SYSTEM INPUTS ###########################
GPU_HARDWARE=(1536+256)
PEAK_NODE_CPU_BW=1555*4# in GB/s
RANKS_PER_NODE=4
PEAK_FILE_SYSTEM=5600
GPU_NODE_FLOPS=4*9.7
#####################################################################


########################### META DATA ###########################
time1=[1096.50, 344.32, 179.56]
time2=[3088.36, 775.56, 225.18]
tflop1=1164*1000
tflop2=12.6*256*1000
batches=[80,20,5]
memory1_per_gpu=[(45.1*1024)/16,(45.1*1024)/16,(45.1*1024)/16,(45.1*1024)/16,(45.1*1024)/16]
memory2_per_gpu=[(133.8)/16,(133.8)/16,(133.8)/16,(133.8)/16,(133.8)/16]
mpi_vol1_per_batch=85.3
mpi_vol2_per_batch=48.5
#####################################################################

########################### WORKFLOW INPUTS ###########################
TOTAL_TASKS=2
PARALLEL_TASKS=1
RANKS_USED=1024 # MPI ranks

FILE_SYSTEM_VOL=70  # GB
NODE_FLOPS=(tflop1+tflop2)/RANKS_USED
NETWORK_VOL=(85.3*5+48.5*5)/16  # (vol_per_batch * #batch )/16
TIME=179.56+225.18
TPS=TOTAL_TASKS/TIME
########################### INPUTS ENDS ###########################


font = { 'size'   : 15}
plt.rc('font', **font)


colors = ['k','k','green','k','c','y','k','crimson']
styles = ['o','s','D','v','^',">","<","*","h","H","+","1","2","3","4","8","p","d","|","_",".",","]

fig = plt.figure(1,figsize=(8,8))
plt.clf()
ax = fig.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Task parallelism')
ax.set_ylabel('Throughput [#tasks/sec]')
nx = 1000
xmin = -1
xmax = 6
ymin = 0.0001
ymax = 1000
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

ax.plot(PARALLEL_TASKS,TPS,c='darkred',marker='o',markersize=10)

system_plot=1
if system_plot==1:
    smemroofs=[]
    scomproofs=[]
    scomp_x_elbow=[]
    scomp_ix_elbow=[]

    PARA_LIMIT=math.floor(GPU_HARDWARE/RANKS_USED)


    smemroofs=[]
    scomproofs=[]
    scomp_x_elbow=[]
    scomp_ix_elbow=[]
    smem_x_elbow=[]
    smem_ix_elbow=[]

    ### node flops
    latency=(NODE_FLOPS)/(GPU_NODE_FLOPS*2)
    smemroofs.append(latency)


    ### mpi vol, system
    latency=(NETWORK_VOL)/(25)
    scomproofs.append(TOTAL_TASKS/((FILE_SYSTEM_VOL)/(PEAK_FILE_SYSTEM)))
    scomproofs.append(TOTAL_TASKS/latency)

    for roof in scomproofs:
        for ix in range(1,nx):
            if (x[ix])/smemroofs[0] >= roof and (x[ix-1])/smemroofs[0] < roof:
                scomp_x_elbow.append(x[ix-1])
                scomp_ix_elbow.append(ix-1)
                break

    for roof in smemroofs:
        for ix in range(1,nx):
            if (scomproofs[0] <= (x[ix])/roof) and (scomproofs[0] > ( x[ix-1])/roof):
            #if (MEM_NODE/roof <= (x[ix])/roof) and (MEM_NODE/roof > ( x[ix-1])/roof):
                smem_x_elbow.append(x[ix-1])
                smem_ix_elbow.append(ix-1)
                break

    for i in range(0,len(scomproofs)):
        roof = scomproofs[i]
        y = np.ones(len(x)) * roof / scalingFactorForRoofs
        ax.plot(x[scomp_ix_elbow[i]:],y[scomp_ix_elbow[i]:],c=colors[i],ls='-',lw='2')

    for i in range(0,len(smemroofs)):
        roof = smemroofs[i]
        y = ((x)/roof) / scalingFactorForRoofs
        ax.plot(x[:smem_ix_elbow[i]+1],y[:smem_ix_elbow[i]+1],c='red',ls='-',lw='2')


para_plot=1
if para_plot==1:
    plt.vlines(x = PARA_LIMIT, ymin = ymin, ymax =0.02 ,color='k',ls='-',lw=2)

ax.grid(True)
marker_handles = list()
#plt.show()
plt.savefig('WRF_BGW_1024.pdf')
