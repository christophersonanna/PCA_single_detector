#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 11 11:15:57 2026

@author: anna
"""

#import numpy as np
from dataclasses import dataclass
from typing import List, Any
import awkward as ak

# Define a Type Alias for clarity, representing variable-length arrays
VarArray = Any 

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
    event_num: int
    event_code: int
    site: int
    run_id: VarArray
    trig_id: VarArray
    errcode: int
    yymmdd: int
    hhmmss: int
    usec: int
    monyymmdd: int
    monhhmmss: int
    nofwf: int
    nretry: VarArray
    wf_id: VarArray
    trig_code: VarArray
    xxyy: VarArray
    clkcnt: VarArray
    mclkcnt: VarArray
    fadcti: VarArray
    fadcav: VarArray
    fadc: VarArray
    pchmip: VarArray
    pchped: VarArray
    lhpchmip: VarArray
    lhpchped: VarArray
    rhpchmip: VarArray
    rhpchped: VarArray
    mftndof: VarArray
    mip: VarArray
    mftchi2: VarArray
    mftp: VarArray
    mftpe: VarArray
    version: int

@dataclass
class ShowLib:
    code: int
    number: int
    angle: float
    particle: int
    energy: float
    first: float
    nmax: float
    x0: float
    xmax: float
    lambda_: float  # 'lambda' is a reserved keyword
    chi2: float
    version: int

@dataclass
class RuSdmc1:
    xcore: float
    ycore: float
    t0: float
    bdist: float
    tdistbr: float
    tdistlr: float
    tdistsk: float
    tdist: float
    version: int

@dataclass
class Rufptn:
    nhits: int
    nsclust: int
    nstclust: int
    nborder: int
    isgood: VarArray
    wfindex: VarArray
    xxyy: VarArray
    nfold: VarArray
    sstart: VarArray
    sstop: VarArray
    lderiv: VarArray
    zderiv: VarArray
    xyzclf: VarArray
    reltime: VarArray
    timeerr: VarArray
    fadcpa: VarArray
    fadcpaerr: VarArray
    pulsa: VarArray
    pulsaerr: VarArray
    ped: VarArray
    pederr: VarArray
    vem: VarArray
    vemerr: VarArray
    qtot: VarArray
    tearliest: VarArray
    tyro_cdist: VarArray
    tyro_xymoments: VarArray
    tyro_xypmoments: VarArray
    tyro_u: VarArray
    tyro_v: VarArray
    tyro_tfitpars: VarArray
    tyro_chi2: VarArray
    tyro_ndof: VarArray
    tyro_theta: VarArray
    tyro_phi: VarArray
    version: int

@dataclass
class RuSdgeom:
    nsds: int
    nsig: VarArray
    sdsigq: VarArray
    sdsigt: VarArray
    sdsigte: VarArray
    igsig: VarArray
    irufptn: VarArray
    xyzclf: VarArray
    pulsa: VarArray
    sdtime: VarArray
    sdterr: VarArray
    igsd: VarArray
    xxyy: VarArray
    sdirufptn: VarArray
    xcore: VarArray
    dxcore: VarArray
    ycore: VarArray
    dycore: VarArray
    t0: VarArray
    dt0: VarArray
    theta: VarArray
    dtheta: VarArray
    phi: VarArray
    dphi: VarArray
    chi2: VarArray
    ndof: VarArray
    a: float
    da: float
    tearliest: float
    version: int

class ParquetEvent:
    """Handles the extraction of a single row into structured dataclasses."""
    def __init__(self, row):
        self.start = StartStop(row.start.active, row.start._version)
        self.stop = StartStop(row.stop.active, row.stop._version)
        
        # Helper to handle the _version underscore mapping
        def get_versioned_data(data):
            d = {k: data[k] for k in data.fields if k != "_version"}
            d["version"] = data._version
            return d

        self.rusdmc = RuSdmc(**get_versioned_data(row.rusdmc))
        self.rusdraw = RuSdraw(**get_versioned_data(row.rusdraw))
        self.rusdmc1 = RuSdmc1(**get_versioned_data(row.rusdmc1))
        
        # Special handling for ShowLib due to 'lambda_' keyword
        sl_data = get_versioned_data(row.showlib)
        sl_data['lambda_'] = sl_data.pop('lambda') 
        self.showlib = ShowLib(**sl_data)
        
        self.rufptn = Rufptn(**get_versioned_data(row.rufptn))
        self.rusdgeom = RuSdgeom(**get_versioned_data(row.rusdgeom))

def load_events(file_path: str):
    """Returns an Awkward Array of all events."""
    return ak.from_parquet(file_path)

#%%
events = load_events("/home/anna/DST_awkward-main/xmax_project_sample.parquet")

# Accessing a nested attribute across all events at once
theta_values = events.rusdmc.theta 

# Filtering: Get all events where energy > 10^18 eV
high_energy_events = events[events.rusdmc.energy > 1e18]

# Accessing variable length FADC data for the first event
first_event_fadc = events[0].rusdraw.fadc

print(theta_values)
print(high_energy_events)
print(first_event_fadc)

#%%
import pandas as pd

data = pd.read_parquet("/home/anna/DST_awkward-main/xmax_project_sample.parquet")

print((data['rusdraw'][0]['fadc'][0][0]))
