#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import config

def reconstruct_waveform(pca_model, mean_vector, pc_scores):
    """
    Reconstructs a waveform: Wave = Mean + (PC1 * score1) + (PC2 * score2) ...
    """
    # inverse_transform does the math: mean_ + pc_scores @ components_
    reconstructed = pca_model.inverse_transform(pc_scores)
    return reconstructed

def plot_pc_influence(pca_model, mean_vector, pc_index=0, std_steps=[-2, 0, 2]):
    """
    Shows how a single PC changes the mean waveform.
    pc_index: 0 for PC1, 1 for PC2, etc.
    std_steps: How many standard deviations to move along the axis.
    """
    plt.figure(figsize=(12, 6))
    
    # Calculate the standard deviation (scale) of this PC from the explained variance
    # eigenvalues = explained_variance_
    scale = np.sqrt(pca_model.explained_variance_[pc_index])

    for step in std_steps:
        # Create a score vector where only the target PC is active
        scores = np.zeros(pca_model.n_components_)
        scores[pc_index] = step * scale
        
        waveform = reconstruct_waveform(pca_model, mean_vector, scores)
        
        # Split into EM and Muon if using your 128+128 format
        label = f"PC{pc_index+1} at {step}σ"
        plt.plot(waveform[:128], label=label, alpha=0.8 if step != 0 else 1.0, 
                 linewidth=2 if step == 0 else 1)

    plt.title(f"Physical Effect of Principal Component {pc_index+1}")
    plt.xlabel("Time Bin")
    plt.ylabel("Reconstructed Amplitude")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def compare_reconstruction(original, reconstructed, event_id=""):
    """Compares the real raw data vs the PCA-compressed version."""
    plt.figure(figsize=(10, 5))
    plt.plot(original, label="Original Data", color='gray', alpha=0.5)
    plt.plot(reconstructed, label="PCA Reconstruction", color='red', linestyle='--')
    plt.title(f"PCA Fidelity Check: Event {event_id}")
    plt.legend()
    plt.show()