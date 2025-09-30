# -*- coding: utf-8 -*-

#import awkward as ak
import pyarrow.parquet as pq
import z_config as config
import pandas as pd #will change later

#loading data
#parquet_file = pq.ParquetFile(config.PROCESSED_DATA_PATH)
parquet_file = pd.read_parquet(config.PROCESSED_DATA_PATH)
            
'''# Read the file in chunks
data_chunks = []
for batch in parquet_file.iter_batches():
    # Convert each batch to an awkward array
    #data_chunk = ak.from_arrow(batch)
    #data_chunks.append(data_chunk)
            
    # Concatenate all chunks into a single awkward array
    #data = ak.concatenate(data_chunks)
#print(data)
    #print(f"Loaded data from {input_file} into variable '{data_var_name}'")
    print(batch)
'''

#print(parquet_file.columns)    
    
