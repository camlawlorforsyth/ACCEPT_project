# README #

These steps outline the procedure to run an automated reduction process which will reduce the *Chandra* data, compute the CAS parameters, and create GGM and unsharp-masked (UM) images. This reduction assumes Hubble parameters of Hubble_Constant = 70, Omega_M = 0.3, and Omega_Vac = 0.7.

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

Open a terminal and enter you data directory, and start CIAO by entering
`ciao`
into the terminal.

Once CIAO is confirmed to be running, run
`python get_all_data.py`.

Upon completion of the previous command, run
`python verify_reproj.py` and check "data/good.txt" for any error messages. If an error is recorded, you will have to re-download and reproject (see: reproj) the data for that cluster. Do so by running the command for that cluster contained within "get_all_data.py" in your terminal. Flags in this verify file are irrelevant and are not read in, in subsequent steps.

## Step 2 ##
START HERE
Once you have the clusters you want, and have no error messages, begin the ROI and point sources analysis.
(for more on this, see the [POINT_README](reduce/POINT_README) in [reduce/](reduce))

Upon completion of the point source analysis, run
`python verify_coords.py` to check that the region files are in the proper coodinates. If there are any issues, re-save the region files in the proper coordinates and re-run
`python verify_coords.py`.

Once you have no errors and all clusters have been analyzed, move on to step 3

## Step 3 ##

In "process_all_data.py", ensure the proper flags for bad clusters "b" and done clusters "d" are set
if ciao is not running, start ciao again. 
run "process_all_data.py".

Once this is finished you will have a "chandastats.txt" file that contains relevant
information about each cluster, and specifically the asymmetry and cluminess of each cluster. Bad clusters
will simply have ",,," where the CAS parameters would go. 
You will also find an "unsharp.fits" image in clusterName/bin=2/UM

## Step 4 ##

Ensure that flags in "ggm_all_data.py" are corrrect as in the previous step.
Ensure that CIAO **is not running** for this step. It is recommended to simply open a new terminal.

From within data/, as with all other steps, run `python ggm_all_data.py`

This will produce several images in the cluster's own ggm_combine/ folder. The important one
is "[clustername]_ggm_filtered.fits".
