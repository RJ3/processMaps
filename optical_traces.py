# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 10:08:22 2017

@author: lab
"""

import scipy.io as spio
import matplotlib.pyplot as plt
import scipy.signal as sig
### TRACES

ca_trace_preload = spio.loadmat('/home/lab/Documents/OpticalMapping/Examples/20170615-rata-08-ca.mat', squeeze_me=True)
vm_trace_preload = spio.loadmat('/home/lab/Documents/OpticalMapping/Examples/20170615-rata-08-vm.mat', squeeze_me=True)
ca_trace=ca_trace_preload['calcium']
vm_trace=vm_trace_preload['voltage']

ca_trace_smooth=sig.savgol_filter(ca_trace,5,3)
vm_trace_smooth=sig.savgol_filter(vm_trace,7,3)

plt.plot(vm_trace_smooth,color='orange',linewidth=2)
ax=plt.gca()
plt.plot(ca_trace_smooth+0.2,color='r',linewidth=2)
ax.tick_params(axis='x', which='both',bottom='on',top='off')
plt.xlim(xmin=350,xmax=1200)
plt.ylim(ymin=-0.4,ymax=0.8)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('Fluorescence',fontsize=16)
plt.xlabel('Time (msec)',fontsize=16)

plt.plot(vm_trace_smooth,color='orange',linewidth=2)
ax=plt.gca()
plt.plot(ca_trace_smooth+0.2,color='r',linewidth=2)
ax.tick_params(axis='x', which='both',bottom='on',top='off')
ax.tick_params(axis='y', which='both',right='off',left='on')
plt.xlim(xmin=400,xmax=440)
plt.ylim(ymin=-0.4,ymax=0.8)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('Fluorescence',fontsize=16)
plt.xlabel('Time (msec)',fontsize=16)

#plt.savefig('ca_vm_trace_zoom.svg')

#


ca_trace_preload = spio.loadmat('/home/lab/Documents/OpticalMapping/Examples/20171017-rata-16-ca-ventricle.mat', squeeze_me=True)
vm_trace_preload = spio.loadmat('/home/lab/Documents/OpticalMapping/Examples/20171017-rata-16-vm-ventricle.mat', squeeze_me=True)
ca_trace=ca_trace_preload['calcium']
vm_trace=vm_trace_preload['voltage']

ca_trace_smooth=sig.savgol_filter(ca_trace,5,3)
vm_trace_smooth=sig.savgol_filter(vm_trace,31,3)

plt.plot(vm_trace_smooth*2,color='orange',linewidth=2)
ax=plt.gca()
plt.plot(ca_trace_smooth+1,color='r',linewidth=2)
ax.tick_params(axis='x', which='both',bottom='on',top='off')
plt.xlim(xmin=350,xmax=1200)
plt.ylim(ymin=1,ymax=2)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('Fluorescence',fontsize=16)
plt.xlabel('Time (msec)',fontsize=16)




ca_trace_preload = spio.loadmat('/home/lab/Documents/OpticalMapping/Examples/20171017-rata-16-ca-atrium.mat', squeeze_me=True)
vm_trace_preload = spio.loadmat('/home/lab/Documents/OpticalMapping/Examples/20171017-rata-16-vm-ventricle.mat', squeeze_me=True)
ca_trace=ca_trace_preload['calcium']
vm_trace=vm_trace_preload['voltage']

ca_trace_smooth=sig.savgol_filter(ca_trace,5,3)
vm_trace_smooth=sig.savgol_filter(vm_trace,31,3)

plt.plot(vm_trace_smooth*2,color='orange',linewidth=2)
ax=plt.gca()
plt.plot(ca_trace_smooth+1.1,color='r',linewidth=2)
ax.tick_params(axis='x', which='both',bottom='on',top='off')
plt.xlim(xmin=350,xmax=1200)
plt.ylim(ymin=1,ymax=2)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.ylabel('Fluorescence',fontsize=16)
plt.xlabel('Time (msec)',fontsize=16)

