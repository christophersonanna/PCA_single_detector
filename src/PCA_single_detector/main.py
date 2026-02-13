#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 12:31:04 2026

@author: anna
"""
import argparse
from config import N_COMPONENTS_PCA
from loader import load_parquet
from processor import apply_cuts, events_to_waveform_set, global_pca_event_aggregation
from plotting import plot_events_by_primary

def main():
    parser = argparse.ArgumentParser(description="Unified PCA Pipeline")
    parser.add_argument("paths", nargs="+", help="Input Parquet files")
    args = parser.parse_args()

    # 1. Load and merge files
    all_events = []
    for path in args.paths:
        all_events.extend(load_parquet(path))

    # 2. Apply cuts (e.g., n_space_cluster > 5)
    all_events = apply_cuts(all_events)

    # 3. Transform to WaveformSet
    ws = events_to_waveform_set(all_events)

    # 4. Global PCA aggregation for FADC0 and FADC1
    res0 = global_pca_event_aggregation(ws, "fadc0", N_COMPONENTS_PCA)
    res1 = global_pca_event_aggregation(ws, "fadc1", N_COMPONENTS_PCA)

    # 5. Plotting results
    plot_events_by_primary(res0, "mean_PC1", "mean_PC2")

if __name__ == "__main__":
    main()