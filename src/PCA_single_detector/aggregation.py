#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import config
from data_structure import Event

# aggregation.py
import numpy as np

def extract_event_features(events):
    features = []
    metadata = []
    
    for e in events:
        # 1. Get all FADC waveforms for this event's hits
        # Shape: (num_hits, 128)
        waves = np.array([h.fadc0 for h in e.hits])
        
        if len(waves) == 0:
            continue
            
        # 2. Calculate the "Event Profile"
        # We take the mean and std across the hits to see the 'average' shower shape
        mean_wf = np.mean(waves, axis=0)
        std_wf = np.std(waves, axis=0)
        
        # 3. Combine them into one feature vector (256 bins)
        # This is what the PCA will actually look at
        f = np.concatenate([mean_wf, std_wf])
        
        features.append(f)
        
        # 4. Store the metadata for coloring the plots later
        metadata.append({
            'xmax': e.xmax,
            'energy': e.energy,
            'particle': e.particle,
            'radius': np.mean([h.radius for h in e.hits])
        })
        
    return np.array(features), metadata