# Import the ASCII filter data for filters and fluorophores
import numpy as np
import matplotlib.pyplot as plt

# Filters required for dual mapping Vm and Ca
dichroic_em = np.loadtxt('T660lpxrxt.txt')
rhod2_em = np.loadtxt('ET585-40m.txt')
rh237_em = np.loadtxt('et710lp-lot296950-transmission.txt')
ex = np.loadtxt('et530-40x-lot321683-transmission.txt')

# Load in the Fluorophore data
rhod2_flm = np.loadtxt('Rhod2Em.txt', delimiter=',') #From ThermoFisher SpectraViewer
rhod2_flx = np.loadtxt('Rhod2Ex.txt', delimiter=',') #From ThermoFisher SpectraViewer
rh237_fl = np.loadtxt('rh237_fl.dat') #From Choi and Salama 2000 - g3data

plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16)

plt.plot(dichroic_em[:,0],dichroic_em[:,1]*100,linewidth=2,color='#FF0000') #Multiply by 100, from Chroma site
plt.plot(rhod2_em[:,0],rhod2_em[:,1]*100,linewidth=2,color='#FFEF00') #Multiply by 100, from Chroma site
plt.plot(rh237_em[:,0],rh237_em[:,1],linewidth=2,color='#ED0000') #From Brian Manning email 2017-10-13
plt.plot(ex[:,0],ex[:,1],linewidth=2,color='#5EFF00') #From Brian Manning email 2017-10-13

#rhod2, =plt.plot(rhod2_flm[:,0],rhod2_flm[:,1],linewidth=2,color='gray',label='Rhod-2') 
#plt.plot(rhod2_flx[:,0],rhod2_flx[:,1],linewidth=2,color='gray') #Multiply by 100, from site
#rh237, =plt.plot(rh237_fl[165:,0],rh237_fl[165:,1]*100,linewidth=2,color='gray',linestyle='dashed',label='RH237') #Multiply by 100, from site

#Print legends after plotting, use 'label' from above
#plt.legend(handles=[rhod2,rh237],loc='upper left',ncol=2, prop={'size':16},numpoints=1,frameon=False,bbox_to_anchor=(0, 1.2))

plt.xlim(xmin=451,xmax=849)
plt.ylim(ymin=0,ymax=100)
ax=plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.tick_params(axis='x', which='both',bottom='on',top='off')
ax.tick_params(axis='y', which='both',right='off',left='on')

plt.text(518,28,'Excitation',ha='left',va='bottom',fontsize=16, rotation=90)
plt.text(578,28,'Rhod-2',ha='left',va='bottom',fontsize=16, rotation=90)
plt.text(670,28,'Em. Dichroic',ha='left',va='bottom',fontsize=16, rotation=90)
plt.text(718,28,'RH237',ha='left',va='bottom',fontsize=16, rotation=90)

plt.ylabel('Filter \nTransmission (%)',fontsize=16)
plt.xlabel('Wavelength (nm)',fontsize=16)

plt.tight_layout()
#plt.savefig('passbands.pdf')