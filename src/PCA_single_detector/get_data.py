# -*- coding: utf-8 -*-

#import awkward as ak
#import pyarrow.parquet as pq
import z_config as config
import pandas as pd #[will change later]

#loading data
"""Major rewrite needed"""
'''I want to write a script that allows me to read in any file(s) I want and out 
        put it as one array'''


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
 
#this is a placeholder until I can clear up the get_data script to account for more than one file
#library
import pandas as pd

# import data
proton_data1 = pd.read_parquet('/home/anna/Downloads/processed_tree_radius_14_MC_pt1.parquet')
proton_data2 = pd.read_parquet('/home/anna/Downloads/processed_tree_radius_14_MC_pt2.parquet')
proton_data3 = pd.read_parquet('/home/anna/Downloads/processed_tree_radius_14_MC_pt3.parquet')
proton_data = pd.concat([proton_data1,proton_data2, proton_data3], ignore_index=True)

iron_data1 = pd.read_parquet('/home/anna/Downloads/processed_tree_radius_2654_MC_pt1.parquet')
iron_data2 = pd.read_parquet('/home/anna/Downloads/processed_tree_radius_2654_MC_pt2.parquet')
iron_data3 = pd.read_parquet('/home/anna/Downloads/processed_tree_radius_2654_MC_pt3.parquet')
iron_data = pd.concat([iron_data1, iron_data2, iron_data3], ignore_index=True)

