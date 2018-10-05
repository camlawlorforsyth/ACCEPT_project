# README #
==========

These steps outline the process to run our automated reduction process. This reduction assumes Hubble parameters of Hubble_Constant = 70, Omega_M = 0.3, and Omega_Vac = 0.7.

## Step 0 ##
------------

Create a new data/ directory and copy: reduce/, checks/, and ggm_combine/ into it.

Copy the following files from the newly copied directories: the 2 "verify\_\*.py" files 
from checks/ and the 3 "\*\_all\_data.py" files from reduce into the main data/ directory.

You will now have you main data/ directory, containing three (3) subdirectories (and files therein), and five (5) files.

## Step 1 ##
-------------

Open a terminal and enter you data directory, and start ciao by entering
`ciao`
into the terminal.

Run
`python get_all_data.py`

After this finishes, run
`python verify_reproj.py` and check "good.txt" for any error messages. If an error is recorded, you have to redownload and reproj that cluster. Do so by running 
the command for that cluster contained within "get_all_data.py" on your terminal.
Flags in this verify file are irrelevant and arent read in.

## Step 2 ##
------------

Once you have the clusters you want, and have no error messages, begin the ROI and point sources analysis.
(for more on this, read "POINT_README" in reduce/)

Upon completion of the point source analysis, run "verify_coords.py" to check that you saved all your 
region files in the proper coodinates. If you didn't, resave it in ds9 properly, overwritting the 
previous file.

Once you have no errors and all clusters have been analyzed, move on to step 3

## Step 3 ##
------------

In "process_all_data.py", ensure the proper flags for bad clusters "b" and done clusters "d" are set
if ciao is not running, start ciao again. 
run "process_all_data.py".

Once this is finished you will have a "chandastats.txt" file that contains relevant
information about each cluster, and specifically the asymmetry and cluminess of each cluster. Bad clusters
will simply have ",,," where the CAS parameters would go. 
You will also find an "unsharp.fits" image in clusterName/bin=2/UM

## Step 4 ##
------------

Ensure that flags in "ggm_all_data.py" are corrrect as in the previous step
ensure that ciao IS NOT RUNNING for this step (easiest way is to open a new terminal)

from within the data directory, as with all other steps, run "ggm_all_data.py"

This will produce several images in the clusters own ggm_combine folder. The important one
is "*_ggm_filtered.fits"
