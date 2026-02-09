#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def plot_wave_against_PCA_recon_waveform(data,PCA, trans, n, comp_start, comp_end,c):
    x = np.linspace(0, 127, 128)
    plt.plot(x, np.linspace(0,0,128), color='gray', alpha=0.5, label='PCs')
    plt.plot(x, data[n], color='k', linewidth=2, label="True Waveform")
    num_components_to_plot = 10
    for i in range(num_components_to_plot):
        component_scale = PCA.components_[i] * trans[n][i]
        '''if i < 2:
            component_scale *= PCA.mean_[i] '''  
        plt.plot(x, component_scale, color='gray', alpha=.5)

    components = PCA.components_[comp_start:comp_end]
    coefficients = trans[n, comp_start:comp_end]
    P_wave_projection = np.einsum('i,ij->j', coefficients, components)
    P_wave = P_wave_projection

    plt.plot(x, P_wave, color=c, label='PCA waveform')
    plt.legend()
    plt.xlabel("Time") # Add labels for clarity
    plt.ylabel("Amplitude")
    plt.title("Waveform and PCA Components")
    plt.grid(alpha=0.5)
    plt.show()