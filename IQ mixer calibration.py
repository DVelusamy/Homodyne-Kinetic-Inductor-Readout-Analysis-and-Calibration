#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 18:55:52 2021

@author: deepikavelusamy
"""

import numpy as np
from numpy import cos as cos
from numpy import sin as sin
from numpy import tan as tan
from numpy import arcsin as Asin
from numpy import arctan as Atan
from numpy import sqrt as sqrt
from numpy import pi as pi
from numpy import log10 as log10

from scipy.interpolate import interp1d

import matplotlib.pyplot as plt
import matplotlib


plt.close('all')




c=3e8   #Speed of light

sim_points=50 #Number of points to simulate

F_min=1e9 # Minimum frequency point to be simulated
F_max=2e9 # Maximum frequency point to be simulated

line_L=0.020   #Physical Length of an ideal transmission line between spliiter and RF port

line_er=2.1  #Permitivity of transmission line dielectric 

Amp=1.   #Amplitude of signal before splitter in volts

freq=np.linspace(F_min,F_max,sim_points)   #Make an array of frequency points to simulate


vp=c/sqrt(line_er)  #Phase velocity on transmission line. 

WL=vp/freq

phi=(line_L/WL)*2.*pi   # Work out the phase of teh signal after passing through a given length of ideal (loss less) transmission line


phi=np.linspace(0,360, sim_points)   #Create a phase shift between 0 and 360 for demonstration


phi=(phi/360.)*2*pi


I_ideal=0.5*Amp*cos(phi)         #simulate I for an ideal mixer
Q_ideal=0.5*Amp*cos(phi+(pi/2))   #simulate Q for an ideal mixer


#### Create so phase deviations from the ideal 90 degrees between I and Q

#phase_error=[89.,95.,96.,92.,87.,84.,88.,85.,91.,93.]    #Create some sample points for the phase deviation
#phase_error_x=np.linspace(F_min,F_max,10)
#
#f2 = interp1d(phase_error_x,phase_error , kind='cubic')   #Interpolate the sample points over the full frequency space
#
#phase_error=f2(freq)
#phase_error_rads=(phase_error/360.)*2.*pi   #Convert phase error into radians


phase_error=pi/20  # Create a fixed phase error

I_real=0.5*Amp*cos(phi)       #simulate I for an "real" mixer
Q_real=(0.5*Amp*cos(phi+(pi/2)+phase_error))

xx=sqrt((I_real**2)+(Q_real**2))

ang=Atan(Q_real/I_real)


dd=(xx*(sin(phase_error))*cos((ang)))


#Q_real=Q_real/(0.5/0.75)
#I_real=I_real*(0.75/0.5)

Q_cal=Q_real-dd  #make an array that we will overwrite each element in teh for loop


for k, kk, in enumerate (I_real):
    #print(k)
    
    Q_cal[k]=Q_real[k]-dd[k]
    
    if I_real[k] > 0:
        
        Q_cal[k]=Q_real[k]+dd[k]
        
    



Q_cal=Q_cal*(1./(cos(phase_error)))





fig01,ax01 = plt.subplots(1,1)
ax01.plot(I_real,Q_real,'*',label='Mixer with phase imbalance')
ax01.plot(I_ideal,Q_ideal,'*', label='Ideal Mixer')
ax01.plot(I_real,Q_cal,'*', label='Callibrated Q')
ax01.plot(I_real,Q_cal, label='Callibrated Q')
ax01.get_xaxis().get_major_formatter().set_useOffset(False)
plt.ylabel('Q')
plt.xlabel('I')
plt.title('I vs Q')
plt.legend(loc=3)
plt.grid(True)
plt.show()  

S21_ideal=(I_ideal**2)+(Q_ideal**2)
S21_real=(I_real**2)+(Q_real**2)
S21_cal=(I_real**2)+(Q_cal*2)



# =============================================================================
# S21_ideal=(I_ideal**2)+(Q_ideal**2)
# S21_real=(I_real**2)+(Q_real**2)
# S21_cal=(I_real**2)+(Q_cal**2)
# 
# =============================================================================
S21_ideal_dB=10*log10(S21_ideal)
S21_real_dB=10*log10(S21_real)
S21_cal_dB=10*log10(S21_cal)


fig03,ax03 = plt.subplots(1,1)

ax03.plot(freq,S21_real_dB,label='Mixer with phase imbalance') 
ax03.plot(freq,S21_ideal_dB,label='Ideal Mixer') 
ax03.plot(freq,S21_cal_dB,label='Cal Mixer') 
ax03.plot(freq,S21_cal_dB,'*',label='Cal Mixer') 
ax03.get_xaxis().get_major_formatter().set_useOffset(False)
plt.ylabel('S21 / dB')
plt.xlabel('Freq')
plt.title('Simulated S21')
plt.grid(True)
plt.legend(loc=3)
plt.show()  