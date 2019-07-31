# README #

These steps outline the procedure to run an automated reduction process which will reduce archival *Chandra* data, compute the concentration, asymmetry, and clumpiness (CAS) parameters, the symmetry, peakiness, and alignment (SPA) parameters, and create Gaussian-Gradient Magnitude (GGM) and unsharp-masked (UM) images for clusters of galaxies present in the [ACCEPT](https://web.pa.msu.edu/astro/MC2/accept/) sample. This reduction adopts the standard flat Lambda-CDM cosmology, with H_0 = 70 km/s /Mpc, Omega_m = 0.3, and Omega_Lambda = 0.7.

## Step 1 - Reduction ##

Open a terminal and navigate to your data/ directory, start CIAO and run `python get_all_data.py` once CIAO is confirmed to be running.
```
cd data/
ciao
python get_all_data.py
```

Upon completion of the previous command, check "data/issues.txt" for any error messages. If an error is recorded, re-run the necessary line from [get_all_data.py](reduction/get_all_data.py) for that cluster, in the terminal. Flags in the "data/issues.txt" file are irrelevant for subsequent steps, and are not used in any way.

Once the desired data has been downloaded, reduced to level 2, reprojected, exposure-corrected, the region-of-interest (ROI) has been created, the point sources have been detected (see [reduce1.py](reduction/reduce1.py)), and there are no error messages present in "data/issues.txt", move on the further analysis steps below.

## Step 2 - Point Source Verification ##

Before continuing with the automated reduction and analysis scripts, we must verify the detected point sources. The sources in "[cluster]/sources.reg" can be viewed in DS9 and any spurious detections can be deleted.
```
ciao
ds9 [cluster]/bin_2/broad_flux.fits -cmap bb -scale log -region [cluster]/sources.reg
```
Save the resulting region file as "[cluster]/sources_mod.reg" in 'ciao' format with 'physical' coordinates.

## Step 3 - CAS Analysis ##

We can now proceed with the CAS analysis of the clusters with sufficient counts for analysis. Note that the quality flags appended in [cas_process_all_data.py](reduction/cas_process_all_data.py) were determined in [reduce1.py](reduction/reduce1.py) by the [ROI_count.py](reduction/ROI_count.py) script.

We need to edit the "cas_process_all_data.py" file to ensure it runs properly. Open gedit (`gedit cas_process_all_data.py`) and add the following lines to the top of the file, then save and close it:
```
# this script assumes Python 3.5 is in use

# imports
import subprocess
```

Ensure that CIAO is running, and then run `python cas_process_all_data.py`.
```
ciao
python cas_process_all_data.py
```

Upon completion of the previous command, there will be a file "data/CAS_parameters_v1.txt" which contains relevant information about each cluster. This file includes the values for the Concentration, Asymmetry, and Clumpiness parameters for each cluster, along with associated 1-sigma uncertainties. Clusters with insufficent counts that have been skipped will have ",,,,,," in the "data/CAS_parameters_v1.txt" file.

An unsharp-masked (UM) image ("unsharp_mask.fits") will be created, and can be found in [cluster]/ROI_2/.

A Gaussian gradient magnitude (GGM) image ("ggm.fits") will also be created, and can be found in [cluster]/ROI/. This image can be used to probe both small- and large-scale structure of the ICM.

## Step 4 - SPA Analysis ##

We can now proceed with the SPA analysis of the clusters with sufficient counts for analysis. Note that the quality flags appended in [spa_process_all_data.py](reduction/spa_process_all_data.py) were determined in [reduce1.py](reduction/reduce1.py) by the [ROI_count.py](reduction/ROI_count.py) script.

We need to edit the "spa_process_all_data.py" file to ensure it runs properly. Open gedit (`gedit spa_process_all_data.py`) and add the following lines to the top of the file, then save and close it:
```
# this script assumes Python 3.5 is in use

# imports
import subprocess
```

Ensure that CIAO is **not** running by simply opening a new terminal, export the shared libraries (for GSL), start HEAsoft, and then run `python spa_process_all_data.py`.
```
cd data
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/home/cam/soft/heasoft-6.26.1/x86_64-pc-linux-gnu-libc2.17/lib
export LD_LIBRARY_PATH
heainit
python spa_process_all_data.py
```

Upon completion of the previous command, there will be a file "data/SPA_parameters_v1.txt" which contains relevant information about each cluster. This file includes the values for the Symmetry, Peakiness, and Alignment parameters for each cluster, along with associated 1-sigma uncertainties. Clusters with insufficent counts that have been skipped will have ",,,,,," in the "data/SPA_parameters_v1.txt" file.

## Conclusion ##

The purpose of this guide was to assist in downloading, reducing, and analyzing archival *Chandra* data, while creating GGM-filtered and UM images, as well as determining the CAS and SPA parameters. Hopefully it was both an informative and useful tool in this regard. Comments, suggestions, and prospective improvements can be sent to C. Lawlor-Forsyth at [lawlorfc@myumanitoba.ca](mailto:lawlorfc@myumanitoba.ca).

### Acknowledgements ###
Much of the early work developing the reduction pipeline was completed by M. Radica, with help from G. Tremblay. The initial automation process was completed by C. McRae. Formatting, presentation, subsequent revisions (including automation) and maintenance by C. Lawlor-Forsyth.
