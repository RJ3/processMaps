#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 13:13:39 2019

Debugger test for traces

@author: raf
"""
import numpy as np
from peak_detect import peak_detect
import matplotlib.pyplot as plt
from process import process

path='/home/raf/Documents/Langendorff-MEHP/2019-02_Final_Figures/data/ap_examples/'
fname='20180720-rata-27-pcl240-t.csv'
fname2='20180720-rata-27-pcl240-vm.csv'

time = np.genfromtxt(path+fname, delimiter=',')
vm = np.genfromtxt(path+fname2, delimiter=',')

#%%
pcl=230
dt = (time[1]-time[0])*1000
LOT = pcl/dt
num_peaks, t0_locs, up_locs, peak_locs, base_locs, max_vel, peak_thresh = peak_detect(vm, 0.5, LOT)

fig = plt.figure(1)
fig.clf()
plt.scatter(t0_locs, vm[t0_locs], s=50, marker='^', color='orange')
plt.scatter(up_locs, vm[up_locs], s=50, marker='^', color='r')
plt.scatter(peak_locs, vm[peak_locs], s=50, marker='o', color='blue')
plt.scatter(base_locs, vm[base_locs], s=50, marker='s', color='blue')
plt.plot(vm)
plt.plot(np.gradient(vm),'r') # 1st derivative of the signal to find max dF/dt (up or upstroke)
plt.plot(np.gradient(np.gradient(vm)),'orange') # 2nd derivative of the signal to find max d2F/dt2 (t0)

#%%
# Debug Process

f_sort=np.sort(vm)
F0=np.mean(f_sort[num_peaks*2]) #F0 for the epoch is the mean of the smallest values (twice the num_peaks)


results = process(vm, dt, num_peaks, t0_locs, up_locs, peak_locs, base_locs, max_vel, F0, 1)