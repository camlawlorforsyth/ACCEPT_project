# README #

These steps outline the procedure to run an automated reduction process which will reduce archival *Chandra* data, compute the concentration, asymmetry, and clumpiness (CAS) parameters, and create Gaussian-Gradient Magnitude (GGM) and unsharp-masked (UM) images for clusters of galaxies present in the [ACCEPT](https://web.pa.msu.edu/astro/MC2/accept/) sample. This reduction adopts the standard Lambda-CDM cosmology, with H_0 = 70 km/s /Mpc, Omega_m = 0.3, and Omega_Lambda = 0.7.

## Step 0 ##

Create a new data/ directory:
```
mkdir data
```
Copy [reduce/](reduce), [checks/](checks), and [ggm_combine/](ggm_combine) into it.

Copy the following files from the newly copied directories:
```
cp /checks/verify_*.py .
cp /reduce/*_all_data.py .
```

Your data/ directory will now contain three (3) subdirectories (and files therein), and five (5) files.

## Step 1 ##

Open a terminal and navigate to your data/ directory, and start CIAO by entering `ciao` into the terminal.

Once CIAO is confirmed to be running, run `python get_all_data.py`.

Upon completion of the previous command, run `python verify_reproj.py` and check "data/good.txt" for any error messages. If an error is recorded, you will have to re-download and reproject (see: `chandra_reproj`) the data for that cluster. This is accomplished by running the necessary line from [get_all_data.py](reduce/get_all_data.py) for that cluster, in the terminal. Flags in this verify file are irrelevant and are not read in, in subsequent steps.

## Step 2 ##

#### Step 2a ####

Once the desired data has been downloaded, reduced to level 2, reprojected and exposure-corrected (see [reduce1.py](reduce/reduce1.py)), and there are no error messages present in "data/good.txt", the region-of-interest (ROI) and point source analysis can be started. See the [POINT_README](reduce/POINT_README.md) in [reduce/](reduce) for additional information.

#### Step 2b ####

Upon completion of the ROI and point source analysis, ensure the proper flags for bad clusters (`b`) and done clusters (`d`) are correctly appended in [verify_coords.py](reduce/verify_coords.py). 'Done' clusters are those that had sufficient counts for analysis, while clusters that had insufficient counts for statistically significant analysis are referred to as 'bad'.

Next, run `python verify_coords.py` to check that the region files are in the proper coordinates. If there are any issues, re-save the region files in the proper coordinates and re-run `python verify_coords.py`.

Once there are no errors present in "data/good.txt", continue to Step 3 below.

## Step 3 ##

In [cas_process_all_data.py](reduce/cas_process_all_data.py), ensure the proper flags for bad clusters (`b`) and done clusters (`d`) are correctly appended.

Ensure that CIAO is running, and then run `python cas_process_all_data.py`.

Upon completion of the previous command, there will be a file "data/chandrastats.txt" which contains relevant information about each cluster. This file also includes the values for the Asymmetry and Clumpiness parameters for each cluster. 'Bad' clusters will have ",,," in the "data/chandrastats.txt" file, where the ASC parameters would normally be present for 'done' clusters.

An unsharp-masked (UM) image ("unsharp.fits") will also be created, and can be found in [cluster_name]/bin=2/UM.

As the concentration parameter must be computed by hand, navigate to each cluster's directory and open the requisite image. Refer to [concentration_README](reduce/concentration_README.md) for further instructions to compute the concentration value. The corresponding value must then be recorded in "chandrastats.txt".

## Step 4 ##

As in Step 3, ensure that flags in [ggm_all_data.py](reduce/ggm_all_data.py) are corrrect for bad clusters (`b`) and done clusters (`d`).

It is important to ensure that CIAO **is not running** for this step. It is recommended to simply open a new terminal.

From within data/, as with all other steps, run `python ggm_all_data.py`

This will produce several images in the cluster's own ggm_combine/ folder. The image of primary interest is "[cluster_name]\_ggm\_filtered.fits", which can be used to probe both small- and large-scale structure of the ICM.

## Conclusion ##

The purpose of this guide was to assist in downloading, reducing, and analyzing archival *Chandra* data, while creating GGM-filtered and UM images, as well as determining the CAS parameters. Hopefully it was both an informative and useful tool in this regard. Comments, suggestions, and prospective improvements can be sent to C. Lawlor-Forsyth at [lawlorfc@myumanitoba.ca](mailto:lawlorfc@myumanitoba.ca).

### Acknowledgements ###
Much of the early work developing the reduction pipeline was completed by M. Radica, with help from G. Tremblay. The automation process was completed by C. McRae. Formatting, presentation, and subsequent revisions and maintenance by C. Lawlor-Forsyth.
