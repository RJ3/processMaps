import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig

### TRACES
# Load from .asc files exported from Andor SOLIS.

## Traces for Rhod-2
base_trace_preload = np.loadtxt('20171206-ratb-07-Ca.asc',delimiter=',')
post_trace_preload = np.loadtxt('20171206-ratb-35-Ca.asc',delimiter=',')
m3_trace_preload = np.loadtxt('20171206-ratb-36-Ca.asc',delimiter=',')

time=base_trace_preload[:,0]

base_trace_smooth=sig.detrend(sig.savgol_filter(base_trace_preload[:,1],5,3))
post_trace_smooth=sig.detrend(sig.savgol_filter(post_trace_preload[:,1],7,3))
m3_trace_smooth=sig.detrend(sig.savgol_filter(m3_trace_preload[:,1],7,3))

plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16)
fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot(2, 3, 1)
plt.plot(time,base_trace_smooth+15,color='orange',linewidth=2,label='Baseline')
ax=plt.gca()
plt.plot(time,np.roll(post_trace_smooth,-110)+10,color='k',linewidth=2,linestyle='--',label='30 sec Ry')
plt.plot(time,np.roll(m3_trace_smooth,-100)+6,color='k',linewidth=2,linestyle=':',label='3 min Ry')
ax.tick_params(axis='x', which='both',bottom='on',top='off')
ax.tick_params(axis='y', which='both',right='off',left='on')
plt.xlim(xmin=0.10,xmax=0.44)
m=['0', '100', '200', '300']
ticks=[0.10, 0.20, 0.30, 0.40]
ax.set_xticks(ticks)
ax.set_xticklabels(m)
plt.ylim(ymin=-1,ymax=50)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('Calcium \nFluorescence (Counts)',fontsize=16)
plt.xlabel('Time (ms)',fontsize=16)
#lt.title('Calcium',fontsize=16)
plt.legend(bbox_to_anchor=(1.2, 1.1),loc='upper right',ncol=1, prop={'size':14},numpoints=1,frameon=False)
yl=ax.get_ylim()
yr=yl[1]-yl[0]
xl=ax.get_xlim()
xr=xl[1]-xl[0]
ax.text(xl[0]-(xr*0.32),yr*0.94+yl[0],'A',ha='center',va='bottom',fontsize=24,fontweight='bold')

## Traces for RH237
base_trace_preload = np.loadtxt('20171206-ratb-07-Vm.asc',delimiter=',')
post_trace_preload = np.loadtxt('20171206-ratb-35-Vm.asc',delimiter=',')
m3_trace_preload = np.loadtxt('20171206-ratb-36-Vm.asc',delimiter=',')

time=base_trace_preload[:,0]

# Butterworth LPF
b, a = sig.butter(1, 0.3, 'low', analog=False)
base_trace_smooth=sig.filtfilt(b,a,sig.detrend(-1*(base_trace_preload[:,1])))
post_trace_smooth=sig.filtfilt(b,a,sig.detrend(-1*(post_trace_preload[:,1])))
m3_trace_smooth=sig.filtfilt(b,a,sig.detrend(-1*(m3_trace_preload[:,1])))

ax = fig.add_subplot(2, 3, 2)
plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16)
plt.plot(time,base_trace_smooth+3,color='r',linewidth=2,label='Baseline')
ax=plt.gca()
plt.plot(time,np.roll(post_trace_smooth,70)+4,color='k',linewidth=2,linestyle='--',label='30 sec Ry')
#label='30 sec 10$\mu$M \nRyanodine')
plt.plot(time,np.roll(m3_trace_smooth,-40)+5,color='k',linewidth=2,linestyle=':',label='3 min Ry')
ax.tick_params(axis='x', which='both',bottom='on',top='off')
ax.tick_params(axis='y', which='both',right='off',left='on')
plt.xlim(xmin=0.82,xmax=1.15)
m=['0', '100', '200', '300']
ticks=[0.82, 0.92, 1.02, 1.12]
ax.set_xticks(ticks)
ax.set_xticklabels(m)
plt.ylim(ymin=-1,ymax=20)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('Counts',fontsize=16)
plt.xlabel('Time (ms)',fontsize=16)
plt.ylabel('Voltage \nFluorescence (Counts)',fontsize=16)
plt.legend(bbox_to_anchor=(1.2, 1.1),loc='upper right',ncol=1, prop={'size':14},numpoints=1,frameon=False)
yl=ax.get_ylim()
yr=yl[1]-yl[0]
xl=ax.get_xlim()
xr=xl[1]-xl[0]
ax.text(xl[0]-(xr*0.32),yr*0.94+yl[0],'B',ha='center',va='bottom',fontsize=24,fontweight='bold')

# CALCIUM Amplitude
base_RT=[100,100]
p1_RT=[60,59.5]
p2_RT=[40.1,53.2]

width = 0.2

ax1 = fig.add_subplot(2, 3, 3)

base_sem=np.std(base_RT)/np.sqrt(3);
p1_sem=np.std(p1_RT)/np.sqrt(3)

ax1.bar(0.4-width/2,np.mean(base_RT), width, color='orange',yerr=[base_sem],ecolor='k', error_kw=dict(lw=2, capsize=12, capthick=2))
ax1.bar(0.7-width/2,np.mean(p1_RT),width, color='w',yerr=p1_sem,ecolor='k', error_kw=dict(lw=2, capsize=12, capthick=2))

plt.ylim(ymin=0,ymax=120)
plt.xlim(xmin=0.1,xmax=1)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

labels=['Baseline','Ry']
plt.xticks([0.4,0.7], labels, rotation=0,fontsize=16)
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_ylabel('CaT Amplitude (%)',fontsize=16)
ax1.text(0.55,110,'*',ha='center',va='bottom',fontsize=20)
ax1.plot([0.4, 0.7], [110, 110], "k-",linewidth=4)
yl=ax1.get_ylim()
yr=yl[1]-yl[0]
xl=ax1.get_xlim()
xr=xl[1]-xl[0]
ax1.text(xl[0]-(xr*0.30),yr*0.94,'C',ha='center',va='bottom',fontsize=24,fontweight='bold')

# CALCIUM RISE TIME
base_RT=[21.6,19.4,33.4]
p1_RT=[34.1,33.4,28.1]
p2_RT=[40.1,53.2]

ax1 = fig.add_subplot(2, 3, 4)

base_sem=np.std(base_RT)/np.sqrt(3);
p1_sem=np.std(p1_RT)/np.sqrt(3)

ax1.bar(0.4-width/2,np.mean(base_RT), width, color='orange',yerr=[base_sem],ecolor='k', error_kw=dict(lw=2, capsize=12, capthick=2))
ax1.bar(0.7-width/2,np.mean(p1_RT),width, color='w',yerr=p1_sem,ecolor='k', error_kw=dict(lw=2, capsize=12, capthick=2))

plt.ylim(ymin=0,ymax=35)
plt.xlim(xmin=0.1,xmax=1)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

labels=['Baseline','Ry']
plt.xticks([0.4,0.7], labels, rotation=0,fontsize=16)
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_ylabel('CaT Rise Time (ms)',fontsize=16)
yl=ax1.get_ylim()
yr=yl[1]-yl[0]
xl=ax1.get_xlim()
xr=xl[1]-xl[0]
ax1.text(xl[0]-(xr*0.22),yr*0.96,'D',ha='center',va='bottom',fontsize=24,fontweight='bold')


# CALCIUM CaD80
base_CaD80=[175,161,179]
p1_CaD80=[215,213,304]

ax1 = fig.add_subplot(2, 3, 5)

base_sem=np.std(base_CaD80)/np.sqrt(3);
p1_sem=np.std(p1_CaD80)/np.sqrt(3)

ax1.bar(0.4-width/2,np.mean(base_CaD80), width, color='orange',yerr=base_sem,ecolor='k', error_kw=dict(lw=2, capsize=12, capthick=2))
ax1.bar(0.7-width/2,np.mean(p1_CaD80),width, color='w',yerr=p1_sem,ecolor='k', error_kw=dict(lw=2, capsize=12, capthick=2))
plt.ylim(ymin=0,ymax=300)
plt.xlim(xmin=0.1,xmax=1)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

labels=['Baseline','Ry']
plt.xticks([0.4,0.7], labels, rotation=0,fontsize=16)
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_ylabel('CaD80 (ms)',fontsize=16)
ax1.text(0.55,292,'*',ha='center',va='bottom',fontsize=20)
ax1.plot([0.4, 0.7], [292, 292], "k-",linewidth=4)
yl=ax1.get_ylim()
yr=yl[1]-yl[0]
xl=ax1.get_xlim()
xr=xl[1]-xl[0]
ax1.text(xl[0]-(xr*0.28),yr*0.96,'E',ha='center',va='bottom',fontsize=24,fontweight='bold')

# VOLTAGE APD80
base_CaD80=[99.7,88.3]
p1_CaD80=[122,140]

ax1 = fig.add_subplot(2, 3, 6)

base_sem=np.std(base_CaD80)/np.sqrt(3);
p1_sem=np.std(p1_CaD80)/np.sqrt(3)

ax1.bar(0.4-width/2,np.mean(base_CaD80), width, color='r',yerr=base_sem,ecolor='k', error_kw=dict(lw=2, capsize=12, capthick=2))
ax1.bar(0.7-width/2,np.mean(p1_CaD80),width, color='w',yerr=p1_sem,ecolor='k', error_kw=dict(lw=2, capsize=12, capthick=2))
plt.ylim(ymin=0,ymax=160)
plt.xlim(xmin=0.1,xmax=1)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

labels=['Baseline','Ry']
plt.xticks([0.4,0.7], labels, rotation=0,fontsize=16)
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
ax1.set_ylabel('APD80 (ms)',fontsize=16)
ax1.text(0.55,150,'*',ha='center',va='bottom',fontsize=20)
ax1.plot([0.4,0.7], [150, 150], "k-",linewidth=4)
yl=ax1.get_ylim()
yr=yl[1]-yl[0]
xl=ax1.get_xlim()
xr=xl[1]-xl[0]
ax1.text(xl[0]-(xr*0.28),yr*0.96,'F',ha='center',va='bottom',fontsize=24,fontweight='bold')

#h_pad = height between edges of adjacent subplots, w_pad width between edges of adjacent subplots
#pad = padding between the figure edge and the edges of subplots, as a fraction of the font-size
plt.rcParams.update({'font.size': 22})
plt.tight_layout(pad=0.3, w_pad=3, h_pad=2)

fig.savefig('Ryanodine_combined.pdf')

