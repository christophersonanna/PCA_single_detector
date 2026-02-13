# -*- coding: utf-8 -*-

import pandas as pd
import awkward as ak
import config

def load_dataset(file_list):
    """Combines multiple parquet files into one Awkward array."""
    dfs = [pd.read_parquet(f) for f in file_list]
    return pd.concat(dfs, ignore_index=True)

# Load based on config
proton_data = load_dataset(config.DATA_FILES["proton"])
iron_data = load_dataset(config.DATA_FILES["iron"])
sample_data = ak.from_parquet(config.DATA_FILES["sample"][0])

#still figuring this out 