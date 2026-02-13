#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 21:06:54 2026

@author: anna
"""

# modules/processor.py
import numpy as np
from sklearn.decomposition import PCA
from core import config
from core.types import Event, WaveformSet, EventPCAResult

def apply_cuts(events: list[Event], n_space_cluster_min: int = 5) -> list[Event]:
    """Filters events based on the number of space clusters."""
    return [
        e for e in events
        if e.n_space_cluster is not None and e.n_space_cluster > n_space_cluster_min
    ]

def normalize_waveform(wf: np.ndarray) -> np.ndarray:
    """Normalizes a waveform by its maximum amplitude."""
    max_val = np.max(np.abs(wf))
    return wf / max_val if max_val > 0 else wf

def events_to_waveform_set(events: list[Event], drop_zero: bool = True) -> WaveformSet:
    """Flattens a list of events into a single set of waveforms for PCA input."""
    fadc0, fadc1, ids, primaries = [], [], [], []
    
    for ev in events:
        for hit in ev.hits:
            if drop_zero and np.sum(hit.fadc0) == 0 and np.sum(hit.fadc1) == 0:
                continue
            fadc0.append(hit.fadc0)
            fadc1.append(hit.fadc1)
            ids.append(ev.event_id)
            primaries.append(ev.primary if ev.primary is not None else config.PRIMARY_UNKNOWN)
            
    return WaveformSet(
        fadc0=fadc0, 
        fadc1=fadc1, 
        event_id=np.array(ids), 
        primary=np.array(primaries)
    )

def global_pca_event_aggregation(ws: WaveformSet, channel: str, n_comp: int) -> EventPCAResult:
    """
    Performs PCA on all waveforms and then aggregates scores back to the event level
    by calculating the mean and standard deviation of components per event.
    """
    waveforms = getattr(ws, channel)
    X = np.array(waveforms, dtype=np.float64)
    
    pca = PCA(n_components=n_comp)
    scores = pca.fit_transform(X)

    unique_ev, ev_inverse = np.unique(ws.event_id, return_inverse=True)
    n_events = len(unique_ev)
    features = np.zeros((n_events, 2 * n_comp))
    
    # Identify labels for each unique event
    _, first_indices = np.unique(ev_inverse, return_index=True)
    event_primaries = ws.primary[first_indices]

    for i in range(n_events):
        mask = ev_inverse == i
        event_scores = scores[mask]
        features[i, :n_comp] = np.mean(event_scores, axis=0)
        features[i, n_comp:] = np.std(event_scores, axis=0)

    f_names = [f"mean_PC{k+1}" for k in range(n_comp)] + [f"std_PC{k+1}" for k in range(n_comp)]
    
    return EventPCAResult(unique_ev, event_primaries, features, f_names, pca)