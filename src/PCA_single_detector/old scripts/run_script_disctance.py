#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 11:23:01 2026

@author: anna
"""
import numpy as np

import z_config as config
from c_split_events_waveform_extraction import normalize_waveform
from f_get_mc import proton_data, iron_data
from d_waveform_pca import PCA_single_detector
from e_visualization_plotting import waveform_PCA_visualization,upper_and_lower_waveform_PCA_visualization

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
    r5_up = []

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
            r5_up.append(data[i])
    return core, r1, r2, r3, r4, r5_up

#%%splitting
'Proton'
fadc0_p_core, fadc0_p_r1, fadc0_p_r2, fadc0_p_r3, fadc0_p_r4, fadc0_p_r5 = splitting_radius(fadc0_p,rad_p)
fadc1_p_core, fadc1_p_r1, fadc1_p_r2, fadc1_p_r3, fadc1_p_r4, fadc1_p_r5 = splitting_radius(fadc1_p,rad_p)
'Iron'
fadc0_f_core, fadc0_f_r1, fadc0_f_r2, fadc0_f_r3, fadc0_f_r4, fadc0_f_r5 = splitting_radius(fadc0_f,rad_f)
fadc1_f_core, fadc1_f_r1, fadc1_f_r2, fadc1_f_r3, fadc1_f_r4, fadc1_f_r5 = splitting_radius(fadc1_f,rad_f)

#%%
def norm_pca_and_visualize(primary, up_low, core, r1, r2, r3, r4, r5):
    list = [core, r1, r2, r3, r4, r5]
    color = ['red', 'orange', 'green', 'blue', 'purple']
    for i in range(0,len(list)):
        list[i] = [arr for arr in list[i] if np.sum(arr) != 0]
        Norm_list = normalize_waveform(list[i], True)
        Pca, transformed_Pca = PCA_single_detector(Norm_list)
        waveform_PCA_visualization(Pca, primary+' '+up_low+' '+str(list[i]), color[i])

    
norm_pca_and_visualize('Proton', "FADC0", fadc0_p_core, fadc0_p_r1, fadc0_p_r2, fadc0_p_r3, fadc0_p_r4, fadc0_p_r5)
norm_pca_and_visualize('Proton', "FADC1", fadc1_p_core, fadc1_p_r1, fadc1_p_r2, fadc1_p_r3, fadc1_p_r4, fadc1_p_r5)

norm_pca_and_visualize('Iron', "FADC0", fadc0_f_core, fadc0_f_r1, fadc0_f_r2, fadc0_f_r3, fadc0_f_r4, fadc0_f_r5)
norm_pca_and_visualize('Iron', "FADC1", fadc1_f_core, fadc1_f_r1, fadc1_f_r2, fadc1_f_r3, fadc1_f_r4, fadc1_f_r5)
