# -*- coding: utf-8 -*-

# should be able to suggest cuts from terminal
# spacecluster > n
# detector status = n
# ...
# export only one dataframe with correct labels (data_df)

#importing
import z_config as config
import a_get_data as get_data


#extraction parameters
data_df = pd.read_parquet(config.PROCESSED_DATA_PATH)
data_df = data_df[data_df['NSpaceCluster'] > 4].reset_index(drop=True) #write in function new var
print("Initial Data Columns:", data_df.columns.tolist())