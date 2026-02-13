# -*- coding: utf-8 -*-

from pathlib import Path

# Data Loading
DATA_FILES = {
    "proton": [
        '/home/anna/Downloads/processed_tree_radius_14_MC_pt1.parquet',
        '/home/anna/Downloads/processed_tree_radius_14_MC_pt2.parquet',
        '/home/anna/Downloads/processed_tree_radius_14_MC_pt3.parquet'
    ],
    "iron": [
        '/home/anna/Downloads/processed_tree_radius_2654_MC_pt1.parquet',
        '/home/anna/Downloads/processed_tree_radius_2654_MC_pt2.parquet',
        '/home/anna/Downloads/processed_tree_radius_2654_MC_pt3.parquet'
    ],
    "sample": ['/home/anna/DST_awkward-main/xmax_project_sample.parquet']
}

N_COMPONENTS_PCA = 128
WAVEFORM_LENGTH = 128
PLOT_PRINCIPLE_COMPONENTS = 25
PROTON = 14
IRON = 5626
PRIMARY_UNKNOWN = -1