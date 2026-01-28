#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Reading in every file and function so they're all avaliable for use
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import config
from get_data import parquet_file, iron_data, proton_data
from parameter_cuts_and_organization import data_df
from plotting import waveform_PCA_visualization, upper_and_lower_waveform_PCA_visualization, PCA_comparisons, PCA3_comparisons, variance_plot
from waveform_extraction import fadc_single_detector_array, extract_waveforms, normalize_waveform
from waveform_PCA import PCA_single_detector
from waveform_reconstruction import plot_wave_against_PCA_recon_waveform


#%%

