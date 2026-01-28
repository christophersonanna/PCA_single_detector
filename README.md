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

*) reform events with PCA data

*) output file



Plans to reformat:

-) Config File

a) definitions of functions

b) definitions of plots/visualzation

c) getting and organizing data

d-??) Different files to call based on what I want done
        - examples:
            - plot PCA of the entire files
            - plot upper and lower signals
            - plot radius PCA 
                - specify the radius of interest or do all
            - plot primary 
            
y) Run script (calls everything into one script)

z) Playground file - lets me figure things out without touching the good files
