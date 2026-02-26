#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
from glob import glob
from load import load_and_transform
from aggregation import extract_event_features

def run_preprocessing(input_dir, output_filename="processed_data.npz"):
    file_list = sorted(glob(os.path.join(input_dir, "*.parquet")))
    print(f"Found {len(file_list)} files. Starting extraction...")

    all_features = []
    all_xmax = []
    all_energy = []
    all_particle = []
    all_radius = []

    for i, f in enumerate(file_list):
        events = load_and_transform(f)
        if not events: continue
        
        feats, meta = extract_event_features(events)
        
        all_features.append(feats)
        all_xmax.extend([m['xmax'] for m in meta])
        all_energy.extend([m['energy'] for m in meta])
        all_particle.extend([m['particle'] for m in meta])
        all_radius.extend([m['radius'] for m in meta])
        
        if i % 100 == 0:
            print(f"Processed {i}/{len(file_list)} files...")

    # Save to compressed numpy format
    np.savez_compressed(
        output_filename,
        features=np.vstack(all_features),
        xmax=np.array(all_xmax),
        energy=np.array(all_energy),
        particle=np.array(all_particle),
        radius=np.array(all_radius)
    )
    print(f"Done! Saved to {output_filename}")

if __name__ == "__main__":
    import sys
    run_preprocessing(sys.argv[1])
