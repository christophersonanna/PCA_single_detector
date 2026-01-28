z) Config constant

y) Run script (all other files shouldn't plot/print anything)

Plans to reformat:

* config.py

* get_data.py
    ! Most work needed here (see note in script)
    - Reads data file in

* parameter_cuts_and_organization.py
    ! Needs to be reworked into a def/class
    - Applies all cuts wanted and organizes the data.

* waveform_extraction.py
    - fadc_single_detector_array(data, parameter): Extracts detectors from all 
            events into one array. Run if trace signals off all detectors in 
            an event are in one array.

    - extract_waveforms(dataframe): Extracts detectors from all events into one 
            array. Run if the trace signals are already in distinct arrays.
            
    -normalize_waveform(data, exclude_saturation=True): Normalizes the waveform 
            BEFORE the PCA to ensure less saturated principal components

*  waveform_PCA.py
    - PCA_single_detector(data): Runs the PCA and outputs two things; the pca 
             information and the transformed data
             
* plotting.py
    - waveform_PCA_visualization(pca, label, color): Scree plot and PC plot for 
            one PCA only

    - PCA_comparisons(upper_pca, lower_pca, label, color): PC plot comparing 
            two data sets 

    - PCA3_comparisons(pca1, pca2, ID1, ID2, label, color1, color2): PC plot 
            comparing three data sets

    - upper_and_lower_waveform_PCA_visualization(pca1, pca2, pca3,label): PC 
            plot for the upper and lower trace signals PCAs for one dataset

    - variance_plot(data_after_pca, label, color): Projects the PCA data in the 
            first 3 PCs

* waveform_reconstruction.py
    - plot_wave_against_PCA_recon_waveform(data,PCA, trans, n, comp_start, comp_end,c):
            Reconstructions the detectors waveform from the stated principal 
            components

* sandbox.py
    -Script to mess around with new ideas
    
* main.py
    -main script to read and run all other SCRIPTS
    !!! Currently just running what I need, need to rewrite 
    
*

Wants: 
d-??) Different files to call based on what I want done
        - examples:
            - plot PCA of the entire files
            - plot upper and lower signals
            - plot radius PCA 
                - specify the radius of interest or do all
            - plot primary 






---------[OLD SCRIPTS]

a) Get data

b) Extract parameters of interest

c) Split events into single detector array -  Extract waveform [Needs cleaning]
    
    - fadc_single_detector_array: Extracts detectors from all events into one 
                array. Run if trace signals off all detectors in an event are 
                in one array.
    
    - extract_waveforms: Extracts detectors from all events into one 
                array. Run if the trace signals are already in distinct arrays.
                
    -normalize_waveform: Normalizes the waveform BEFORE the PCA to ensure less 
                saturated principal components
    
d) PCA
    
    - PCA_single_detector: Runs the PCA and outputs two things; the pca 
                 information and the transformed data

e) Plotting script: Scree plots and Principal component plot
    
    - waveform_PCA_visualization: Scree plot and PC plot for one PCA only
    
    - PCA_comparisons: PC plot comparing two data sets 
    
    - PCA3_comparisons: PC plot comparing three data sets
    
    - upper_and_lower_waveform_PCA_visualization: PC plot for the upper and 
                lower trace signals PCAs for one dataset
    
    - variance_plot: Projects the PCA data in the first 3 PCs

f) Get MC data (combine with script a)

g) Residual PCA [WIP]

i) Playground script: used to test new ideas before adding to the rest of the 
                project. The code here will allows be very messy.
    
    - Currently: Plotting PCA of primaries according to distance from core
    
                 Plotting variance of primaries
                 Time testing PCA


onhold for now:

*) output file
