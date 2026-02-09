#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 11:00:14 2025

@author: anna
"""
import numpy as np
import matplotlib.pyplot as plt
from f_get_mc import proton_data, iron_data
import b_perameter_extraction as extract
from c_split_events_waveform_extraction import fadc_single_detector_array, extract_waveforms
from d_waveform_pca import PCA_single_detector
from e_visualization_plotting import waveform_PCA_visualization,PCA_comparisons, PCA3_comparisons,upper_and_lower_waveform_PCA_visualization
from e_visualization_plotting import variance_plot
#import g_residual_pca

'''Extracting Waveforms'''
#extraction fadc0 and fadc1 of original data
fadc0_singdec = fadc_single_detector_array(extract.data_df, 'FADC0')

# Data Processing
fadc0_p, fadc1_p = extract_waveforms(proton_data)
fadc0_p = [arr for arr in fadc0_p if np.sum(arr) != 0]
fadc1_p = [arr for arr in fadc1_p if np.sum(arr) != 0]
fadc0_f, fadc1_f = extract_waveforms(iron_data)
fadc0_f = [arr for arr in fadc0_f if np.sum(arr) != 0]
fadc1_f = [arr for arr in fadc1_f if np.sum(arr) != 0]
print(f"Extracted {len(fadc0_p)} single FADC0 waveforms for Protons.")

'''PCA'''
#running PCA
FADC0_PCA, transformed_FADC0_data = PCA_single_detector(fadc0_singdec)
Ppca_fadc0, transformed_Ppca_fadc0 = PCA_single_detector(fadc0_p)
Fpca_fadc0, transformed_Fpca_fadc0 = PCA_single_detector(fadc0_f)
#%%
def plot_wave_against_PCA_recon_waveform(data,PCA, trans, n, comp_start, comp_end,c):
    x = np.linspace(0, 127, 128)
    plt.plot(x, np.linspace(0,0,128), color='gray', alpha=0.5, label='PCs')
    plt.plot(x, data[n], color='k', linewidth=2, label="True Waveform")
    num_components_to_plot = 10
    for i in range(num_components_to_plot):
        component_scale = PCA.components_[i] * trans[n][i]
        '''if i < 2:
            component_scale *= PCA.mean_[i] '''  
        plt.plot(x, component_scale, color='gray', alpha=.5)

    components = PCA.components_[comp_start:comp_end]
    coefficients = trans[n, comp_start:comp_end]
    P_wave_projection = np.einsum('i,ij->j', coefficients, components)
    P_wave = P_wave_projection

    plt.plot(x, P_wave, color=c, label='PCA waveform')
    plt.legend()
    plt.xlabel("Time") # Add labels for clarity
    plt.ylabel("Amplitude")
    plt.title("Waveform and PCA Components")
    plt.grid(alpha=0.5)
    plt.show()
    
#%%
plot_wave_against_PCA_recon_waveform(fadc0_p, Ppca_fadc0, transformed_Ppca_fadc0, 500, 0, 128,'r')
plot_wave_against_PCA_recon_waveform(fadc0_p, Ppca_fadc0, transformed_Ppca_fadc0, 501, 2, 128,'r')

plot_wave_against_PCA_recon_waveform(fadc0_p, Ppca_fadc0, transformed_Ppca_fadc0, 1421, 0, 128,'r')
plot_wave_against_PCA_recon_waveform(fadc0_p, Ppca_fadc0, transformed_Ppca_fadc0, 1422, 2, 128,'r')

plot_wave_against_PCA_recon_waveform(fadc0_p, Ppca_fadc0, transformed_Ppca_fadc0, 9454,0, 128,'r')
plot_wave_against_PCA_recon_waveform(fadc0_p, Ppca_fadc0, transformed_Ppca_fadc0, 9455,0, 128,'r')

plot_wave_against_PCA_recon_waveform(fadc0_p, Ppca_fadc0, transformed_Ppca_fadc0, 48399,0, 128,'r')
plot_wave_against_PCA_recon_waveform(fadc0_p, Ppca_fadc0, transformed_Ppca_fadc0, 48400,0, 128,'r')

plot_wave_against_PCA_recon_waveform(fadc0_p, Ppca_fadc0, transformed_Ppca_fadc0, 123996,0, 128,'r')
plot_wave_against_PCA_recon_waveform(fadc0_p, Ppca_fadc0, transformed_Ppca_fadc0, 123997,0, 128,'r')


#%%
plot_wave_against_PCA_recon_waveform(fadc0_f, Fpca_fadc0, transformed_Fpca_fadc0, 500, 0, 15,'b')
plot_wave_against_PCA_recon_waveform(fadc0_f, Fpca_fadc0, transformed_Fpca_fadc0, 501, 2, 15,'b')

plot_wave_against_PCA_recon_waveform(fadc0_f, Fpca_fadc0, transformed_Fpca_fadc0, 1428, 0, 15,'b')
plot_wave_against_PCA_recon_waveform(fadc0_f, Fpca_fadc0, transformed_Fpca_fadc0, 1429, 2, 15,'b')

plot_wave_against_PCA_recon_waveform(fadc0_f, Fpca_fadc0, transformed_Fpca_fadc0, 14254, 0, 15,'b')
plot_wave_against_PCA_recon_waveform(fadc0_f, Fpca_fadc0, transformed_Fpca_fadc0, 14255, 2, 15,'b')

plot_wave_against_PCA_recon_waveform(fadc0_f, Fpca_fadc0, transformed_Fpca_fadc0, 48400, 0, 15,'b')
plot_wave_against_PCA_recon_waveform(fadc0_f, Fpca_fadc0, transformed_Fpca_fadc0, 48399, 2, 15,'b')

plot_wave_against_PCA_recon_waveform(fadc0_f, Fpca_fadc0, transformed_Fpca_fadc0, 124005, 0, 15,'b')
plot_wave_against_PCA_recon_waveform(fadc0_f, Fpca_fadc0, transformed_Fpca_fadc0, 123999, 2, 15,'b')

#%%
x = np.linspace(0,127,128)

#n=14249
n=14254


plt.plot(x,fadc0_f[n], color = 'k', linewidth=2, label = "True Waveform")

#print(transformed_Ppca_fadc0)
plt.plot(x,Fpca_fadc0.components_[0]*transformed_Fpca_fadc0[n][0]*Fpca_fadc0.mean_[0], color = 'gray', alpha = .5)
plt.plot(x,Fpca_fadc0.components_[1]*transformed_Fpca_fadc0[n][1]*Fpca_fadc0.mean_[1], color = 'gray', alpha = .5)
plt.plot(x,Fpca_fadc0.components_[2]*transformed_Fpca_fadc0[n][2], color = 'gray', alpha = .5)
plt.plot(x,Fpca_fadc0.components_[3]*transformed_Fpca_fadc0[n][3], color = 'gray', alpha = .5)
plt.plot(x,Fpca_fadc0.components_[4]*transformed_Fpca_fadc0[n][4], color = 'gray', alpha = .5)
plt.plot(x,Fpca_fadc0.components_[5]*transformed_Fpca_fadc0[n][5], color = 'gray', alpha = .5)
plt.plot(x,Fpca_fadc0.components_[6]*transformed_Fpca_fadc0[n][6], color = 'gray', alpha = .5)
plt.plot(x,Fpca_fadc0.components_[7]*transformed_Fpca_fadc0[n][7], color = 'gray', alpha = .5)
plt.plot(x,Fpca_fadc0.components_[8]*transformed_Fpca_fadc0[n][8], color = 'gray', alpha = .5)
plt.plot(x,Fpca_fadc0.components_[9]*transformed_Fpca_fadc0[n][9], color = 'gray', alpha = .5)

P_wave = (Ppca_fadc0.components_[0]*transformed_Fpca_fadc0[n][0]+#*Ppca_fadc0.mean_[0]+
          Fpca_fadc0.components_[1]*transformed_Fpca_fadc0[n][1]+#*Ppca_fadc0.mean_[1]+
          Fpca_fadc0.components_[2]*transformed_Fpca_fadc0[n][2]+
          Fpca_fadc0.components_[3]*transformed_Fpca_fadc0[n][3]+
          Fpca_fadc0.components_[4]*transformed_Fpca_fadc0[n][4]+
          Fpca_fadc0.components_[5]*transformed_Fpca_fadc0[n][5]+
          Fpca_fadc0.components_[6]*transformed_Fpca_fadc0[n][6]+
          Fpca_fadc0.components_[7]*transformed_Fpca_fadc0[n][7]+
          Fpca_fadc0.components_[8]*transformed_Fpca_fadc0[n][8]+
          Fpca_fadc0.components_[9]*transformed_Fpca_fadc0[n][9]+
          Fpca_fadc0.components_[10]*transformed_Fpca_fadc0[n][10]+
          Fpca_fadc0.components_[11]*transformed_Fpca_fadc0[n][11]+
          Fpca_fadc0.components_[12]*transformed_Fpca_fadc0[n][12]+
          Fpca_fadc0.components_[13]*transformed_Fpca_fadc0[n][13]+
          Fpca_fadc0.components_[14]*transformed_Fpca_fadc0[n][14]+
          Fpca_fadc0.components_[15]*transformed_Fpca_fadc0[n][15]+
          Fpca_fadc0.components_[16]*transformed_Fpca_fadc0[n][16]+
          Fpca_fadc0.components_[17]*transformed_Fpca_fadc0[n][17]+
          Fpca_fadc0.components_[18]*transformed_Fpca_fadc0[n][18]+
          Fpca_fadc0.components_[19]*transformed_Fpca_fadc0[n][19])

plt.plot(x,P_wave, color='red', label = 'PCA waveform')

plt.show()
