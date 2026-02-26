#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def calculate_separation(p_coords, i_coords):
    if len(p_coords) == 0 or len(i_coords) == 0: return {"sep": 0}
    p_m, i_m = np.mean(p_coords, axis=0), np.mean(i_coords, axis=0)
    dist = np.linalg.norm(p_m - i_m)
    spread = np.mean(np.std(p_coords, axis=0)) + np.mean(np.std(i_coords, axis=0))
    return {"sep": dist / (spread + 1e-9)}
