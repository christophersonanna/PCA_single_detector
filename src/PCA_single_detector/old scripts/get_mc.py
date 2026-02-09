# -*- coding: utf-8 -*-


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

