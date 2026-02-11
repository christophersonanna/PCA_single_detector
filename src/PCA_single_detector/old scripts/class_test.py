#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#import numpy as np
from dataclasses import dataclass
from typing import List, Optional

import awkward as ak
import pandas as pd

@dataclass
class StartStop:
    active: bool
    version: int

@dataclass
class RuSdmc:
    event_num: int
    parttype: int
    corecounter: int
    tc: int
    energy: float
    height: float
    theta: float
    phi: float
    corexyz: List[float]
    version: int

@dataclass
class RuSdraw:
    # High-level event info
    event_num: int
    event_code: int
    site: int
    # Variable arrays (simplified list representation)
    fadc: List[List[List[int]]] 
    mip: List[List[float]]
    # ... and so on for the 30+ fields in rusdraw
    version: int

class ParquetEvent:
    """
    Container for a single event in the Parquet file.
    """
    def __init__(self, data_row):
        # Nested structures
        self.start = StartStop(data_row.start.active, data_row.start._version)
        self.rusdmc = RuSdmc(**{k: data_row.rusdmc[k] for k in data_row.rusdmc.fields})
        self.rusdraw = data_row.rusdraw
        self.showlib = data_row.showlib
        self.rusdmc1 = data_row.rusdmc1
        self.rufptn = data_row.rufptn
        self.rusdgeom = data_row.rusdgeom
        self.stop = StartStop(data_row.stop.active, data_row.stop._version)

def load_parquet_schema(file_path):
    # Awkward array is the standard for 'var *' type parquet files
    events = ak.from_parquet(file_path)
    return events
#%%

events = load_parquet_schema("/home/anna/DST_awkward-main/xmax_project_sample.parquet")

# Accessing a nested attribute across all events at once
theta_values = events.rusdmc.theta 

# Filtering: Get all events where energy > 10^18 eV
high_energy_events = events[events.rusdmc.energy > 1e18]

# Accessing variable length FADC data for the first event
first_event_fadc = events[0].rusdraw.fadc


#%%
data = pd.read_parquet("/home/anna/DST_awkward-main/xmax_project_sample.parquet")

print(data['rusdraw'])
