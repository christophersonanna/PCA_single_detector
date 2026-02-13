#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import libraries
from dataclasses import dataclass
from typing import List, Any
import awkward as ak
import numpy as np

#define a Type Alias for clarity, representing variable-length arrays
np.ndarray = Any 

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
    run_id: np.ndarray
    trig_id: np.ndarray
    errcode: int
    yymmdd: int
    hhmmss: int
    usec: int
    monyymmdd: int
    monhhmmss: int
    nofwf: int
    nretry: np.ndarray
    wf_id: np.ndarray
    trig_code: np.ndarray
    xxyy: np.ndarray
    clkcnt: np.ndarray
    mclkcnt: np.ndarray
    fadcti: np.ndarray
    fadcav: np.ndarray
    fadc: np.ndarray
    pchmip: np.ndarray
    pchped: np.ndarray
    lhpchmip: np.ndarray
    lhpchped: np.ndarray
    rhpchmip: np.ndarray
    rhpchped: np.ndarray
    mftndof: np.ndarray
    mip: np.ndarray
    mftchi2: np.ndarray
    mftp: np.ndarray
    mftpe: np.ndarray
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
    lambda_: float
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
    isgood: np.ndarray
    wfindex: np.ndarray
    xxyy: np.ndarray
    nfold: np.ndarray
    sstart: np.ndarray
    sstop: np.ndarray
    lderiv: np.ndarray
    zderiv: np.ndarray
    xyzclf: np.ndarray
    reltime: np.ndarray
    timeerr: np.ndarray
    fadcpa: np.ndarray
    fadcpaerr: np.ndarray
    pulsa: np.ndarray
    pulsaerr: np.ndarray
    ped: np.ndarray
    pederr: np.ndarray
    vem: np.ndarray
    vemerr: np.ndarray
    qtot: np.ndarray
    tearliest: np.ndarray
    tyro_cdist: np.ndarray
    tyro_xymoments: np.ndarray
    tyro_xypmoments: np.ndarray
    tyro_u: np.ndarray
    tyro_v: np.ndarray
    tyro_tfitpars: np.ndarray
    tyro_chi2: np.ndarray
    tyro_ndof: np.ndarray
    tyro_theta: np.ndarray
    tyro_phi: np.ndarray
    version: int

@dataclass
class RuSdgeom:
    nsds: int
    nsig: np.ndarray
    sdsigq: np.ndarray
    sdsigt: np.ndarray
    sdsigte: np.ndarray
    igsig: np.ndarray
    irufptn: np.ndarray
    xyzclf: np.ndarray
    pulsa: np.ndarray
    sdtime: np.ndarray
    sdterr: np.ndarray
    igsd: np.ndarray
    xxyy: np.ndarray
    sdirufptn: np.ndarray
    xcore: np.ndarray
    dxcore: np.ndarray
    ycore: np.ndarray
    dycore: np.ndarray
    t0: np.ndarray
    dt0: np.ndarray
    theta: np.ndarray
    dtheta: np.ndarray
    phi: np.ndarray
    dphi: np.ndarray
    chi2: np.ndarray
    ndof: np.ndarray
    a: float
    da: float
    tearliest: float
    version: int

class ParquetEvent:
    def __init__(self, row):
        # Maps the complex nested Awkward structures to Python objects
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
    return ak.from_parquet(file_path)

#%%
events = load_events("/home/anna/DST_awkward-main/xmax_project_sample.parquet")

# Accessing a nested attribute across all events at once
theta_values = events.rusdmc.theta 

# Filtering: Get all events where energy > 10^18 eV
high_energy_events = events[events.rusdmc.energy > 1e18]

# Accessing variable length FADC data for the first event
first_event_fadc = events[0].rusdraw.fadc

#print(theta_values)
#print(high_energy_events)
#print(first_event_fadc)
#print(events[0].rusdgeom.xxyy)
print(events[0].rufptn.reltime)