# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 14:12:01 2016

Plot interpolated, averaged, APD maps

@author: lab
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy.interpolate import interp1d

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

data= np.loadtxt('APD_binned2.csv',delimiter=',',skiprows=1)

bcl=data[:,0]
c_mean=data[:,1]
c_std=data[:,2]
m_mean=data[:,3]
m_std=data[:,4]

ls = 'dotted'
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# standard error bars
ax.errorbar(bcl,c_mean, yerr=np.array(c_std)/np.sqrt(3), ls=ls, color='black',marker='o',ms=8)
ax.errorbar(bcl, m_mean, yerr=np.array(m_std)/np.sqrt(3), ls=ls, color='red',marker='s',ms=8)
plt.ylim(ymin=45,ymax=81)
plt.xlim(xmin=60,xmax=290)
plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_ylabel('Action Potential Duration (ms)',fontsize=16)
ax.set_xlabel('Pacing Cycle Length (ms)',fontsize=16)
#labels=['Baseline', 'Week 2', 'Week 4', 'Week 6']
#plt.xticks(x, labels, rotation=45,fontsize=16)

# Legend creation
ctrl_legend = mlines.Line2D([], [], color='black',ls='dotted', marker='o',
                            markersize=8, label='Ctrl')
dehp_legend = mlines.Line2D([], [], color='red',ls='dotted', marker='s',
                          markersize=8, label='MEHP')
plt.legend(handles=[ctrl_legend, dehp_legend],loc='upper left',numpoints=1, fontsize=16)

#fig.savefig('APD.png')