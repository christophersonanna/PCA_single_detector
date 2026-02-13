#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 21:06:32 2026

@author: anna
"""

# modules/loader.py
import awkward as ak
import numpy as np
from pathlib import Path
from types_a import Event, Hit

def load_parquet(path: Path | str) -> list[Event]:
    """
    Reads a parquet file and returns a list of Event objects.
    Handles the mapping from 'rusdraw' and 'rufptn' nested tables.
    """
    path = Path(path)
    table = ak.from_parquet(path)
    n_events = len(table)
    
    # Check if this is MC data (has 'primary' column)
    has_primary = "primary" in table.fields
    
    events = []
    for i in range(n_events):
        rd = table["rusdraw"][i]
        rp = table["rufptn"][i] if "rufptn" in table.fields else None
        
        # Extract Hits
        hits = []
        if rd is not None:
            nofwf_val = ak.to_list(rd["nofwf"])
            nofwf = int(nofwf_val[0] if isinstance(nofwf_val, list) else nofwf_val)
            
            fadc = rd["fadc"]
            for j in range(nofwf):
                a0 = np.asarray(ak.to_numpy(fadc[j][0]), dtype=np.float64)
                a1 = np.asarray(ak.to_numpy(fadc[j][1]), dtype=np.float64)
                hits.append(Hit(fadc0=a0, fadc1=a1))

        # Extract n_space_cluster
        nsc = None
        if rp is not None and hasattr(rp, "nsclust"):
            nsc_val = ak.to_list(rp.nsclust)
            nsc = int(nsc_val[0] if isinstance(nsc_val, list) else nsc_val)

        primary = int(table["primary"][i]) if has_primary else None
        
        events.append(Event(
            event_id=i, 
            hits=hits, 
            n_space_cluster=nsc, 
            primary=primary
        ))

    return events