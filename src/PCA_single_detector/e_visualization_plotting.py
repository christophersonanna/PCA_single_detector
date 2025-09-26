#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Scree plot and PC visualization
#may want to add a comparison between multiple PCAs (probably a different script that
#   uses the ones before this)

#test
# Importing

import matplotlib.pyplot as plt
import numpy as np
import c_split_events_waveform_extraction as extract
import d_waveform_pca as wave_pca

#definition 
def waveform_PCA_visualization(pca, label, color):
    
    # Make Scree plot (FADC0)
    fig, ax = plt.subplots()
    x = np.arange(1, pca.n_components_+1)
    ax.bar(x, pca.explained_variance_ratio_, align="center", color='darkorange', alpha=0.6)
    ax.set_title(label+' Scree Plot')
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
    plt.show()

    # Visualize the first 5 PCs
    fig, ax = plt.subplots(5, 5, figsize=(10, 10),sharey=True, constrained_layout=True)
    for i, ax_this in enumerate(ax.flat):
        ax_this.axhline(0,c='k',linewidth=0.5,alpha=0.5)
        ax_this.plot(pca.components_[i], c=color)
        #ax_this.axes.get_yaxis().set_visible(False)
        ax_this.axes.get_xaxis().set_visible(False)
        ax_this.set_ylim(-0.5,0.5)
        ax_this.set_xlim(0,128)
        ax_this.set_title(f"PC{i}")
    fig.suptitle(label+f" Principle Components\n From {len(extract.fadc0_singdec)} detector waveforms")
    #fig.suptitle(label+" Principle Components")
    plt.show()    

#Applying definition to FADC0 and FADC1 data.
waveform_PCA_visualization(wave_pca.FADC0_PCA, 'FADC0', 'black')
waveform_PCA_visualization(wave_pca.FADC0_PCA, 'FADC1', 'black')