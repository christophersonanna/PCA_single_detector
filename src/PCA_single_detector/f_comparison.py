# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 14:26:57 2025

@author: anna
"""

# Library Import
import matplotlib.pyplot as plt
import d_waveform_pca as wave_pca

#%% definitions 
def PCA_comparisons(pca1, pca2, ID1, ID2, label, color1, color2):
    fig, ax = plt.subplots(5, 5, figsize=(10, 10),sharey=True, constrained_layout=True)
    for i, ax_this in enumerate(ax.flat):
        ax_this.axhline(0,c='k',linewidth=0.5,alpha=0.5)
        ax_this.plot(pca2.components_[i], c=color2,label=ID2)
        ax_this.plot(pca1.components_[i], c=color1,label=ID1)
        ax_this.axes.get_xaxis().set_visible(False)
        ax_this.set_ylim(-0.5,0.5)
        ax_this.set_xlim(0,128)
        ax_this.set_title(f"PC{i}")
    handles, labels = ax_this.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper left')
    fig.suptitle(label+" Principle Components")
    plt.show()
    
def PCA3_comparisons(pca1, pca2, pca3,label):
    fig, ax = plt.subplots(5, 5, figsize=(10, 10),sharey=True, constrained_layout=True)
    for i, ax_this in enumerate(ax.flat):
        ax_this.axhline(0,c='k',linewidth=0.5,alpha=0.5)
        ax_this.plot(pca1.components_[i], c='k',label='General')
        ax_this.plot(pca2.components_[i], c='red',label="Proton")
        ax_this.plot(pca3.components_[i], c='blue',label="Iron")
        ax_this.axes.get_xaxis().set_visible(False)
        ax_this.set_ylim(-0.5,0.5)
        ax_this.set_xlim(0,128)
        ax_this.set_title(f"PC{i}")
    handles, labels = ax_this.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper left')
    fig.suptitle(label+" Principle Components")
    plt.show()

#%% Main execution for proton and iron data
# Applying PCA to Proton and Iron FADC0 data.
#PCA_comparisons(wave_pca.Ppca_fadc0, wave_pca.FADC0_PCA, "Proton", "General", "FADC0", "red", 'k')
#PCA_comparisons(wave_pca.Ipca_fadc0, wave_pca.FADC0_PCA, "Iron", "General", "FADC0", "blue", 'k')
PCA_comparisons(wave_pca.Ppca_fadc0, wave_pca.Ipca_fadc0, "Proton", "Iron", "FADC0", "red", 'blue')

#PCA_comparisons(wave_pca.Ppca_fadc1, wave_pca.FADC1_PCA, "Proton", "General", "FADC1", "red", 'k')
#PCA_comparisons(wave_pca.Ipca_fadc1, wave_pca.FADC1_PCA, "Iron", "General", "FADC1", "blue", 'k')
PCA_comparisons(wave_pca.Ppca_fadc1, wave_pca.Ipca_fadc1, "Proton", "Iron", "FADC1", "red", 'blue')

#%%# 
#PCA3_comparisons(wave_pca.FADC0_PCA,wave_pca.Ppca_fadc0,wave_pca.Ipca_fadc0,"FADC0")
#PCA3_comparisons(wave_pca.FADC1_PCA,wave_pca.Ppca_fadc1,wave_pca.Ipca_fadc1,"FADC1")

#%%
