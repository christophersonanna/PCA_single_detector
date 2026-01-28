#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 11:23:01 2026

@author: anna
"""
import numpy as np

import z_config as config
import matplotlib.pyplot as plt
from f_get_mc import proton_data, iron_data
from d_waveform_pca import PCA_single_detector
from e_visualization_plotting import waveform_PCA_visualization,upper_and_lower_waveform_PCA_visualization
from c_split_events_waveform_extraction import normalize_waveform

def extract_waveforms_radius(dataframe):
    fadc0_list = []
    fadc1_list = []
    radius_list = []

    for event_idx in range(len(dataframe)):
        event_fadc0 = dataframe['FADC0'].iloc[event_idx]
        event_fadc1 = dataframe['FADC1'].iloc[event_idx]
        event_radius = dataframe['radius'].iloc[event_idx]

        # Calculate number of waveforms per event
        num_waveforms_fadc0 = len(event_fadc0) // config.WAVEFORM_LENGTH
        num_waveforms_fadc1 = len(event_fadc1) // config.WAVEFORM_LENGTH
        num_radius = len(event_radius)

        # Extract individual waveforms by slicing
        for i in range(num_waveforms_fadc0):
            fadc0_list.append(event_fadc0[i * config.WAVEFORM_LENGTH:(i + 1) * config.WAVEFORM_LENGTH])

        for i in range(num_waveforms_fadc1):
            fadc1_list.append(event_fadc1[i * config.WAVEFORM_LENGTH:(i + 1) * config.WAVEFORM_LENGTH])
        
        for i in range(num_radius):
            radius_list.append(event_radius[i])
    return fadc0_list, fadc1_list, radius_list

def plot_wave_against_PCA_recon_waveform(data,PCA, trans, n, comp_start, comp_end,c):
    x = np.linspace(0, 127, 128)
    norm_data = []
    for i in range(0,len(data[n])):
        norm_fact = 1/max(data[n][i])
        norm_data.append(norm_fact*(data[n][i]))
    
    plt.plot(x, np.linspace(0,0,128), color='gray', alpha=0.5, label='PCs')
    plt.plot(x, norm_data, color='k', linewidth=2, label="True Waveform")
    num_components_to_plot = 10
    for i in range(num_components_to_plot):
        component_scale = PCA.components_[i] * trans[n][i]
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

#%% normalize wavefunction then PCA
# Proton Data Processing
'''Extracting Waveforms'''
# Proton Data Processing
fadc0_p, fadc1_p, rad_p = extract_waveforms_radius(proton_data)
fadc0_f, fadc1_f, rad_f = extract_waveforms_radius(iron_data)
print('Processing Complete')

#%% splitting by radius
def splitting_radius(data, rad):
    core = []
    r1 = []
    r2 = []
    r3 = []
    r4 = []
    r5 = []
    for i in range(0,len(rad)):
        if rad[i]==0:
            core.append(data[i])
        elif rad[i]==1:
            r1.append(data[i])
        elif rad[i]==2:
            r2.append(data[i])
        elif rad[i]==3:
            r3.append(data[i])
        elif rad[i]==4:
            r4.append(data[i])
        else:
            r5.append(data[i])
    return core, r1, r2, r3, r4, r5

fadc0_p_core, fadc0_p_r1, fadc0_p_r2, fadc0_p_r3, fadc0_p_r4, fadc0_p_r5 = splitting_radius(fadc0_p, rad_p)
fadc1_p_core, fadc1_p_r1, fadc1_p_r2, fadc1_p_r3, fadc1_p_r4, fadc1_p_r5 = splitting_radius(fadc1_p, rad_p)

fadc0_f_core, fadc0_f_r1, fadc0_f_r2, fadc0_f_r3, fadc0_f_r4, fadc0_f_r5 = splitting_radius(fadc0_p, rad_p)
fadc1_f_core, fadc1_f_r1, fadc1_f_r2, fadc1_f_r3, fadc1_f_r4, fadc1_f_r5 = splitting_radius(fadc1_p, rad_p)
    
#%%
def Norm_PCA_and_visual(data, primary, up_low, radius, color):
    data = [arr for arr in data if np.sum(arr) != 0]
    Norm_data = normalize_waveform(data, True)
    Pca, transformed_Pca = PCA_single_detector(Norm_data)
    waveform_PCA_visualization(Pca, primary+' '+up_low+' '+radius, color)
    plot_wave_against_PCA_recon_waveform(data, Pca, transformed_Pca, 1345, 0,128,'red')

#%%proton
color = ['red', 'orange', 'green', 'blue', 'purple']
rad_list = ['R=0','R=1','R=2','R=3','R=4','R=5 and greater']
Pfadc0_list = [fadc0_p_core, fadc0_p_r1, fadc0_p_r2, fadc0_p_r3, fadc0_p_r4, fadc0_p_r5]
Pfadc1_list = [fadc1_p_core, fadc1_p_r1, fadc1_p_r2, fadc1_p_r3, fadc1_p_r4, fadc1_p_r5]
Ffadc0_list = [fadc0_f_core, fadc0_f_r1, fadc0_f_r2, fadc0_f_r3, fadc0_f_r4, fadc0_f_r5]
Ffadc1_list = [fadc1_f_core, fadc1_f_r1, fadc1_f_r2, fadc1_f_r3, fadc1_f_r4, fadc1_f_r5]


for i in range(0, len(Pfadc0_list)):
    Norm_PCA_and_visual(Pfadc0_list[i], 'Proton', "FADC0", rad_list[i], color[i])
#%%
for i in range(0, len(Pfadc0_list)):
    Norm_PCA_and_visual(Pfadc1_list[i], 'Proton', "FADC1", rad_list[i], color[i])
#%%
for i in range(0, len(Pfadc0_list)):
    Norm_PCA_and_visual(Ffadc0_list[i], 'Iron', "FADC0", rad_list[i], color[i])
#%%
for i in range(0, len(Pfadc0_list)):
    Norm_PCA_and_visual(Ffadc1_list[i], 'Iron', "FADC1", rad_list[i], color[i])

#%%

