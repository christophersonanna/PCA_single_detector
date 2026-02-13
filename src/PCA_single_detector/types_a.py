#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import numpy as np
from sklearn.decomposition import PCA

@dataclass
class Hit:
    fadc0: np.ndarray
    fadc1: np.ndarray

@dataclass
class Event:
    event_id: int
    hits: list[Hit]
    n_space_cluster: int | None = None
    primary: int | None = None
    radius: np.ndarray | list | None = None

@dataclass
class WaveformSet:
    fadc0: list[np.ndarray]
    fadc1: list[np.ndarray]
    event_id: np.ndarray | None = None
    primary: np.ndarray | None = None

@dataclass
class EventPCAResult:
    event_id: np.ndarray
    primary: np.ndarray | None
    features: np.ndarray
    feature_names: list[str]
    pca: PCA