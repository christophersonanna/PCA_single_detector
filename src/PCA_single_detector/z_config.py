# -*- coding: utf-8 -*-

from pathlib import Path

# Configuration Constants
PROCESSED_DATA_PATH = Path('/home/anna/Machine_Learning_Xmax/data/processed_tree_sample.parquet')
OUTPUT_DATA_PATH = Path('/home/anna/Machine_Learning_Xmax/data/PCA_single_detector_25PC.parquet')
N_COMPONENTS_PCA = 128
WAVEFORM_LENGTH = 128
PLOT_PRINCIPLE_COMPONENTS = 16 #must be square for now
PROTON = 14
IRON = 5626