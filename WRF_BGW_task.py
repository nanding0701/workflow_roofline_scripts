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
para=[64, 1024]
myx=[1, 1]
time1=[1096.50, 179.56]
time2=[3088.36,  225.18]
tflop1=1164*1000
tflop2=12.6*256*1000
batches=[80,5]
mpi_vol1_per_batch=[85.3,85.3,85.3]
mpi_vol2_per_batch=[48.5,48.5,48.5]
#####################################################################

########################### WORKFLOW INPUTS ###########################
TOTAL_TASKS=2
PARALLEL_TASKS=1
FILE_SYSTEM_VOL=70  # GB
########################### INPUTS ENDS ###########################

font = { 'size'   : 15}
plt.rc('font', **font)

filename = 'plot_' + sys.argv[0].split('_')[0]+'_'+sys.argv[0].split('_')[1]+'_'+sys.argv[0].split('_')[2]

colors = ['red','blue','darkred','darkblue','c','y','k','crimson']
styles = ['o','s','D','v','^',">","<","*","h","H","+","1","2","3","4","8","p","d","|","_",".",","]

fig = plt.figure(1,figsize=(8,8))
plt.clf()
ax = fig.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Number of Parallel Task')
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


myy=[]
myy1=[]
myy2=[]
for i in range(0,len(time1)):
    myy.append(float(1/(time1[i]+time2[i])))
    myy1.append(float(1/(time1[i])))
    myy2.append(float(1/(time2[i])))

for ab in range(0,len(time1)):
    system_plot=1
    if system_plot==1:
        PARA_LIMIT=math.floor(GPU_HARDWARE/para[ab])

        smemroofs=[]
        scomproofs=[]
        scomp_x_elbow=[]
        scomp_ix_elbow=[]
        smem_x_elbow=[]
        smem_ix_elbow=[]

        ### node flops
        latency=(tflop1/para[ab])/(9.7*4)
        smemroofs.append(latency)


        ### mpi vol, system
        scomproofs.append(1/(70/(5600)))


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
        if ab==1:
            for i in range(0,len(scomproofs)):
                roof = scomproofs[i]
                y = np.ones(len(x)) * roof / scalingFactorForRoofs
                if i==0:
                    ax.plot(x[scomp_ix_elbow[i]:],y[scomp_ix_elbow[i]:],c='k',ls='--',lw='2')


        for i in range(0,len(smemroofs)):
            roof = smemroofs[i]
            y = ((x)/roof) / scalingFactorForRoofs
            ax.plot(x[:smem_ix_elbow[i]+1],y[:smem_ix_elbow[i]+1],c=colors[ab+0],ls='--',lw='2')

        para_plot=0
        if para_plot==1:
            print("PARA_LIMIT",PARA_LIMIT)
            if ab==0:
                plt.vlines(x = PARA_LIMIT, ymin = ymin, ymax =0.06 ,color='k',ls='-',lw=2)

        ### sigma
        smemroofs=[]
        scomproofs=[]
        scomp_x_elbow=[]
        scomp_ix_elbow=[]
        smem_x_elbow=[]
        smem_ix_elbow=[]

        ### node flops
        latency=(tflop2/para[ab])/(9.7*4)
        smemroofs.append(latency)


        ### mpi vol, system
        scomproofs.append(1/((70)/(5600)))

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


        for i in range(0,len(smemroofs)):
            roof = smemroofs[i]
            y = ((x)/roof) / scalingFactorForRoofs
            ax.plot(x[:smem_ix_elbow[i]+1],y[:smem_ix_elbow[i]+1],c=colors[ab+1],ls='--',lw='2')

    if ab==0:
        ax.scatter(myx[ab],myy1[ab],s=100, facecolors=colors[0], edgecolors=colors[0],lw=2)
        ax.scatter(myx[ab],myy2[ab],s=100, facecolors=colors[1], edgecolors=colors[1],lw=2)
    if ab==1:
        ax.scatter(myx[ab],myy1[ab],s=100, facecolors=colors[2],edgecolors=colors[2],lw=2) #marker='s'
        ax.scatter(myx[ab],myy2[ab],s=100, facecolors=colors[3],edgecolors=colors[3],lw=2) #marker='s'

ax.grid(True)
marker_handles = list()
plt.show()
plt.savefig('WRF_BGW_task.pdf')
