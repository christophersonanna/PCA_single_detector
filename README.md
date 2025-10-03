z) Config constant

y) Run script (all other files shouldn't plot/print anything)

---------

a) Get data

b) Extract parameters of interest

c) Split events into single detector array -  Extract waveform [Needs cleaning]
    - fadc_single_detector_array: Extracts detectors from all events into one 
                array. Run if trace signals off all detectors in an event are 
                in one array.
    - extract_waveforms: Extracts detectors from all events into one 
                array. Run if the trace signals are already in distinct arrays.

d) PCA
     PCA_single_detector: Runs the PCA and outputs two things; the pca 
                 information and the transformed data

e) Plotting script: Scree plots and Principal component plot
    - waveform_PCA_visualization: Scree plot and PC plot for one PCA only
    - PCA_comparisons: PC plot comparing two data sets 
    - PCA3_comparisons: PC plot comparing three data sets
    - upper_and_lower_waveform_PCA_visualization: PC plot for the upper and 
                lower trace signals PCAs for one dataset

f) Get MC data (combine with script a)

g) Residual PCA [WIP]

i) Playground script: used to test new ideas before adding to the rest of the 
                project
    - Currently: Time testing PCA
                 Plotting variance of primaries (super messy)



onhold for now:

*) reform events with PCA data

*) output file