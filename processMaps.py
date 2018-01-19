# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 16:20:35 2018

Optical Map Processor

@author: Rafael Jaimes III, PhD
"""

import numpy as np
import cv2 #use zypper install python3-opencv to get this module

def processMaps():

    import scipy.io as spio
    import matplotlib.pyplot as plt       

    def removeBG(data,thresh):
        # This function removes the background using thresholding
        # Adjust the input "thresh" value based on the histogram of the data.
        # A lower threshold will allow more pixels through.
        from skimage import morphology    # python3-scikit-image
        from skimage import img_as_ubyte
        # First determine the standard deviation image
        imstd=np.zeros([np.size(data,axis=0),np.size(data,axis=1)],dtype="float32")
        for r in range(0,np.size(data,axis=0)):
            for c in range(0,np.size(data,axis=1)):
                imstd[r,c]=np.std(data[r,c,:])  
        ret1, imthres = cv2.threshold(imstd, thresh, 1, cv2.THRESH_BINARY)  
        imUbyte=img_as_ubyte(imthres)
        # Remove the small objects. set min_size of pixel group and connectivity (num of px away from heart)        
        imNoSmall=morphology.remove_small_objects(imUbyte.astype(bool), min_size=1024, connectivity=1) #min_size=512 works
        # use MORPH_CLOSE to fill the gaps
        kernel = np.ones((15,15),dtype="uint8") # increase the kernel size to fill bigger holes
        imFilled = cv2.morphologyEx(imNoSmall.astype("uint8"), cv2.MORPH_CLOSE, kernel)
        mask = imFilled.astype(bool);
    
        data_no_BG=np.zeros(np.shape(data),dtype="float32")
        for p in range(0,np.size(data,axis=2)):
            data_no_BG[:,:,p]=data[:,:,p]*mask;
        return data_no_BG, mask
        
    def normalize(data):
        # This function normalizes the images across time
        min_data=np.amin(data,axis=2) #Get the array minimum across time (axis=2)
        max_data=np.amax(data,axis=2)
        diff_data=max_data-min_data;
    
        norm_data=np.zeros(np.shape(data),dtype="float32")
        for p in range(0,np.size(data,axis=2)):
            norm_data[:,:,p]=np.divide((data[:,:,p]-min_data),diff_data);  
        return norm_data
        
    def smooth(data):
        kernel=np.ones((45,45),np.float32)/2025 #Smoothing Kernel
        smooth_data=np.zeros(np.shape(data),dtype="float32")
        for p in range(0,np.size(data,axis=2)):    
            smooth_data[:,:,p] = cv2.filter2D(data[:,:,p],-1,kernel) # convolve the image 
        return smooth_data
        
    def rotImage(data):        
        rows,cols=data[:,:,1].shape # Get the X and Y dim from first frame
        rot=cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
        rot_data=np.zeros(np.shape(data),dtype="float32")
        for p in range(0,np.size(data,axis=2)):
            rot_data[:,:,p]=cv2.warpAffine(data[:,:,p],rot,(cols,rows))
        return rot_data
        
    # Main Functions Start Here
    
    # Process the Voltage signals
    preload_vm = spio.loadmat('/run/media/lab/NVMe/Data/Mapping/Dual/20171221-rata-06-vm.mat', squeeze_me=True)
    vm_data=-preload_vm['data'];
    v_cmap="jet"
    VmNoBG, vm_mask=removeBG(vm_data,thresh=20); #thresh of 20 works well.
    vm_smooth=smooth(VmNoBG);
    vm_norm=normalize(vm_smooth)
    #vm_rot=rotImage(vm_norm);

    
    # Process the Calcium signals
    preload_ca = spio.loadmat('/run/media/lab/NVMe/Data/Mapping/Dual/20171221-rata-06-ca.mat', squeeze_me=True)
    ca_data=preload_ca['data'];
    c_cmap="CMRmap"
    CaNoBG, ca_mask=removeBG(ca_data,thresh=9); #thresh of 10 works well.
    ca_smooth=smooth(ca_data);    
    ca_norm=normalize(ca_smooth)    


#==============================================================================
#     fig = plt.figure(figsize=(12,5),dpi=72)
#     ax = fig.add_subplot(2, 2, 1)
#     plt.imshow(ca_data[:,:,1])
#     plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#     
#     fig = plt.figure(figsize=(12,5),dpi=72)
#     ax = fig.add_subplot(2, 2, 2)
#     plt.imshow(ca[:,:,1]*mask)
#     plt.title('BG Removed'), plt.xticks([]), plt.yticks([])
#     
#     fig = plt.figure(figsize=(12,5),dpi=72)
#     ax = fig.add_subplot(2, 2, 3)
#     plt.imshow(ca_semi[:,:,1](mask))
#     plt.title('Normed, Smooth, BG'), plt.xticks([]), plt.yticks([])
#     
#     fig = plt.figure(figsize=(12,5),dpi=72)
#     ax = fig.add_subplot(2, 2, 4)
#     plt.imshow(ca_final[:,:,1]*mask)
#     plt.title('Smooth, Normed, BG'), plt.xticks([]), plt.yticks([])#     
#==============================================================================


    #frames=(522,530,535,559,580); #Select the frame numbers you want to display here
    #frames=(520,530,540,550,560);    
    frames=(522,527,532,537,542)    
    
    fig = plt.figure(figsize=(12,5),dpi=72)
    ax = fig.add_subplot(2, 5, 1)
    plt.imshow(vm_norm[:,:,frames[0]]*vm_mask,cmap=v_cmap)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylabel('Vm',fontsize=16)    
    ax.text(-50,25,'A',ha='center',va='bottom',fontsize=24,fontweight='bold')
    
    ax = fig.add_subplot(2, 5, 2)
    plt.imshow(vm_norm[:,:,frames[1]]*vm_mask,cmap=v_cmap)
    ax.set_xticks([])
    ax.set_yticks([])    
    
    ax = fig.add_subplot(2, 5, 3)
    plt.imshow(vm_norm[:,:,frames[2]]*vm_mask,cmap=v_cmap)
    ax.set_xticks([])
    ax.set_yticks([])    
    
    ax = fig.add_subplot(2, 5, 4)
    plt.imshow(vm_norm[:,:,frames[3]]*vm_mask,cmap=v_cmap)
    ax.set_xticks([])
    ax.set_yticks([])    
    
    ax = fig.add_subplot(2, 5, 5)
    plt.imshow(vm_norm[:,:,frames[4]]*vm_mask,cmap=v_cmap)
    ax.set_xticks([])
    ax.set_yticks([])  
    
    ax = fig.add_subplot(2, 5, 6)
    plt.imshow(ca_norm[:,:,frames[0]]*ca_mask,cmap=c_cmap)
    ax.set_xticks([])
    ax.set_yticks([])    
    ax.set_xlabel('t=0 ms',fontsize=16)
    ax.set_ylabel('Ca',fontsize=16)    
    ax.text(-50,25,'B',ha='center',va='bottom',fontsize=24,fontweight='bold')
    
    ax = fig.add_subplot(2, 5, 7)
    plt.imshow(ca_norm[:,:,frames[1]]*ca_mask,cmap=c_cmap)
    ax.set_xticks([])
    ax.set_yticks([])  
    ax.set_xlabel('t=10 ms',fontsize=16)
    
    ax = fig.add_subplot(2, 5, 8)
    plt.imshow(ca_norm[:,:,frames[2]]*ca_mask,cmap=c_cmap)
    ax.set_xticks([])
    ax.set_yticks([])    
    ax.set_xlabel('t=20 ms',fontsize=16)
    
    ax = fig.add_subplot(2, 5, 9)
    plt.imshow(ca_norm[:,:,frames[3]]*ca_mask,cmap=c_cmap)
    ax.set_xticks([])
    ax.set_yticks([])  
    ax.set_xlabel('t=30 ms',fontsize=16)
    
    ax = fig.add_subplot(2, 5, 10)
    plt.imshow(ca_norm[:,:,frames[4]]*ca_mask,cmap=c_cmap)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('t=40 ms',fontsize=16)    

    fig.savefig('Vm_Ca_maps.pdf')
processMaps()