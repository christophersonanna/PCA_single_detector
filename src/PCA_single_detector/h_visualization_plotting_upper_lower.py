# -*- coding: utf-8 -*-

#plotting the upper and lower waveform of the PCA

# Importing
import matplotlib.pyplot as plt
import c_split_events_waveform_extraction as extract
import d_waveform_pca as wave_pca

#definition
def upper_and_lower_waveform_PCA_visualization(upper_pca, lower_pca, label, color):
    # Visualize the first 25 PCs
    fig, ax = plt.subplots(5, 5, figsize=(10, 10),sharey=True, constrained_layout=True)
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

#Applying definition to FADC0 and FADC1 data.
upper_and_lower_waveform_PCA_visualization(wave_pca.FADC0_PCA,wave_pca.FADC1_PCA, 'General FADC', 'purple')
upper_and_lower_waveform_PCA_visualization(wave_pca.Ppca_fadc0,wave_pca.Ppca_fadc1, 'Proton FADC', 'blue')
upper_and_lower_waveform_PCA_visualization(wave_pca.Ipca_fadc0,wave_pca.Ipca_fadc1, 'Iron FADC', 'r')