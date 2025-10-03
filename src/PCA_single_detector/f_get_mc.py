# -*- coding: utf-8 -*-


#this is a placeholder until I can clear up the get_data script to account for more than one file
#library
import pandas as pd

# import data
proton_data1 = pd.read_parquet('/home/anna/Downloads/processed_tree_14_MC.parquet')
proton_data2 = pd.read_parquet('/home/anna/Downloads/processed_tree_14_MC_pt2.parquet')
proton_data = pd.concat([proton_data1,proton_data2], ignore_index=True)

iron_data1 = pd.read_parquet('/home/anna/Downloads/processed_tree_5426_MC.parquet')
iron_data2 = pd.read_parquet('/home/anna/Downloads/processed_tree_2654_MC_pt2.parquet')
iron_data = pd.concat([iron_data1, iron_data2], ignore_index=True)

