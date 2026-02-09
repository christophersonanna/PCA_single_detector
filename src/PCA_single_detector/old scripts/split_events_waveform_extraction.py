# -*- coding: utf-8 -*-

#split events into single detectors
#applies cuts defined in file b that need to be given to single detectors like 
#   detector status
#extracts waveforms FADC0 and FADC1 128 length arrays and ignores overhang
    #for now, may write in something later to account for that
#outputs single dataframe (data_df_single_detector)

import z_config as config

#creating definition for making an array of detectors (not event based)
    ##might want to write in a new column which states the event the detector is a part of
def fadc_single_detector_array(data, parameter):
    fadc_singdec = [
        data[parameter][event_idx][hit_idx * config.WAVEFORM_LENGTH:(hit_idx + 1) * config.WAVEFORM_LENGTH]
        for event_idx, n_hits in enumerate(data['NHits'])
        for hit_idx in range(n_hits)]
    return fadc_singdec

#!!!need to clean this up later!!!
#this is due to the fact that Doug's MC doesn't have nhits in the dataframe. 
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

def normalize_waveform(data, exclude_saturation=True):
    if exclude_saturation == True:
        data = [arr for arr in data if max(arr)<=1]
    elif exclude_saturation == False:
        data = data
    norm_data = []
    for i in range(0,len(data)):
        norm_fact = 1/max(data[i])
        norm_data.append(norm_fact*(data[i]))
    return norm_data
