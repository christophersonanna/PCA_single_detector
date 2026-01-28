# -*- coding: utf-8 -*-

import numpy as np
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
fadc1_singdec = fadc_single_detector_array(extract.data_df,'FADC1')
print(f"Extracted {len(fadc0_singdec)} single detector waveforms.")

# Proton Data Processing
print("\nProton Data")
fadc0_p, fadc1_p = extract_waveforms(proton_data)
fadc0_p = [arr for arr in fadc0_p if np.sum(arr) != 0]
fadc1_p = [arr for arr in fadc1_p if np.sum(arr) != 0]
print(f"Extracted {len(fadc0_p)} single FADC0 waveforms for Protons.")

# Iron Data Processing
print("\nIron Data")
fadc0_f, fadc1_f = extract_waveforms(iron_data)
fadc0_f = [arr for arr in fadc0_f if np.sum(arr) != 0]
fadc1_f = [arr for arr in fadc1_f if np.sum(arr) != 0]
print(f"Extracted {len(fadc0_f)} single FADC0 waveforms for Iron.")


'''PCA'''
#running PCA
#FADC0_PCA, transformed_FADC0_data = PCA_single_detector(fadc0_singdec)
Ppca_fadc0, transformed_Ppca_fadc0 = PCA_single_detector(fadc0_p)
Ipca_fadc0, transformed_Ipca_fadc0 = PCA_single_detector(fadc0_f)

#!!!!need to create a condition that MC isn't called unless it needs to be used later

#FADC1_PCA, transformed_FADC1_data = PCA_single_detector(fadc1_singdec)
Ppca_fadc1, transformed_Ppca_fadc1 = PCA_single_detector(fadc1_p)
Ipca_fadc1, transformed_Ipca_fadc1 = PCA_single_detector(fadc1_f)


'''Visualizing'''
'Singles'
#Applying definition to FADC0 and FADC1 data.
#waveform_PCA_visualization(FADC0_PCA, 'FADC0', 'black')
#waveform_PCA_visualization(FADC1_PCA, 'FADC1', 'black')
'Upper and Lower Together'
#upper_and_lower_waveform_PCA_visualization(FADC0_PCA,FADC1_PCA, 'General FADC', 'purple')
upper_and_lower_waveform_PCA_visualization(Ppca_fadc0,Ppca_fadc1, 'Proton FADC', 'blue')
upper_and_lower_waveform_PCA_visualization(Ipca_fadc0,Ipca_fadc1, 'Iron FADC', 'r')
'''Variance'''
#variance_plot(transformed_FADC0_data, 'FADC0')
variance_plot(transformed_Ppca_fadc0, 'proton fadc0', 'red')
variance_plot(transformed_Ipca_fadc0, 'iron fadc0', 'blue')

variance_plot(transformed_Ppca_fadc1, 'proton fadc1','red')
variance_plot(transformed_Ipca_fadc1, 'iron fadc1','blue')

'''Comparison'''
# Main execution for proton and iron data
# Applying PCA to Proton and Iron FADC0 data.
#PCA_comparisons(Ppca_fadc0, FADC0_PCA, "Proton", "General", "FADC0", "red", 'k')
#PCA_comparisons(Ipca_fadc0, FADC0_PCA, "Iron", "General", "FADC0", "blue", 'k')
#PCA_comparisons(Ppca_fadc0, Ipca_fadc0, "Proton", "Iron", "FADC0", "red", 'blue')

#PCA_comparisons(Ppca_fadc1, FADC1_PCA, "Proton", "General", "FADC1", "red", 'k')
#PCA_comparisons(Ipca_fadc1, FADC1_PCA, "Iron", "General", "FADC1", "blue", 'k')
#PCA_comparisons(Ppca_fadc1, Ipca_fadc1, "Proton", "Iron", "FADC1", "red", 'blue')

# 
#PCA3_comparisons(FADC0_PCA,Ppca_fadc0,Ipca_fadc0,"FADC0")
#PCA3_comparisons(FADC1_PCA,Ppca_fadc1,Ipca_fadc1,"FADC1")

'''Residual PCA'''
#not adding it here since it messy at the moment and I don't want to run it unless I absolutely want to

