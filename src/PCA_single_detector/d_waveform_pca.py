# -*- coding: utf-8 -*-

#Only step is processing the data from c through a PCA
#for now, we'll create a new PCA for the data, but I will need to account for 
#   when I need to apply new data to a pre-existing PCA

import z_config as config
import c_split_events_waveform_extraction as waveform
import numpy as np
from sklearn.decomposition import PCA

#creating PCA definition for single detector waveforms
def PCA_single_detector(data):
    data_array = np.array(data)
    pca = PCA(n_components=config.N_COMPONENTS_PCA)
    transformed_data = pca.fit_transform(data_array)
    return pca, transformed_data

#running PCA
FADC0_PCA, transformed_FADC0_data = PCA_single_detector(waveform.fadc0_singdec)
FADC1_PCA, transformed_FADC1_data = PCA_single_detector(waveform.fadc1_singdec)