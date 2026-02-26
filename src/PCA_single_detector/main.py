#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import numpy as np
from glob import glob
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

import config
from load import load_and_transform
from aggregation import extract_event_features
from statistics import calculate_separation
import plotting

def analyze_subset(events, label, args):
    """Universal analysis for Protons, Irons, or mixed datasets."""
    
    # Identify populations
    protons = [e for e in events if e.particle == config.PROTON_ID]
    irons = [e for e in events if e.particle == config.IRON_ID]
    
    print(f"\n--- Analysis for: {label} ---")
    print(f"Total Events: {len(events)} ({len(protons)} P, {len(irons)} I)")

    if len(events) < 2:
        print("Warning: Skipping - Need at least 2 events for PCA.")
        return 0

    # 1. Feature & Metadata Extraction
    all_feat, all_meta = extract_event_features(events)
    
    # 2. Waveform Plotting (Mean/Std)
    if args.plot_wave:
        p_feat, _ = extract_event_features(protons) if protons else (None, None)
        i_feat, _ = extract_event_features(irons) if irons else (None, None)
        plotting.plot_mean_std(p_feat, i_feat, label)

    # 3. PCA Calculation
    # Solve for max of (requested n_pcs) and 12 (required for the 3D grid)
    n_to_solve = min(max(args.n_pcs, 12), len(all_feat))
    pca = PCA(n_components=n_to_solve).fit(all_feat)
    all_trans = pca.transform(all_feat)

    # 4. PC Shape and Scree Plots
    if args.plot_pcs:
        plotting.plot_scree(pca)
        plotting.plot_pca_components(pca, args.n_pcs)

    # 5. 3D Variance Grid
    if args.plot_3d:
        p_idx = [i for i, e in enumerate(events) if e.particle == config.PROTON_ID]
        i_idx = [i for i, e in enumerate(events) if e.particle == config.IRON_ID]
        
        p_trans = all_trans[p_idx] if p_idx else np.empty((0, n_to_solve))
        i_trans = all_trans[i_idx] if i_idx else np.empty((0, n_to_solve))
        p_meta = [all_meta[i] for i in p_idx]
        i_meta = [all_meta[i] for i in i_idx]
        
        plotting.plot_3d_variance_grid(p_trans, i_trans, p_meta, i_meta, color_attr=args.color_by)

    # Return separation power if both exist
    if len(protons) > 1 and len(irons) > 1:
        return calculate_separation(all_trans[p_idx], all_trans[i_idx])['sep']
    return 0

def main():
    parser = argparse.ArgumentParser(description="TA PCA Analysis Suite")
    parser.add_argument("-i", "--input", required=True, help="Path to .parquet file or directory")
    parser.add_argument("-R", "--radius", type=float, help="Radius cut (km)")
    parser.add_argument("-E", "--energy", type=float, help="Energy cut (log10 eV)")
    parser.add_argument("-X", "--xmax", type=float, help="Xmax cut (g/cm^2)")
    
    # Plotting Controls
    parser.add_argument("--plot-pcs", action="store_true")
    parser.add_argument("--n-pcs", type=int, default=6)
    parser.add_argument("--plot-wave", action="store_true")
    parser.add_argument("--plot-3d", action="store_true")
    parser.add_argument("--color-by", type=str, default="xmax", 
                        choices=["xmax", "energy", "particle", "radius"])
    parser.add_argument("--sweep", action="store_true")
    
    args = parser.parse_args()

    # File Discovery
    if os.path.isdir(args.input):
        file_list = sorted(glob(os.path.join(args.input, "*.parquet")))
        print(f"Directory detected. Found {len(file_list)} Parquet files.")
    else:
        file_list = [args.input]

    if not file_list:
        print("Error: No parquet files found.")
        return

    # Aggregate Events
    all_events = []
    for f in file_list:
        try:
            loaded = load_and_transform(f)
            all_events.extend(loaded)
        except Exception as e:
            print(f"Failed to load {f}: {e}")
    
    print(f"Total Combined Events: {len(all_events)}")
    
    # Apply Cuts
    events = all_events
    if args.energy:
        events = [e for e in events if abs(e.energy - args.energy) < config.ENERGY_WINDOW]
        print(f"Energy cut applied: {args.energy}")
    if args.xmax:
        events = [e for e in events if abs(e.xmax - args.xmax) < 50.0]
        print(f"Xmax cut applied: {args.xmax}")

    # Run Analysis
    if args.sweep:
        sweep_data = []
        for r in [2.0, 4.0, 6.0, 8.0, 10.0, 12.0]:
            r_evs = [e for e in events if abs(np.mean([h.radius for h in e.hits]) - r) < config.RADIUS_WINDOW]
            if len(r_evs) > 2:
                sep = analyze_subset(r_evs, f"Radius {r}km", args)
                sweep_data.append({'r': r, 's': sep})
        if sweep_data:
            plotting.plot_radius_sweep(sweep_data)
    else:
        if args.radius:
            events = [e for e in events if abs(np.mean([h.radius for h in e.hits]) - args.radius) < config.RADIUS_WINDOW]
            label = f"Radius {args.radius}km"
        else:
            label = "Full Combined Dataset"
        analyze_subset(events, label, args)

if __name__ == "__main__":
    main()