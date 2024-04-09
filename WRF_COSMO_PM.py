import numpy as np
import matplotlib.pyplot as plt
import sys

########################### SYSTEM INPUTS ###########################
GPU_HARDWARE=(1536+256)
PEAK_NODE_GPU_BW=1555*4# in GB/s
RANKS_PER_NODE=4
PEAK_FILE_SYSTEM=5600
GPU_NODE_FLOPS=4*9.7
#####################################################################


########################### META DATA ###########################
run_start=[1696936770182,	1696936796492,	1696936796581,	1696936798379,	1696936770313,	1696936778223,	1696936770002,	1696936780535,	1696936777522,	1696936797801,	1696936798563,	1696936793627] #,	1696936770002]
run_stop=[1696937060209,	1696937073610,	1696937071778,	1696937066575,	1696937065146,	1696937051693,	1696937037660,	1696937039951,	1696937073031,	1696937075874,	1696937064235,	1696937070007] #,	1696937075874]
#####################################################################

########################### WORKFLOW INPUTS ###########################
TOTAL_TASKS=12
PARALLEL_TASKS=12
EPOCHS=25
NODES_PER_TASK=128
FILE_SYSTEM_VOL=2*1024  # GB
PCIE_VOL=(10*1024)/NODES_PER_TASK
TOT_SAMPLE=524288 #2^19
HBM_BYTES_PER_SAMPLE=6.4 #GB
HBM_TIME=(HBM_BYTES_PER_SAMPLE*TOT_SAMPLE)/(PEAK_NODE_GPU_BW*NODES_PER_TASK)  #=4.21s

########################### INPUTS ENDS ###########################

font = { 'size'   : 15}
plt.rc('font', **font)

colors = ['blue','red','green','m','c','y','k','crimson']
styles = ['o','s','D','v','^',">","<","*","h","H","+","1","2","3","4","8","p","d","|","_",".",","]

fig = plt.figure(1,figsize=(8,8))
plt.clf()
ax = fig.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Number of Instances')
ax.set_ylabel('Throughput [#Epochs/sec]')
nx = 1000
xmin = -3
xmax = 3
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
run_time=[]

for i in range(0,len(run_start)):
    run_time.append(float((run_stop[i]-run_start[i])/(1000)))
duration=(max(run_stop)-min(run_start))/(1000)
throughput=(PARALLEL_TASKS)/duration


plt.plot(1, (1*EPOCHS)/run_time[0],c='darkred',marker='o',markersize=10)
#plt.plot(1, 1/(run_time[0]/4.5),c=colors[5],marker='s')
min_time=min(1696936770182,	1696936796492)
max_time=max(1696937060209,	1696937073610)
plt.plot(2, (2*EPOCHS)/((max_time-min_time)/1000),c='darkred',marker='o',markersize=10)
min_time=min(1696936770182,	1696936796492,	1696936796581,	1696936798379)
max_time=max(1696937060209,	1696937073610,	1696937071778,	1696937066575)
plt.plot(4, (4*EPOCHS)/((max_time-min_time)/1000),c='darkred',marker='o',markersize=10)
min_time=min(1696936770182,	1696936796492,	1696936796581,	1696936798379,	1696936770313,	1696936778223,	1696936770002,	1696936780535)
max_time=max(1696937060209,	1696937073610,	1696937071778,	1696937066575,	1696937065146,	1696937051693,	1696937037660,	1696937039951)
plt.plot(8, (8*EPOCHS)/((max_time-min_time)/1000),c='darkred',marker='o',markersize=10)
plt.plot(PARALLEL_TASKS, throughput*EPOCHS,c='darkred',marker='o',markersize=10)

system_plot=1
if system_plot==1:
    smemroofs=[]
    scomproofs=[]
    scomp_x_elbow=[]
    scomp_ix_elbow=[]

    PARA_LIMIT=GPU_HARDWARE/NODES_PER_TASK

    for ab in range(0,1):
        smemroofs=[]
        scomproofs=[]
        scomp_x_elbow=[]
        scomp_ix_elbow=[]
        smem_x_elbow=[]
        smem_ix_elbow=[]



        latency=(PCIE_VOL/4096)/100
        smemroofs.append(latency)

        latency=HBM_TIME
        smemroofs.append(latency)


        scomproofs.append((PARALLEL_TASKS*EPOCHS)/((PARALLEL_TASKS*FILE_SYSTEM_VOL)/(PEAK_FILE_SYSTEM)))

        scomproofs.append((1*EPOCHS)/((1*FILE_SYSTEM_VOL)/(PEAK_FILE_SYSTEM)))

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
            ax.plot(x[:smem_ix_elbow[i]+1],y[:smem_ix_elbow[i]+1],c='k',ls='-',lw='2')



para_plot=1
if para_plot==1:

    plt.axvline(x = PARA_LIMIT , color = 'k')


ax.grid(True)
marker_handles = list()

plt.savefig('WRF_COSMO_PM.pdf')
