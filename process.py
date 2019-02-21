#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processes a series of transient signals across time.

@author: Rafael Jaimes
raf@cardiacmap.com
v1: 2019-02-20 
"""

import scipy.optimize as curve_fit
import numpy as np
import pandas as pd

# You must run peak_detect first to feed all the peak locations.
# Specify the fluorescent probe you are analyzing:
# probe = 0 for voltage
# probe = 1 for calcium
# The probe specification will alter the column labels in the data frame and change how the activation time is computed
# F0 is computed beforehand, user can adjust with slider if needed.
def process(f, dt, num_peaks, t0_locs, up_locs, peak_locs, base_locs, max_vel, F0, probe):      
    if base_locs[0] < t0_locs[0]: # If there is a baseline point before the first transient
        base_locs = base_locs[1:]
        
    if t0_locs[-1] > base_locs[-1]: # If the last t0 points occurs after the last baseline point
        t0_locs = t0_locs[0:-1]
    
    num_transients = len(t0_locs)
    trans=0
    
    results = pd.DataFrame(np.zeros(shape=(num_transients,13)),
                           columns=['ActTime', 'Vmax', 'TimeToPeak', 'RiseTime', 'D30', 'DXX', 'D90', 
                                    'D30_DXX', 'Tri', 'TauFall', 'Dias', 'Sys','CL'])
    
    for p in range(0,num_transients): # Don't skip any transients
        
        if t0_locs[p] < up_locs[p] < peak_locs[p] < base_locs[p]:
            t0 = t0_locs[p]
            up = up_locs[p]
            peak = peak_locs[p]
            base = base_locs[p]
        else:
            print('Detection Error')
        
        # Finding points on the decay portion back to baseline
        decay = (f[peak:base] - f[base])/ (f[peak] - f[base]) # Normalize the decay portion from 1 to 0
        ret30 = np.nonzero(decay < 0.7)[0][0] # return to 30%, for CaD30/APD30, fitting Tau, and triangulation
        retXX = np.nonzero(decay < 0.8)[0][0] # return to XX% for CaDXX/APDXX
        ret90 = np.nonzero(decay < 0.9)[0][0] # return to 90% for CaD90/APD90 and triangulation
        
        # Finding point on the upstroke portion up to peak
        upstroke = (f[t0:peak] - f[t0])/ (f[peak] - f[t0]) # Normalize the upstroke portion from 1 to 0
        up90 = np.nonzero(upstroke > 0.9)[0][0] # return the first point that breaks 90% upstroke
        
        # Fitting routine       
        #time = np.linspace(0, len(decay)*dt, len(decay)) 
        #popt, pcov = curve_fit(func, time, decay, bounds=(0, [3., 1., 0.5]))
        #decay_fit = func(time, *popt)
        popt=[0, 1, 2]
        
        if probe == 0:
            start = up # for voltage, use max dF/dt as the start
        else:
            start = t0 # for calcium, use max d2F/dt2 as the start
                    
        results.ActTime[trans] = t0*dt
        results.Vmax[trans] = max_vel[p]
        results.TimeToPeak[trans] = (peak-t0)*dt
        results.RiseTime[trans] = (up90)*dt
        results.D30[trans] = (ret30+peak-start)*dt
        results.DXX[trans] = (retXX+peak-start)*dt
        results.D90[trans] = (ret90+peak-start)*dt
        results.D30_DXX[trans] = (ret30+peak-start)/(retXX+peak-start)
        results.Tri[trans] = (ret90+peak-start)*dt - (ret30+peak-start)*dt
        results.TauFall[trans] = 1/(popt[1])
        results.Dias[trans] = f[base]
        results.Sys[trans] = f[peak]
        if trans < num_peaks-1:
            results.CL[trans] = (peak_locs[trans+1]-peak)*dt
        else:
            results.CL[trans] = np.nan # last transient, cannot calculate CL anymore

            
        trans=trans+1
            
    if probe == 0:
        results.rename(columns={'D30':'APD30', 'DXX':'APDXX', 'D90':'APD90', 'D30_DXX':'APD30/APDXX'}, inplace=True)
    else:                
        results.rename(columns={'D30':'CaD30', 'DXX':'CaDXX', 'D90':'CaD90', 'D30_DXX':'CaD30/CaDXX'}, inplace=True)                    
             
    return results