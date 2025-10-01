# -*- coding: utf-8 -*-

#split events into single detectors
#applies cuts defined in file b that need to be given to single detectors like 
#   detector status
#extracts waveforms FADC0 and FADC1 128 length arrays and ignores overhang
    #for now, may write in something later to account for that
#outputs single dataframe (data_df_single_detector)

import numpy as np
import z_config as config
import b_perameter_extraction as extract
#import f_a_get_mc as get_mc

#creating definition for making an array of detectors (not event based)
    ##might want to write in a new column which states the event the detector is a part of
def fadc_single_detector_array(data, parameter):
    fadc_singdec = [
        data[parameter][event_idx][hit_idx * config.WAVEFORM_LENGTH:(hit_idx + 1) * config.WAVEFORM_LENGTH]
        for event_idx, n_hits in enumerate(data['NHits'])
        for hit_idx in range(n_hits)]
    return fadc_singdec

#extraction fadc0
fadc0_singdec = fadc_single_detector_array(extract.data_df, 'FADC0')

#extraction fadc1
fadc1_singdec = fadc_single_detector_array(extract.data_df,'FADC1')

print(f"Extracted {len(fadc0_singdec)} single detector waveforms.")

'''
#%%need to clean this up later!!!
def extract_waveforms(dataframe):
    fadc0_list = []
    fadc1_list = []

    for event_idx in range(len(dataframe)):
        event_fadc0 = dataframe['FADC0'].iloc[event_idx]
        event_fadc1 = dataframe['FADC1'].iloc[event_idx]

        # Calculate number of waveforms per event
        num_waveforms_fadc0 = len(event_fadc0) // config.WAVEFORM_LENGTH
        num_waveforms_fadc1 = len(event_fadc1) // config.WAVEFORM_LENGTH

        # Extract individual waveforms by slicing
        for i in range(num_waveforms_fadc0):
            fadc0_list.append(event_fadc0[i * config.WAVEFORM_LENGTH:(i + 1) * config.WAVEFORM_LENGTH])

        for i in range(num_waveforms_fadc1):
            fadc1_list.append(event_fadc1[i * config.WAVEFORM_LENGTH:(i + 1) * config.WAVEFORM_LENGTH])

    return fadc0_list, fadc1_list


# Proton Data Processing
print("\nProton Data")
fadc0_p, fadc1_p = extract_waveforms(get_mc.proton_data)
fadc0_p = [arr for arr in fadc0_p if np.sum(arr) != 0]
fadc1_p = [arr for arr in fadc1_p if np.sum(arr) != 0]
print(f"Extracted {len(fadc0_p)} single FADC0 waveforms for Protons.")

# Iron Data Processing
print("\nIron Data")
fadc0_f, fadc1_f = extract_waveforms(get_mc.iron_data)
fadc0_f = [arr for arr in fadc0_f if np.sum(arr) != 0]
fadc1_f = [arr for arr in fadc1_f if np.sum(arr) != 0]
print(f"Extracted {len(fadc0_f)} single FADC0 waveforms for Iron.")'''