# -*- coding: utf-8 -*-

#split events into single detectors
#applies cuts defined in file b that need to be given to single detectors like 
#   detector status
#extracts waveforms FADC0 and FADC1 128 length arrays and ignores overhang
    #for now, may write in something later to account for that
#outputs single dataframe (data_df_single_detector)


fadc0_singdec = [
    data_df['FADC0'][event_idx][hit_idx * WAVEFORM_LENGTH:(hit_idx + 1) * WAVEFORM_LENGTH]
    for event_idx, n_hits in enumerate(data_df['NHits'])
    for hit_idx in range(n_hits)]

fadc1_singdec = [
    data_df['FADC1'][event_idx][hit_idx * WAVEFORM_LENGTH:(hit_idx + 1) * WAVEFORM_LENGTH]
    for event_idx, n_hits in enumerate(data_df['NHits'])
    for hit_idx in range(n_hits)]

print(f"Extracted {len(fadc0_singdec)} single FADC0 waveforms.")