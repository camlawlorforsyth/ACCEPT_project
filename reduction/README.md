# README #

These steps outline the procedure to run an automated reduction process which will reduce archival *Chandra* data, compute the concentration, asymmetry, and clumpiness (CAS) parameters, the symmetry, peakiness, and alignment (SPA) parameters, and create Gaussian-Gradient Magnitude (GGM) and unsharp-masked (UM) images for clusters of galaxies present in the [ACCEPT](https://web.pa.msu.edu/astro/MC2/accept/) sample. This reduction adopts the standard flat Lambda-CDM cosmology, with H_0 = 70 km/s /Mpc, Omega_m = 0.3, and Omega_Lambda = 0.7.

## Step 1 - Initial Reduction ##

Open a terminal and navigate to your data/ directory, start CIAO and run `python get_all_data.py` once CIAO is confirmed to be running.
```
cd data/
ciao
python get_all_data.py >> initial_reduction.log 2>> initial_reduction_error.log
```

Upon completion of the previous command, check "data/initial_reduction_error.log" for any significant error messages. If an error is recorded, re-run the necessary line from [get_all_data.py](get_all_data.py) for that cluster, in the terminal.

## Step 2 - Point Source Verification ##

Before continuing with the automated reduction and analysis scripts, we must verify the detected point sources. First we must verify that all the necessary files are present in the cluster directory.
```
cd data/
ciao
python check_all_data.py >> check.log 2>> check_error.log
```

The above command creates a text file called "data/checks.txt" which shows the number of files present in each cluster directory, as well as the number of lines in each "data/[cluster]/sources.reg" file, if present. If the "sources.reg" file is not present, an error message is appended. Conversely, if the cluster has insufficent data for further analysis, the total amount of insufficient data for that cluster is recorded.

Now the sources in "[cluster]/sources.reg" can be viewed in DS9 and any spurious detections can be deleted.
```
cd data/
ciao
ds9 [cluster]/SPA/broad_thresh.fits -scale log -region [cluster]/sources.reg -region [cluster]/roi_sky.reg
```
Save the resulting region file as "[cluster]/sources_mod.reg" in 'ciao' format with 'physical' coordinates.

## Step 3 - Further Reduction ##

The subsequent reduction steps can now be completed. Note that the quality flags appended in [reduce_all_data.py](reduce_all_data.py) were determined in [reduce1.py](reduce1.py) by the [roi_count.py](roi_count.py) script.

Ensure that CIAO is running, and then run `python reduce_all_data.py`.
```
cd data/
ciao
python reduce_all_data.py >> secondary_reduction.log 2>> secondary_reduction_error.log
```

Upon completion of the previous command, check "data/secondary_reduction_error.log" for any significant error messages. If an error is recorded, re-run the necessary line from [reduce_all_data.py](reduce_all_data.py) for that cluster, in the terminal.

## Step 4 - CAS Analysis ##

We can now proceed with the CAS analysis of the clusters with sufficient counts for analysis. Note that the quality flags appended in [cas_process_all_data.py](cas_process_all_data.py) were determined in [reduce1.py](reduce1.py) by the [roi_count.py](roi_count.py) script.

Ensure that CIAO is running, and then run `python cas_process_all_data.py`.
```
cd data/
ciao
python cas_process_all_data.py >> CAS_analysis.log 2>> CAS_analysis_error.log
```

Upon completion of the previous command, there will be a file "data/CAS_parameters_v2.txt" which contains relevant information about each cluster. This file includes the values for the Concentration (C), Asymmetry (A), and Clumpiness (S) parameters for each cluster, along with associated 1-sigma uncertainties. Clusters with insufficent counts that have been skipped will have ",,,,,," on their corresponding line in the "data/CAS_parameters_v2.txt" file.

An unsharp-masked (UM) image ("unsharp_mask.fits") will be created, and can be found in [cluster]/ROI_2/. This image can be used to probe both small- and large-scale structure of the ICM.

A Gaussian gradient magnitude (GGM) image ("ggm.fits") will also be created, and can be found in [cluster]/ggm/. This image can be used to probe both small- and large-scale structure of the ICM.

## Step 5 - SPA Analysis ##

We can now proceed with the SPA analysis of the clusters with sufficient counts for analysis. Note that the quality flags appended in [spa_process_all_data.py](spa_process_all_data.py) were determined in [reduce1.py](reduce1.py) by the [roi_count.py](roi_count.py) script.

Ensure that CIAO is **not** running by simply opening a new terminal. Now export the shared libraries (for GSL), start HEAsoft, and then run `python spa_process_all_data.py`.
```
cd data/
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/home/cam/soft/heasoft-6.26.1/x86_64-pc-linux-gnu-libc2.17/lib
export LD_LIBRARY_PATH
heainit
python spa_process_all_data.py >> SPA_analysis.log 2>> SPA_analysis_error.log
```

Upon completion of the previous command, there will be a file "data/SPA_parameters_v2.txt" which contains relevant information about each cluster. This file includes the values for the Symmetry (*s*), Peakiness (*p*), and Alignment (*a*) parameters for each cluster, along with associated 1-sigma uncertainties. Clusters with insufficent counts that have been skipped will have ",,,,,," on their corresponding line in the "data/SPA_parameters_v2.txt" file.

## Conclusion ##

The purpose of this guide was to assist in downloading, reducing, and analyzing archival *Chandra* data, while creating GGM-filtered and UM images, as well as determining the CAS and SPA parameters. Hopefully it was both an informative and useful tool in this regard. Comments, suggestions, and prospective improvements can be sent to C. Lawlor-Forsyth at [lawlorfc@myumanitoba.ca](mailto:lawlorfc@myumanitoba.ca).

### Acknowledgements ###
Much of the early work developing the reduction pipeline was completed by M. Radica, with help from G. Tremblay. The initial automation process was completed by C. McRae. Formatting, presentation, subsequent revisions (including automation) and maintenance by C. Lawlor-Forsyth.
