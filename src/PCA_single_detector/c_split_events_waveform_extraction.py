# -*- coding: utf-8 -*-

#split events into single detectors
#applies cuts defined in file b that need to be given to single detectors like 
#   detector status
#extracts waveforms FADC0 and FADC1 128 length arrays and ignores overhang
    #for now, may write in something later to account for that
#outputs single dataframe (data_df_single_detector)

import z_config as config
import b_perameter_extraction as extract

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