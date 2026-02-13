#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# modules/plotting.py
import matplotlib.pyplot as plt
import numpy as np
from core import config

def plot_scree_and_pcs(pca_result, title_prefix=""):
    """Plots the explained variance (Scree) and the first 25 Principal Components."""
    pca = pca_result.pca
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Scree Plot
    x = np.arange(1, len(pca.explained_variance_ratio_) + 1)
    ax1.bar(x, pca.explained_variance_ratio_, alpha=0.6, color='darkorange')
    ax1.plot(x, np.cumsum(pca.explained_variance_ratio_), marker='o', color='navy')
    ax1.set_title(f"{title_prefix} Scree Plot")
    ax1.set_xlabel("Component")
    ax1.set_ylabel("Explained Variance")

    # Visualize first few components (e.g., 9 in a 3x3 grid)
    fig2, axes = plt.subplots(3, 3, figsize=(10, 10))
    for i, ax in enumerate(axes.flat):
        if i < len(pca.components_):
            ax.plot(pca.components_[i], color='blue')
            ax.set_title(f"PC {i+1}")
    plt.tight_layout()
    plt.savefig(f"{title_prefix.lower().replace(' ', '_')}_components.png")

def plot_events_by_primary(res, x_feat="mean_PC1", y_feat="mean_PC2"):
    """Scatter plot of events in PC space, colored by particle type (Proton/Iron)."""
    plt.figure(figsize=(8, 6))
    ix = res.feature_names.index(x_feat)
    iy = res.feature_names.index(y_feat)
    
    for p_id, label, color in [(config.PROTON, "Proton", "red"), (config.IRON, "Iron", "blue")]:
        mask = res.primary == p_id
        if np.any(mask):
            plt.scatter(res.features[mask, ix], res.features[mask, iy], 
                        label=label, color=color, alpha=0.5, s=10)
    
    plt.xlabel(x_feat)
    plt.ylabel(y_feat)
    plt.legend()
    plt.title(f"Event Distribution: {x_feat} vs {y_feat}")
    plt.savefig(f"scatter_{x_feat}_{y_feat}.png")


'''#Scree plot and PC visualization
#may want to add a comparison between multiple PCAs (probably a different script that
#   uses the ones before this)

"""Need to simplify these to make a single def more versatile"""

# Importing
import matplotlib.pyplot as plt
import numpy as np
from config import PLOT_PRINCIPLE_COMPONENTS as NumPC

#Plot of a single PCA: Scree plot and visualization of the first 25 PCs
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

    # Visualize the first 25 PCs
    fig, ax = plt.subplots(int(np.sqrt(NumPC)), int(np.sqrt(NumPC)), figsize=(10, 10),sharey=True, constrained_layout=True)
    for i, ax_this in enumerate(ax.flat):
        ax_this.axhline(0,c='k',linewidth=0.5,alpha=0.5)
        ax_this.plot(pca.components_[i], c=color)
        #ax_this.axes.get_yaxis().set_visible(False)
        ax_this.axes.get_xaxis().set_visible(False)
        ax_this.set_ylim(-0.5,0.5)
        ax_this.set_xlim(0,128)
        ax_this.set_title(f"PC{i+1}")
    #fig.suptitle(label+f" Principle Components\n From {len(extract.fadc0_singdec)} detector waveforms") #need to figure out how to make this data specific
    fig.suptitle(label+" Principle Components")
    plt.show()


#Plots upper and lower trace single PCA together for one dataset
#!!!techincally, I could combine all the definitions together, but that's a clean up thing for later.
def upper_and_lower_waveform_PCA_visualization(upper_pca, lower_pca, label, color):
    # Visualize the first 25 PCs
    fig, ax = plt.subplots(int(np.sqrt(NumPC)), int(np.sqrt(NumPC)), figsize=(10, 10),sharey=True, constrained_layout=True)
    for i, ax_this in enumerate(ax.flat):
        ax_this.axhline(0,c='k',linewidth=0.5,alpha=0.5)
        ax_this.plot(upper_pca.components_[i], c=color,label='Upper')
        ax_this.plot(lower_pca.components_[i], c='k',label='Lower')
        #ax_this.axes.get_yaxis().set_visible(False)
        ax_this.axes.get_xaxis().set_visible(False)
        ax_this.set_ylim(-0.5,0.5)
        ax_this.set_xlim(0,128)
        ax_this.set_title(f"PC{i}")
    handles, labels = ax_this.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper left')
    fig.suptitle(label+" Principle Components\n")
    plt.show()
    
#Plotting 2 different PCA for comparison
def PCA_comparisons(pca1, pca2, ID1, ID2, label, color1, color2):
    fig, ax = plt.subplots(int(np.sqrt(NumPC)), int(np.sqrt(NumPC)), figsize=(10, 10),sharey=True, constrained_layout=True)
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

#Plotting 3 PCA for comparison
def PCA3_comparisons(pca1, pca2, pca3,label):
    fig, ax = plt.subplots(int(np.sqrt(NumPC)), int(np.sqrt(NumPC)), figsize=(10, 10),sharey=True, constrained_layout=True)
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

# Project the PCA data in the first 3 PCs and display them in a 3D scatter plot
def variance_plot(data_after_pca, label, color):
    fig = plt.figure(figsize=(7,6))
    ax = fig.add_subplot(projection='3d')
    cs = ax.scatter(data_after_pca[:,0], data_after_pca[:,1], data_after_pca[:,2], color=color)

    ax.view_init(30, -60)  # change these two numbers to rotate the view 
                           # TO DO: MAKE THIS A USER CHOSE IN TERMINAL
    
    ax.set_xlabel("PC 1")
    ax.set_ylabel("PC 2")
    ax.set_zlabel("PC 3")
    plt.colorbar(cs, label=" ", shrink=0.7)
    plt.title(label)
    fig.tight_layout()'''