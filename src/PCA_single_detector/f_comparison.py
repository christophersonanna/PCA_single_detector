# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 14:26:57 2025

@author: anna
"""

# Library Import
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix

# import data
proton_data1 = pd.read_parquet('/home/anna/Downloads/processed_tree_14_MC.parquet')
proton_data2 = pd.read_parquet('/home/anna/Downloads/processed_tree_14_MC_pt2.parquet')
proton_data = pd.concat([proton_data1,proton_data2], ignore_index=True)

iron_data1 = pd.read_parquet('/home/anna/Downloads/processed_tree_5426_MC.parquet')
iron_data2 = pd.read_parquet('/home/anna/Downloads/processed_tree_2654_MC_pt2.parquet')
iron_data = pd.concat([iron_data1, iron_data2], ignore_index=True)

parquet_file = pd.read_parquet('/home/anna/Machine_Learning_Xmax/data/processed_tree_sample.parquet')
data = parquet_file[parquet_file['NSpaceCluster'] > 4].reset_index(drop=True) #write in function new var

# Configuration Constants_PFE_MC_single_detector_25PC.parquet'
N_COMPONENTS_PCA = 128
WAVEFORM_LENGTH = 128
PROTON = 14
IRON = 5626

#%% definitions
# Waveform Extraction
def extract_waveforms(dataframe):
    fadc0_list = []
    fadc1_list = []

    for event_idx in range(len(dataframe)):
        event_fadc0 = dataframe['FADC0'].iloc[event_idx]
        event_fadc1 = dataframe['FADC1'].iloc[event_idx]

        # Calculate number of waveforms per event
        num_waveforms_fadc0 = len(event_fadc0) // WAVEFORM_LENGTH
        num_waveforms_fadc1 = len(event_fadc1) // WAVEFORM_LENGTH

        # Extract individual waveforms by slicing
        for i in range(num_waveforms_fadc0):
            fadc0_list.append(event_fadc0[i * WAVEFORM_LENGTH:(i + 1) * WAVEFORM_LENGTH])

        for i in range(num_waveforms_fadc1):
            fadc1_list.append(event_fadc1[i * WAVEFORM_LENGTH:(i + 1) * WAVEFORM_LENGTH])

    return fadc0_list, fadc1_list

# PCA
def PCA_fadc(dataframe):
    data_array = np.array(dataframe)
    pca = PCA(n_components=N_COMPONENTS_PCA)
    transformed_data = pca.fit_transform(data_array)
    return pca, transformed_data
    
# visualizing
def PCA_visualization(pca, ID, label, color,Data):
    
    '''# Make Scree plot (FADC0)
    fig, ax = plt.subplots()
    x = np.arange(1, pca.n_components_+1)
    ax.bar(x, pca.explained_variance_ratio_, align="center", color='darkorange', alpha=0.6)
    ax.set_title(ID+""+label+' Scree Plot')
    ax.set_xlabel('n-th component')
    ax.set_ylabel('Explained variance ratio (per component)', color='darkorange')
    ax.set_ylim(0, 1.05)
    ax.grid()

    ax2 = ax.twinx()
    ax2.plot(x, np.cumsum(pca.explained_variance_ratio_), color=color, lw=2)
    ax2.set_ylabel('Explained variance ratio (cumulative)', color=color)
    ax2.axline((0,1),(200,1), linewidth = 0.5, color='black')
    ax2.set_ylim(0, 1.05);
    ax2.set_xlim(0,25);
    #plt.showt()
    '''
    # Visualize the first 5 PCs
    fig, ax = plt.subplots(5, 5, figsize=(10, 10),sharey=True, constrained_layout=True)
    for i, ax_this in enumerate(ax.flat):
        ax_this.axhline(0,c='k',linewidth=0.5,alpha=0.5)
        ax_this.plot(pca.components_[i], c=color)
        #ax_this.plot(MCpca.components_[i], c=color)
        ax_this.axes.get_xaxis().set_visible(False)
        ax_this.set_ylim(-0.5,0.5)
        ax_this.set_xlim(0,128)
        ax_this.set_title(f"PC{i}")
    fig.suptitle(ID+" "+label+f" Principle Components\n From {len(Data)} detector waveforms from "+ ID + " events")
    plt.show()    

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

#%% Main execution for proton and iron data

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

#General data Processing
print("\nGeneral MC Data")
fadc0_Gen, fadc1_Gen = extract_waveforms(data)
print(f"Extracted {len(fadc0_Gen)} single FADC0 waveforms for General MC.")

# Applying PCA to Proton and Iron FADC0 data.
Ppca_fadc0, transformed_Ppca_fadc0 = PCA_fadc(fadc0_p)
Ipca_fadc0, transformed_Ipca_fadc0 = PCA_fadc(fadc0_f)
Gpca_fadc0, transformed_Gpca_fadc0 = PCA_fadc(fadc0_Gen)

PCA_visualization(Ppca_fadc0, "Proton", "FADC0", 'red',transformed_Ppca_fadc0)
PCA_visualization(Ipca_fadc0, "Iron", "FADC0", 'blue',transformed_Ipca_fadc0)
PCA_visualization(Gpca_fadc0, "General", "FADC0", 'k',transformed_Gpca_fadc0)

PCA_comparisons(Ppca_fadc0, Gpca_fadc0, "Proton", "General", "FADC0", "red", 'k')
PCA_comparisons(Ipca_fadc0, Gpca_fadc0, "Iron", "General", "FADC0", "blue", 'k')
PCA_comparisons(Ppca_fadc0, Ipca_fadc0, "Proton", "Iron", "FADC0", "red", 'blue')

# Applying PCA to Proton and Iron FADC1 data.
Ppca_fadc1, transformed_Ppca_fadc1 = PCA_fadc(fadc1_p)
Ipca_fadc1, transformed_Ipca_fadc1 = PCA_fadc(fadc1_f)
Gpca_fadc1, transformed_Gpca_fadc1 = PCA_fadc(fadc1_Gen)

PCA_visualization(Ppca_fadc1, "Proton", "FADC1", 'red',transformed_Ppca_fadc1)
PCA_visualization(Ipca_fadc1, "Iron", "FADC1", 'blue',transformed_Ipca_fadc1)
PCA_visualization(Gpca_fadc1, "General", "FADC1", 'k',transformed_Gpca_fadc1)

PCA_comparisons(Ppca_fadc1, Gpca_fadc1, "Proton", "General", "FADC1", "red", 'k')
PCA_comparisons(Ipca_fadc1, Gpca_fadc1, "Iron", "General", "FADC1", "blue", 'k')
PCA_comparisons(Ppca_fadc1, Ipca_fadc1, "Proton", "Iron", "FADC1", "red", 'blue')

#%%# 
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

PCA3_comparisons(Gpca_fadc0,Ppca_fadc0,Ipca_fadc0,"FADC0")
PCA3_comparisons(Gpca_fadc1,Ppca_fadc1,Ipca_fadc1,"FADC1")

#%%
