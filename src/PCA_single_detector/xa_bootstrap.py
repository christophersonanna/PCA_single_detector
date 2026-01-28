#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 11:00:48 2025

@author: anna
"""

import numpy as np
from scipy.stats import bootstrap
import matplotlib.pyplot as plt
import pandas as pd

from f_get_mc import proton_data, iron_data
import b_perameter_extraction as extract
from c_split_events_waveform_extraction import fadc_single_detector_array, extract_waveforms
from d_waveform_pca import PCA_single_detector
from e_visualization_plotting import waveform_PCA_visualization,PCA_comparisons, PCA3_comparisons,upper_and_lower_waveform_PCA_visualization
from e_visualization_plotting import variance_plot
from z_config import PLOT_PRINCIPLE_COMPONENTS as NumPC
#import g_residual_pca

'''Extracting Waveforms'''
# Proton Data Processing
fadc0_p, fadc1_p = extract_waveforms(proton_data)
fadc0_p = [arr for arr in fadc0_p if np.sum(arr) != 0]
fadc1_p = [arr for arr in fadc1_p if np.sum(arr) != 0]

# Iron Data Processing
fadc0_f, fadc1_f = extract_waveforms(iron_data)
fadc0_f = [arr for arr in fadc0_f if np.sum(arr) != 0]
fadc1_f = [arr for arr in fadc1_f if np.sum(arr) != 0]

#%%
fadc0_p = pd.DataFrame(fadc0_p)
fadc0_f = pd.DataFrame(fadc0_f)

fadc0 = pd.concat([fadc0_p, fadc0_f], ignore_index = True)
#%%bootstrap

def boot_strap(data, num_boot, num_event):
    data_df = pd.DataFrame(data)
    boots_pca = []
    for i in range(0,num_boot):
        boot = data_df.sample(replace=True, n=num_event, random_state=10)
        boot_pca, trans_boot_pca = PCA_single_detector(boot)
        boots_pca.append(boot_pca)

    boot_pca_mean = []
    boot_pca_std = []

    for i in range(0,len(boots_pca[0].components_)):
        mean_comp = []
        std_comp = []
        for j in range(0,len(boots_pca[0].components_[i])):   
            Data = []
            for k in range(0,len(boots_pca)):
                Data.append(boots_pca[k].components_[i][j])
            dataset = np.array(Data)
            mean = dataset.mean(axis=0)
            std = dataset.std(axis=0)
            mean_comp.append(mean)
            std_comp.append(std)
        boot_pca_mean.append(mean_comp)
        boot_pca_std.append(std_comp)
    return boot_pca_mean,boot_pca_std

def boot_waveform_PCA_visualization(pca_mean, pca_std, label, color):
    # Visualize the first 10 PCs
    fig, ax = plt.subplots(2,5, figsize=(10, 6),sharey=True, constrained_layout=True)
    for i, ax_this in enumerate(ax.flat):
        ax_this.axhline(0,c='k',linewidth=0.5,alpha=0.5)
        ax_this.plot(pca_mean[i], c=color)
        x = np.linspace(0, 127, 128)
        ax_this.errorbar(x, pca_mean[i], yerr = pca_std[i], capsize=1, barsabove=True, color = 'k')
        #ax_this.axes.get_yaxis().set_visible(False)
        ax_this.axes.get_xaxis().set_visible(False)
        ax_this.set_ylim(-0.3,0.3)
        ax_this.set_xlim(0,128)
        ax_this.set_title(f"PC{i+1}")
    #fig.suptitle(label+f" Principle Components\n From {len(extract.fadc0_singdec)} detector waveforms") #need to figure out how to make this data specific
    fig.suptitle(label+" Principle Components")
    plt.show()

#%%
'''
#Proton
boot_mean_fadc0_p, boot_std_fadc0_p = boot_strap(fadc0_p, 50, 100000)
boot_waveform_PCA_visualization(boot_mean_fadc0_p, boot_std_fadc0_p, 'FADC0 Proton Bootstrap', 'red')

boot_mean_fadc1_p, boot_std_fadc1_p = boot_strap(fadc1_p, 50, 100000)
boot_waveform_PCA_visualization(boot_mean_fadc1_p, boot_std_fadc1_p, 'FADC1 Proton Bootstrap', 'red')

#Iron
boot_mean_fadc0_f, boot_std_fadc0_f = boot_strap(fadc0_f, 50, 100000)
boot_waveform_PCA_visualization(boot_mean_fadc0_p, boot_std_fadc0_p, 'FADC0 Iron Bootstrap', 'blue')

boot_mean_fadc1_f, boot_std_fadc1_f = boot_strap(fadc1_f, 50, 100000)
boot_waveform_PCA_visualization(boot_mean_fadc0_p, boot_std_fadc0_p, 'FADC1 Iron Bootstrap', 'blue')
'''
boot_mean_fadc0, boot_std_fadc0 = boot_strap(fadc0, 50, 100000)
boot_waveform_PCA_visualization(boot_mean_fadc0, boot_std_fadc0, 'FADC0 Proton Bootstrap', 'red')



