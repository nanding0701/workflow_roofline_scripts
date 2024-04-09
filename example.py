import numpy as np
import matplotlib.pyplot as plt
import sys
import math

font = { 'size'   : 15}
plt.rc('font', **font)


#bandwidth= [1, 3.5,6.5, 100]
smemroofs = [120] #, 200,1000/3.5, 1000/6.5, 1000/100, 1000/20]
#smemroofs = [120, 200,1000/3.5, 1000/6.5, 1000/100, 1000/20]
smem_roof_name = ['quanta=256KB','quanta=4KB','quanta=32B','quanta=8B']




colors = ['blue','red','green','m','red','c']
styles = ['o','s','v','^','D',">","<","*","h","H","+","1","2","3","4","8","p","d","|","_",".",","]

fig = plt.figure(1,figsize=(8,6))
plt.clf()
ax = fig.gca()
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Task parallelism')
ax.set_ylabel('Throughput [#tasks/sec]')

nx = 1000
xmin = -1
xmax = 4
ymin = 0.001
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
#for roof in scomproofs:
#   for ix in range(1,nx):
#        if (x[ix])/smemroofs[0] >= roof and (x[ix-1])/smemroofs[0] < roof:
#            scomp_x_elbow.append(x[ix-1])
#            scomp_ix_elbow.append(ix-1)
#            break
#    #print(scomp_x_elbow)
#
#for roof in smemroofs:
#    for ix in range(1,nx):
#        if (scomproofs[0] <= (x[ix])/roof) and (scomproofs[0] > ( x[ix-1])/roof):
#            smem_x_elbow.append(x[ix-1])
#            smem_ix_elbow.append(ix-1)
#            break
#    #print(scomp_x_elbow)
#
#for i in range(0,len(scomproofs)):
#    roof = scomproofs[i]
#    y = np.ones(len(x)) * roof / scalingFactorForRoofs
#    ax.plot(x[scomp_ix_elbow[i]:],y[scomp_ix_elbow[i]:],c='k',ls='--',lw='2')
#
#for i in range(0,len(smemroofs)):
#    roof = smemroofs[i]
#    y = ((x)/roof) / scalingFactorForRoofs
#    ax.plot(x[:smem_ix_elbow[i]+1],y[:smem_ix_elbow[i]+1],c='k',ls='--',lw='2')

system_plot=1
if system_plot==1:
    TaskNum=5
    data=1000
    #achieved_bandwidth=[(512/(6555))] #6.5,3.5]
    #achieved_bandwidth=[5/(1000/(6555/5))] #6.5,3.5]
    achieved_bandwidth=[((1000/8)/(204.8*2))] #6.5,3.5]
    #achieved_bandwidth=[25,3.5] #6.5,3.5]
    smemroofs=[]
    scomproofs=[]
    scomp_x_elbow=[]
    scomp_ix_elbow=[]

    Cores_per_task=1024
    CPU_HARDWARE=3072
    GPU_NODE=1536+256
    MEM_NODE=1000
    BURST_BUFFER_N0DE=(1.7*1000)/6.5
    PARA_LIMIT=math.floor(CPU_HARDWARE/(1024/128))

    print(PARA_LIMIT)

    for ab in range(0,len(achieved_bandwidth)):
        smemroofs=[]
        scomproofs=[]
        scomp_x_elbow=[]
        scomp_ix_elbow=[]
        smem_x_elbow=[]
        smem_ix_elbow=[]

        #scomproofs.append(5/(1000/(100)))
        #scomproofs.append(5/(1000/(2.6*8)))

        #scomproofs.append(5/(1000/(20)))
        #scomproofs.append(5/(1000/((2.6*8)/5)))

        #scomproofs.append(5/(1000/((2.6*8)/5)))
        #scomproofs.append(5/(1000/(4.16)))
        #scomproofs.append(5/120)
        #latency=data/achieved_bandwidth[ab]
        #peak_throughput_node=5/latency
        smemroofs.append(1/(1/25))
        smemroofs.append(1/(0.1/(9.7*4)))

        scomproofs.append(1/(1000/(5600)))
        scomproofs.append(1/(1000/(100)))
        #scomproofs.append(5/(1000/(100)))
        #scomproofs.append(5/(1000/(100)))
        #scomproofs.append(5/(1000/(25/5)))
        #scomproofs.append(5/(1000/6.5))

        #scomproofs.append(5/(1000/(12.5)))
        #scomproofs.append(5/(1000/(0.125)))


        for roof in scomproofs:
            for ix in range(1,nx):
                if (x[ix])/smemroofs[0] >= roof and (x[ix-1])/smemroofs[0] < roof:
                    scomp_x_elbow.append(x[ix-1])
                    scomp_ix_elbow.append(ix-1)
                    break
        print(scomp_x_elbow)
        print(roof)
        print(smemroofs[0])

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
            ax.plot(x[scomp_ix_elbow[i]:],y[scomp_ix_elbow[i]:],c='k',ls='-',lw='2')

        for i in range(0,len(smemroofs)):
            roof = smemroofs[i]
            y = ((x)/roof) / scalingFactorForRoofs
            ax.plot(x[:smem_ix_elbow[i]+1],y[:smem_ix_elbow[i]+1],c='k',ls='-',lw='2')



para_plot=1
if para_plot==1:

    plt.vlines(x = PARA_LIMIT, ymin = ymin, ymax =scomproofs[0] ,color='k',ls='-',lw=2)
    #plt.axvline(x = PARA_LIMIT , color = 'k')

    #PARA_LIMIT=MEM_NODE
    #print(PARA_LIMIT)
    #plt.axvline(x = PARA_LIMIT , color = 'r')

    #PARA_LIMIT=BURST_BUFFER_N0DE
    #print(PARA_LIMIT)
    #plt.axvline(x = BURST_BUFFER_N0DE , color = 'b')



ax.grid(True)
marker_handles = list()

plt.savefig('example.pdf')
