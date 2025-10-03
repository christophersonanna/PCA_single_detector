# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd 

import z_config as config
import c_split_events_waveform_extraction as extract

from b_perameter_extraction import data_df
from f_a_get_mc import proton_data, iron_data
from d_waveform_pca import PCA_single_detector
from e_visualization_plotting import waveform_PCA_visualization

#need to figure out how to make the columns not casesensitive 
    #one dataframe has a parameter ClockCount and the other is clockcount
#for now...
data_df['clockcount']=data_df['ClockCount']


#needs fixing --> add a def to find only clockcount in waveform extraction script
def extract_waveforms_clockcount(dataframe):
    fadc0_list = []
    fadc1_list = []
    clockcount_list = []

    for event_idx in range(len(dataframe)):
        event_fadc0 = dataframe['FADC0'].iloc[event_idx]
        event_fadc1 = dataframe['FADC1'].iloc[event_idx]
        event_clockcount = dataframe['clockcount'].iloc[event_idx]

        # Calculate number of waveforms per event
        num_waveforms_fadc0 = len(event_fadc0) // config.WAVEFORM_LENGTH
        num_waveforms_fadc1 = len(event_fadc1) // config.WAVEFORM_LENGTH
        num_clockcount = len(event_clockcount)

        # Extract individual waveforms by slicing
        for i in range(num_waveforms_fadc0):
            fadc0_list.append(event_fadc0[i * config.WAVEFORM_LENGTH:(i + 1) * config.WAVEFORM_LENGTH])

        for i in range(num_waveforms_fadc1):
            fadc1_list.append(event_fadc1[i * config.WAVEFORM_LENGTH:(i + 1) * config.WAVEFORM_LENGTH])
        
        for i in range(num_clockcount):
            clockcount_list.append(event_clockcount[i])
    return fadc0_list, fadc1_list, clockcount_list


# Proton Data Processing
print("\nProton Data")
fadc0_p, fadc1_p, clockcount_p = extract_waveforms_clockcount(proton_data)
fadc0_p = [arr for arr in fadc0_p if np.sum(arr) != 0]
fadc1_p = [arr for arr in fadc1_p if np.sum(arr) != 0]
clockcount_p = [arr for arr in clockcount_p if arr != 0]

# Iron Data Processing
print("\nIron Data")
fadc0_f, fadc1_f, clockcount_f = extract_waveforms_clockcount(iron_data)
fadc0_f = [arr for arr in fadc0_f if np.sum(arr) != 0]
fadc1_f = [arr for arr in fadc1_f if np.sum(arr) != 0]
clockcount_f = [arr for arr in clockcount_f if arr != 0]

#%%combine time and fadc
time_fadc0_p = []
time_fadc1_p = []
for i in range(len(clockcount_p)):
    detector0 = []
    detector0.append(clockcount_p[i])
    for j in range(len(fadc0_p[i])):
        detector0.append(fadc0_p[i][j])
    time_fadc0_p.append(detector0)
for i in range(len(clockcount_p)):
    detector1 = []
    detector1.append(clockcount_p[i])
    for j in range(len(fadc1_p[i])):
        detector1.append(fadc1_p[i][j])
    time_fadc1_p.append(detector1)


#%%pca
time_fadc0_pca_p, transformed_time_fadc0_pca_p= PCA_single_detector(time_fadc0_p)

time_fadc1_pca_p, transformed_time_fadc1_pca_p= PCA_single_detector(time_fadc1_p)

#%%visualizing
waveform_PCA_visualization(time_fadc0_pca_p, 'Clockcount and FADC0', 'red')

waveform_PCA_visualization(time_fadc1_pca_p, 'Clockcount and FADC1', 'red')

#%%