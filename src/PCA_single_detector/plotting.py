#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def _check_show():
    plt.tight_layout()
    plt.show(block=True)

def plot_scree(pca):
    print("Generating Scree Plot...")
    var_exp = pca.explained_variance_ratio_
    cum_var_exp = np.cumsum(var_exp)
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.bar(range(1, len(var_exp) + 1), var_exp, alpha=0.5, label='Individual Variance', color='g')
    ax2 = ax1.twinx()
    ax2.step(range(1, len(cum_var_exp) + 1), cum_var_exp, where='mid', label='Cumulative', color='red')
    ax1.set_xlabel('PC Index')
    ax1.set_ylabel('Variance Ratio')
    plt.title('Scree Plot (PCA Information Capture)')
    _check_show()

def plot_pca_components(pca, n_pcs):
    print(f"Plotting {n_pcs} Principal Components...")
    # Handle case where requested PCs exceed available components
    available_pcs = len(pca.components_)
    n_pcs = min(n_pcs, available_pcs)
    
    rows = int(np.ceil(n_pcs / 3))
    fig, axes = plt.subplots(rows, 3, figsize=(15, rows * 3))
    axes = axes.flatten()
    
    for i in range(n_pcs):
        var_pct = pca.explained_variance_ratio_[i] * 100
        axes[i].plot(pca.components_[i])
        axes[i].set_title(f"PC {i+1} ({var_pct:.2f}%)")
        axes[i].grid(True, alpha=0.3)
        
    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')
        
    _check_show()

def plot_mean_std(p_feat, i_feat, label):
    print(f"Plotting Mean and Std for: {label}")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    if p_feat is not None and len(p_feat) > 0:
        p_avg = np.mean(p_feat, axis=0)
        ax1.plot(p_avg[:128], color='purple', label='Proton Mean')
        ax2.plot(p_avg[128:], color='purple', linestyle='--', label='Proton Std')
    
    if i_feat is not None and len(i_feat) > 0:
        i_avg = np.mean(i_feat, axis=0)
        ax1.plot(i_avg[:128], color='orange', label='Iron Mean')
        ax2.plot(i_avg[128:], color='orange', linestyle='--', label='Iron Std')
        
    ax1.set_title(f"Mean Waveform: {label}")
    ax1.legend()
    ax2.set_title("Standard Deviation (Fluctuation)")
    ax2.legend()
    _check_show()

def plot_3d_variance_grid(p_trans, i_trans, p_meta, i_meta, color_attr="xmax"):
    print(f"Plotting 3D Variance Grid (Color attribute: {color_attr})")
    fig = plt.figure(figsize=(16, 12))
    groups = [(0,1,2), (3,4,5), (6,7,8), (9,10,11)]
    labels = {
        "xmax": "Xmax (g/cm^2)", 
        "energy": "log10(Energy)", 
        "particle": "Particle ID", 
        "radius": "Avg Radius (km)"
    }
    
    p_sc, i_sc = None, None
    
    for idx, (cx, cy, cz) in enumerate(groups):
        # Ensure we don't index beyond available PCA components
        total_comp = p_trans.shape[1] if len(p_trans) > 0 else i_trans.shape[1]
        if cz >= total_comp:
            continue
            
        ax = fig.add_subplot(2, 2, idx + 1, projection='3d')
        
        if len(p_trans) > 0:
            p_colors = [m[color_attr] for m in p_meta]
            p_sc = ax.scatter(p_trans[:, cx], p_trans[:, cy], p_trans[:, cz], 
                              c=p_colors, cmap='viridis', marker='o', label='Proton', alpha=0.6)
        
        if len(i_trans) > 0:
            i_colors = [m[color_attr] for m in i_meta]
            i_sc = ax.scatter(i_trans[:, cx], i_trans[:, cy], i_trans[:, cz], 
                              c=i_colors, cmap='magma', marker='^', label='Iron', alpha=0.6)
        
        ax.set_title(f"PCs: {cx+1}, {cy+1}, {cz+1}")
        ax.set_xlabel(f"PC{cx+1}")
        ax.set_ylabel(f"PC{cy+1}")
        ax.set_zlabel(f"PC{cz+1}")

    # Add Colorbar
    ref_sc = p_sc if p_sc is not None else i_sc
    if ref_sc:
        cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
        fig.colorbar(ref_sc, cax=cbar_ax, label=labels.get(color_attr, color_attr))
    
    fig.suptitle(f"3D PCA Variance Grid - Colored by {color_attr.upper()}")
    _check_show()

def plot_radius_sweep(sweep_data):
    print("Plotting Radius Sweep Summary...")
    plt.figure(figsize=(8, 5))
    radii = [d['r'] for d in sweep_data]
    seps = [d['s'] for d in sweep_data]
    
    plt.plot(radii, seps, 'ro-', linewidth=2)
    plt.xlabel("Radius (km)")
    plt.ylabel("Separation Power")
    plt.title("Discrimination Efficiency vs. Distance")
    plt.grid(True, linestyle='--', alpha=0.7)
    _check_show()